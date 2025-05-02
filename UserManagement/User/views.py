from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from allauth.socialaccount.models import SocialApp
from urllib.parse import urlencode
import requests
from .serializers import (
    UserRegistrationSerializer, UserSerializer, GroupSerializer,
    ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer,
    PermissionSerializer
)

# Get the User model
User = get_user_model()

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class GroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Group model operations.
    Handles CRUD operations and custom actions for group management.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['post'])
    def assign_permissions(self, request, pk=None):
        """
        Custom action for assigning permissions to a group.
        Replaces all existing permissions with the new ones.
        """
        permission_ids = request.data.get('permission_ids')
        if not permission_ids:
            return Response(
                {"error": "permission_ids is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            group = self.get_object()
            permissions = Permission.objects.filter(id__in=permission_ids)
            group.permissions.set(permissions)
            return Response(
                {"message": "Permissions assigned successfully"},
                status=status.HTTP_200_OK
            )
        except Permission.DoesNotExist:
            return Response(
                {"error": "One or more permissions not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_permissions(self, request, pk=None):
        """
        Custom action for removing permissions from a group.
        Removes only the specified permissions while keeping others intact.
        """
        permission_ids = request.data.get('permission_ids')
        if not permission_ids:
            return Response(
                {"error": "permission_ids is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            group = self.get_object()
            permissions = Permission.objects.filter(id__in=permission_ids)
            group.permissions.remove(*permissions)
            return Response(
                {"message": "Permissions removed successfully"},
                status=status.HTTP_200_OK
            )
        except Permission.DoesNotExist:
            return Response(
                {"error": "One or more permissions not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model operations.
    Handles CRUD operations and custom actions for user management.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Override to allow registration without authentication.
        """
        if self.action == 'register':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        elif user.groups.filter(name="Manager").exists():
            return User.objects.exclude(is_superuser=True)
        return User.objects.filter(id=user.id)


    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Custom action for user registration.
        Allows new users to create an account.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "message": "User created successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        """
        Custom action for changing user password.
        Requires the old password for verification.
        """
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not request.user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": ["Wrong password."]}, 
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

    @action(detail=False, methods=['post'])
    def forgot_password(self, request):
        """
        Custom action for handling forgot password requests.
        Generates a reset token and sends it via email.
        """
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

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        """
        Custom action for resetting password using the reset token.
        Validates the token and sets the new password.
        """
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

class UserLogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Permission model operations.
    Provides read-only access to permissions and custom actions for permission management.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAdminUser]

class GoogleLoginRedirect(APIView):
    """
    View to initiate Google OAuth2 login flow.
    Returns the Google OAuth2 authorization URL.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            app = SocialApp.objects.get(provider='google')
            params = {
                "client_id": app.client_id,
                "redirect_uri": request.build_absolute_uri('/api/auth/google/callback/'),
                "response_type": "code",
                "scope": "openid email profile",
                "access_type": "offline",
                "prompt": "consent"
            }
            url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
            return Response({"auth_url":url})
        except SocialApp.DoesNotExist:
            return Response(
                {"error": "Google OAuth configuration not found"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GoogleCallbackView(APIView):
    """
    View to handle Google OAuth2 callback.
    Processes the authorization code, creates/updates user, and returns JWT tokens.
    """
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        code = request.GET.get("code")
        
        if not code:
            return Response(
                {"error": "No authorization code provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            app = SocialApp.objects.get(provider="google")
            data = {
                "code": code,
                "client_id": app.client_id,
                "client_secret": app.secret,
                "redirect_uri": request.build_absolute_uri('/api/auth/google/callback/'),
                "grant_type": "authorization_code"
            }

            # Exchange code for token
            token_response = requests.post("https://oauth2.googleapis.com/token", data=data)
            token_response.raise_for_status()  # Raise exception for bad status codes
            token_data = token_response.json()

            access_token = token_data.get("access_token")
            if not access_token:
                return Response(
                    {"error": "Failed to obtain access token"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get user info from Google
            user_info_response = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            user_info_response.raise_for_status()
            user_info = user_info_response.json()

            if not user_info.get("email"):
                return Response(
                    {"error": "Email not provided by Google"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create or update user
            user, created = User.objects.get_or_create(
                email=user_info["email"],
                defaults={
                    "username": user_info["email"].split("@")[0],
                    "first_name": user_info.get("given_name", ""),
                    "last_name": user_info.get("family_name", "")
                }
            )

            # Create JWT tokens
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            refresh = str(refresh)


            # Return tokens in JSON response
            return Response({
                'code':code,
                "access_token": access,
                "refresh_token": refresh,
                "user": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            })

        except SocialApp.DoesNotExist:
            return Response(
                {"error": "Google OAuth configuration not found"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except requests.RequestException as e:
            return Response(
                {"error": f"Failed to communicate with Google: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )