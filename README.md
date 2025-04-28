# Django User Management System

A comprehensive user management system built with Django REST Framework, featuring authentication, role-based access control, and user management capabilities.

## Features

- User Authentication (Registration, Login, Token Refresh)
- Role-Based Access Control using Django Groups
- User Profile Management
- Group Management
- Permission Management
- Admin Interface Integration

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
    "last_name": "string"
}
```
Response:
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string"
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

#### 3. Token Refresh
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
GET /api/auth/users/{id}/
```
Headers:
```
Authorization: Bearer <access_token>
```
Response:
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "groups": [
        {
            "id": "integer",
            "name": "string"
        }
    ]
}
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
    "last_name": "string"
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


