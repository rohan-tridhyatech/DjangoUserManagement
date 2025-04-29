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


