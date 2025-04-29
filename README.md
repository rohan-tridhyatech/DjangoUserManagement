# Django User Management System API Documentation

A comprehensive guide to the User Management System APIs, featuring JWT authentication, user management, group-based permissions, and password management.

## Table of Contents
1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Group Management](#group-management)
4. [Permission Management](#permission-management)

## Authentication

### Login
```http
POST /api/auth/login/
```
Authenticate user and receive JWT tokens.

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Notes:**
- The access token is used for API authentication
- The refresh token is used to obtain a new access token
- Tokens expire after a configured time (default: 5 minutes for access, 24 hours for refresh)

### Logout
```http
POST /api/auth/logout/
```
Invalidate the refresh token.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
    "message": "Successfully logged out"
}
```

## User Management

### Register User
```http
POST /api/users/register/
```
Create a new user account.

**Request Body:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "password2": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "group_ids": [1, 2]  // Optional
}
```

**Response (201 Created):**
```json
{
    "user": {
        "id": 1,
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "phone_number": "string",
        "is_verified": false,
        "groups": []
    },
    "message": "User created successfully"
}
```

**Validation Rules:**
- Username must be unique
- Email must be unique and valid
- Password must meet complexity requirements
- Passwords must match
- Phone number must be valid (if provided)

### List Users
```http
GET /api/users/
```
Get list of all users (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "phone_number": "string",
        "is_verified": true,
        "groups": [
            {
                "id": 1,
                "name": "string"
            }
        ]
    }
]
```

### Get User Details
```http
GET /api/users/{id}/
```
Get specific user details.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "is_verified": true,
    "groups": [
        {
            "id": 1,
            "name": "string"
        }
    ]
}
```

### Update User
```http
PUT /api/users/{id}/
```
Update user information (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "is_active": true,
    "is_staff": false,
    "is_superuser": false
}
```

### Delete User
```http
DELETE /api/users/{id}/
```
Delete user account (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

### Change Password
```http
POST /api/users/change_password/
```
Change user password.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "old_password": "string",
    "new_password": "string",
    "new_password2": "string"
}
```

**Response (200 OK):**
```json
{
    "message": "Password changed successfully"
}
```

### Forgot Password
```http
POST /api/users/forgot_password/
```
Request password reset.

**Request Body:**
```json
{
    "email": "string"
}
```

**Response (200 OK):**
```json
{
    "message": "Password reset link has been sent to your email"
}
```

### Reset Password
```http
POST /api/users/reset_password/
```
Reset password with token.

**Request Body:**
```json
{
    "reset_token": "string",
    "new_password": "string",
    "new_password2": "string"
}
```

**Response (200 OK):**
```json
{
    "message": "Password has been reset successfully"
}
```

## Group Management

### List Groups
```http
GET /api/groups/
```
Get list of all groups.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "name": "string"
    }
]
```

### Create Group
```http
POST /api/groups/
```
Create new group (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "name": "string"
}
```

### Get Group Details
```http
GET /api/groups/{id}/
```
Get specific group details.

**Headers:**
```
Authorization: Bearer <access_token>
```

### Update Group
```http
PUT /api/groups/{id}/
```
Update group information (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "name": "string"
}
```

### Delete Group
```http
DELETE /api/groups/{id}/
```
Delete group (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

### Assign Permissions to Group
```http
POST /api/groups/{id}/assign_permissions/
```
Assign permissions to group (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "permission_ids": [1, 2]
}
```

**Response (200 OK):**
```json
{
    "message": "Permissions assigned successfully"
}
```

### Remove Permissions from Group
```http
POST /api/groups/{id}/remove_permissions/
```
Remove permissions from group (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "permission_ids": [1, 2]
}
```

**Response (200 OK):**
```json
{
    "message": "Permissions removed successfully"
}
```

## Permission Management

### List Permissions
```http
GET /api/permissions/
```
Get list of all permissions (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "name": "Can add user",
        "codename": "add_user",
        "content_type": {
            "id": 1,
            "app_label": "auth",
            "model": "user"
        }
    }
]
```

### Get Permission Details
```http
GET /api/permissions/{id}/
```
Get specific permission details (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

### Assign Permission to Group
```http
POST /api/permissions/{id}/assign_to_group/
```
Assign permission to group (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "group_id": 1
}
```

**Response (200 OK):**
```json
{
    "message": "Permission assigned to group successfully"
}
```

### Remove Permission from Group
```http
POST /api/permissions/{id}/remove_from_group/
```
Remove permission from group (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "group_id": 1
}
```

**Response (200 OK):**
```json
{
    "message": "Permission removed from group successfully"
}
```

## Error Handling

### 400 Bad Request
```json
{
    "field_name": ["error message"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 429 Too Many Requests
```json
{
    "detail": "Request was throttled."
}
```