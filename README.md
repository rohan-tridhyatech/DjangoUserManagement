# Django User Management System

A comprehensive user management system built with Django REST Framework, featuring authentication, role-based access control, and user management capabilities.

## Features

- User Authentication (Registration, Login, Logout)
- Social Authentication (Google Login)
- Password Management (Change Password, Forgot Password, Reset Password)
- Role-Based Access Control using Django Groups
- User Profile Management
- Group Management
- Permission Management
- Admin Interface Integration
- JWT Token Authentication

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Configure email settings in settings.py:
   ```python
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'
   ```
7. Configure Google OAuth2 settings in settings.py:
   ```python
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your-google-client-id'
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your-google-client-secret'
   ```

## API Documentation

### Authentication APIs

#### 1. User Registration
```http
POST /api/auth/users/register/
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
    "phone_number": "string"
}
```
Response:
```json
{
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string"
    },
    "message": "User created successfully"
}
```

#### 2. User Login
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
Response:
```json
{
    "access": "string",
    "refresh": "string"
}
```

#### 3. User Logout
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
    "refresh": "string"
}
```

#### 4. Google Login
```http
POST /api/auth/google-login/
```
Request Body:
```json
{
    "access_token": "google-oauth2-access-token"
}
```
Response:
```json
{
    "access": "string",
    "refresh": "string",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string"
    }
}
```

#### 5. Change Password
```http
POST /api/auth/users/change_password/
```
Headers:
```
Authorization: Bearer <access_token>
```
Request Body:
```json
{
    "old_password": "string",
    "new_password": "string",
    "confirm_password": "string"
}
```

#### 6. Forgot Password
```http
POST /api/auth/users/forgot_password/
```
Request Body:
```json
{
    "email": "string"
}
```

#### 7. Reset Password
```http
POST /api/auth/users/reset_password/
```
Request Body:
```json
{
    "reset_token": "string",
    "new_password": "string",
    "confirm_password": "string"
}
```

#### 8. Token Refresh
```http
POST /api/auth/token/refresh/
```
Request Body:
```json
{
    "refresh": "string"
}
```
Response:
```json
{
    "access": "string"
}
```

### User Management APIs

#### 1. Get User Profile
```http
GET /api/auth/users/me/
```
Headers:
```
Authorization: Bearer <access_token>
```

#### 2. Update User Profile
```http
PUT /api/auth/users/{id}/
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
    "phone_number": "string"
}
```

#### 3. Delete User
```http
DELETE /api/auth/users/{id}/
```
Headers:
```
Authorization: Bearer <access_token>
```

#### 4. Assign Groups to User
```http
POST /api/auth/users/{id}/assign_groups/
```
Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```
Request Body:
```json
{
    "group_ids": ["integer"]
}
```

### Group Management APIs

#### 1. Create Group
```http
POST /api/auth/groups/
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

#### 2. List Groups
```http
GET /api/auth/groups/
```
Headers:
```
Authorization: Bearer <access_token>
```

#### 3. Get Group Details
```http
GET /api/auth/groups/{id}/
```
Headers:
```
Authorization: Bearer <access_token>
```

#### 4. Update Group
```http
PUT /api/auth/groups/{id}/
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

#### 5. Delete Group
```http
DELETE /api/auth/groups/{id}/
```
Headers:
```
Authorization: Bearer <access_token>
```

## Permission Requirements

- User Registration: No authentication required
- User Login: No authentication required
- Token Refresh: No authentication required
- User Profile Management: Requires authentication
- Group Management: Requires admin privileges
- User Deletion: Requires admin privileges

## Error Responses

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

## Security Features

1. JWT Token Authentication
2. Password Validation
3. Email Verification
4. Token Blacklisting for Logout
5. Role-Based Access Control
6. Google OAuth2 Authentication

## Development

1. Run development server:
   ```bash
   python manage.py runserver
   ```

2. Run tests:
   ```bash
   python manage.py test
   ```

## Production Deployment

For production deployment:

1. Set DEBUG = False in settings.py
2. Use secure email settings
3. Configure proper database (e.g., PostgreSQL)
4. Set up proper CORS settings
5. Use environment variables for sensitive data
6. Configure proper static file serving
7. Set up proper SSL/TLS certificates

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request


