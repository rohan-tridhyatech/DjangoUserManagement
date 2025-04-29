from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .serializers import (
    UserRegistrationSerializer, UserSerializer, GroupSerializer,
    ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
)

User = get_user_model()

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_permissions(self):
        if self.action == 'register':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_groups(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {"error": "Only admin users can assign groups"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        user = self.get_object()
        group_ids = request.data.get('group_ids', [])
        
        if not group_ids:
            return Response(
                {"error": "group_ids is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            groups = Group.objects.filter(id__in=group_ids)
            user.groups.set(groups)
            return Response(
                {"message": "Groups assigned successfully"},
                status=status.HTTP_200_OK
            )
        except Group.DoesNotExist:
            return Response(
                {"error": "One or more groups not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not request.user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"error": "Old password is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            
            return Response(
                {"message": "Password changed successfully"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate reset token
                reset_token = get_random_string(length=32)
                user.reset_token = reset_token
                user.save()
                
                # Send email with reset link
                reset_link = f"{settings.FRONTEND_URL}/reset-password/{reset_token}"
                send_mail(
                    'Password Reset Request',
                    f'Click the following link to reset your password: {reset_link}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                
                return Response(
                    {"message": "Password reset link has been sent to your email"},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            reset_token = serializer.validated_data['reset_token']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(reset_token=reset_token)
                user.set_password(new_password)
                user.reset_token = None  # Clear the reset token
                user.save()
                
                return Response(
                    {"message": "Password has been reset successfully"},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid reset token"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class UserLogoutView(TokenBlacklistView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return Response(
                    {"error": "User is not authenticated"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Check for refresh token
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the authorization header
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return Response(
                    {"error": "Invalid authorization header format"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Try to blacklist the token
            try:
                return super().post(request, *args, **kwargs)
            except Exception as e:
                return Response(
                    {"error": f"Failed to blacklist token: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
