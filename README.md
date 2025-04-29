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

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### User Management
- `POST /api/users/register/` - Register new user
- `GET /api/users/me/` - Get current user details
- `PUT /api/users/me/` - Update current user
- `POST /api/users/change_password/` - Change password
- `POST /api/users/forgot_password/` - Request password reset
- `POST /api/users/reset_password/` - Reset password

### Group Management
- `GET /api/groups/` - List all groups
- `POST /api/groups/` - Create new group
- `GET /api/groups/{id}/` - Get group details
- `PUT /api/groups/{id}/` - Update group
- `DELETE /api/groups/{id}/` - Delete group

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


