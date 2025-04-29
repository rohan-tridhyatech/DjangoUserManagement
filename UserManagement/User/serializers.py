from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group, Permission

# Get the User model
User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for Group model.
    Handles serialization and deserialization of group data.
    """
    class Meta:
        model = Group
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Handles serialization and deserialization of user data including groups.
    """
    # Serialize groups as nested objects
    groups = GroupSerializer(many=True, read_only=True)
    
    # Allow writing group IDs directly
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
    """
    Serializer for user registration.
    Handles validation and creation of new users.
    """
    # Password fields with validation
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    # Allow writing group IDs directly
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
        """
        Validate that the two password fields match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    Validates old password and new password requirements.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Validate that the two new password fields match.
        """
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for forgot password requests.
    Validates email format and existence.
    """
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation.
    Validates reset token and new password requirements.
    """
    reset_token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Validate that the two new password fields match.
        """
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Permission model.
    Handles serialization of permission data including content type information.
    """
    # Custom field to get content type information
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename', 'content_type')

    def get_content_type(self, obj):
        """
        Get content type information for the permission.
        Returns a dictionary with content type details.
        """
        return {
            'id': obj.content_type.id,
            'app_label': obj.content_type.app_label,
            'model': obj.content_type.model
        } 