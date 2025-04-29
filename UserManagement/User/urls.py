from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, GroupViewSet,
    UserLoginView, UserLogoutView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
]
