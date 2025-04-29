from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    group_ids = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        source='groups',
        write_only=True,
        many=True,
        required=False
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                 'phone_number', 'is_verified', 'created_at', 'updated_at',
                 'groups', 'group_ids')
        read_only_fields = ('is_verified', 'created_at', 'updated_at')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    group_ids = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        source='groups',
        write_only=True,
        many=True,
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name',
                 'phone_number', 'group_ids')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    reset_token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs 