from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserLoginView, GroupViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginView.as_view(), name='user-login'),
]
