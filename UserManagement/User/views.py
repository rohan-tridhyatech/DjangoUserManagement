from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .serializers import (
    UserRegistrationSerializer, UserSerializer, GroupSerializer
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

class UserLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
