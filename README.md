# Django User Management System

A robust user management system built with Django REST framework, featuring JWT authentication, user registration, password management, and group-based permissions.

## Features

- 🔐 JWT-based Authentication
- 👤 User Registration and Management
- 🔑 Password Change and Reset
- 👥 Group-based Permissions
- 📧 Email Notifications
- 🔒 Secure Password Validation
- 🚀 RESTful API Endpoints

## Prerequisites

- Python 3.8+
- Django 5.2+
- Django REST Framework
- Django REST Framework SimpleJWT
- SQLite (default) or any other database supported by Django

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd UserManagement
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

### Authentication

#### Login
```http
POST /api/auth/login/
```
Request Body:
```json
{
    "username": "string",
    "password": "string"
}
```
Response (200 OK):
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Logout
```http
POST /api/auth/logout/
```
Headers:
```
Authorization: Bearer <access_token>
```
Request Body:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
Response (200 OK):
```json
{
    "message": "Successfully logged out"
}
```

#### Token Refresh
```http
POST /api/auth/token/refresh/
```
Request Body:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
Response (200 OK):
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Token Verify
```http
POST /api/auth/token/verify/
```
Request Body:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
Response (200 OK):
```json
{}
```

### User Management

#### Register
```http
POST /api/users/register/
```
Request Body:
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
Response (201 Created):
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

#### List Users (Admin Only)
```http
GET /api/users/
```
Headers:
```
Authorization: Bearer <access_token>
```
Response (200 OK):
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

#### Get User Details
```http
GET /api/users/{id}/
```
Headers:
```
Authorization: Bearer <access_token>
```
Response (200 OK):
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

#### Get Current User
```http
GET /api/users/me/
```
Headers:
```
Authorization: Bearer <access_token>
```
Response (200 OK):
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

#### Update Current User
```http
PUT /api/users/me/
```
Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```
Request Body:
```json
{
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string"
}
```
Response (200 OK):
```json
{
    "id": 1,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "is_verified": true,
    "groups": []
}
```

#### Update User (Admin Only)
```http
PUT /api/users/{id}/
```
Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```
Request Body:
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
Response (200 OK):
```json
{
    "id": 1,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "is_verified": true,
    "groups": []
}
```

#### Delete User (Admin Only)
```http
DELETE /api/users/{id}/
```
Headers:
```
Authorization: Bearer <access_token>
```
Response (204 No Content)

#### Change Password
```http
POST /api/users/change_password/
```
Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```
Request Body:
```json
{
    "old_password": "string",
    "new_password": "string",
    "new_password2": "string"
}
```
Response (200 OK):
```json
{
    "message": "Password changed successfully"
}
```

#### Forgot Password
```http
POST /api/users/forgot_password/
```
Request Body:
```json
{
    "email": "string"
}
```
Response (200 OK):
```json
{
    "message": "Password reset link has been sent to your email"
}
```

#### Reset Password
```http
POST /api/users/reset_password/
```
Request Body:
```json
{
    "reset_token": "string",
    "new_password": "string",
    "new_password2": "string"
}
```
Response (200 OK):
```json
{
    "message": "Password has been reset successfully"
}
```

#### Assign Groups to User (Admin Only)
```http
POST /api/users/{id}/assign_groups/
```
Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```
Request Body:
```json
{
    "group_ids": [1, 2]
}
```
Response (200 OK):
```json
{
    "message": "Groups assigned successfully"
}
```

### Group Management

#### List Groups
```http
GET /api/groups/
```
Headers:
```
Authorization: Bearer <access_token>
```
Response (200 OK):
```json
[
    {
        "id": 1,
        "name": "string"
    }
]
```

#### Create Group (Admin Only)
```http
POST /api/groups/
```
Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```
Request Body:
```json
{
    "name": "string"
}
```
Response (201 Created):
```json
{
    "id": 1,
    "name": "string"
}
```

#### Get Group Details
```http
GET /api/groups/{id}/
```
Headers:
```
Authorization: Bearer <access_token>
```
Response (200 OK):
```json
{
    "id": 1,
    "name": "string"
}
```

#### Update Group (Admin Only)
```http
PUT /api/groups/{id}/
```
Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```
Request Body:
```json
{
    "name": "string"
}
```
Response (200 OK):
```json
{
    "id": 1,
    "name": "string"
}
```

#### Delete Group (Admin Only)
```http
DELETE /api/groups/{id}/
```
Headers:
```
Authorization: Bearer <access_token>
```
Response (204 No Content)

### Permission Management

#### List Permissions (Admin Only)
```http
GET /api/permissions/
```
Headers:
```
Authorization: Bearer <access_token>
```
Response (200 OK):
```json
[
    {
        "id": 1,
        "name": "string",
        "codename": "string",
        "content_type": {
            "id": 1,
            "app_label": "string",
            "model": "string"
        }
    }
]
```

#### Assign Permissions to Group (Admin Only)
```http
POST /api/groups/{id}/assign_permissions/
```
Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```
Request Body:
```json
{
    "permission_ids": [1, 2]
}
```
Response (200 OK):
```json
{
    "message": "Permissions assigned successfully"
}
```

### Error Responses

#### 400 Bad Request
```json
{
    "field_name": ["error message"]
}
```

#### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

#### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

#### 404 Not Found
```json
{
    "detail": "Not found."
}
```

#### 429 Too Many Requests
```json
{
    "detail": "Request was throttled."
}
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
FRONTEND_URL=http://localhost:3000
```

## Security Features

- JWT token-based authentication
- Password hashing and validation
- CSRF protection
- Secure password reset flow
- Group-based permission system

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email [your-email@example.com] or open an issue in the repository.

## Acknowledgments

- Django REST Framework
- SimpleJWT
- Django

# Django User Management System API Documentation

A comprehensive guide to the User Management System APIs, featuring JWT authentication, user management, group-based permissions, and password management.

## Table of Contents
1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Group Management](#group-management)
4. [Permission Management](#permission-management)
5. [Error Handling](#error-handling)
6. [Authentication Flow](#authentication-flow)
7. [Security Considerations](#security-considerations)

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

## Authentication Flow

1. User logs in with username/password
2. System returns JWT access and refresh tokens
3. User includes access token in Authorization header for protected endpoints
4. When access token expires, user can get a new one using refresh token
5. User can logout to invalidate refresh token

## Security Considerations

1. All sensitive endpoints require authentication
2. Password reset tokens expire after 24 hours
3. JWT tokens are used for authentication
4. Admin-only endpoints are protected by IsAdminUser permission
5. Password validation enforces complexity requirements
6. Rate limiting is implemented for sensitive endpoints
7. CSRF protection is enabled
8. Secure password reset flow with email verification

## Rate Limits

- Login attempts: 5 per minute
- Password reset requests: 3 per hour
- API requests: 1000 per day per user

## Environment Variables

Required environment variables:
```env
DEBUG=True
SECRET_KEY=your-secret-key
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
FRONTEND_URL=http://localhost:3000
```

## Testing

Run the test suite:
```bash
python manage.py test
```

## Support

For support, email [your-email@example.com] or open an issue in the repository.


