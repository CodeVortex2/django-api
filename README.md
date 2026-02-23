# Django REST API with JWT Authentication

A complete, production-ready Django REST API with JWT authentication and CRUD operations.

## Features

- **JWT Authentication** - Secure token-based authentication using djangorestframework-simplejwt
- **User Management** - Registration, login, logout, profile management, password change
- **CRUD Operations** - Full CRUD for Articles and Comments
- **Custom User Model** - Extended user model with additional fields
- **API Documentation** - browsable API interface
- **Security** - CORS support, permission classes, password validation
- **Pagination** - Built-in pagination for list endpoints
- **Search & Filtering** - Search and ordering capabilities

## Project Structure

```
django-api/
├── core/                    # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py             # Root URL configuration
│   ├── wsgi.py             # WSGI entry point
│   └── asgi.py             # ASGI entry point
├── accounts/               # User authentication app
│   ├── models.py           # Custom User model
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # Authentication views
│   ├── urls.py             # Auth URL routes
│   └── admin.py            # Admin configuration
├── api/                    # Main API app (CRUD)
│   ├── models.py          # Article & Comment models
│   ├── serializers.py      # DRF serializers
│   ├── views.py           # ViewSets
│   ├── urls.py            # API URL routes
│   └── admin.py           # Admin configuration
├── manage.py              # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project**

   ```bash
   cd django-api
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   # On Linux/Mac
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   The API will be available at: http://127.0.0.1:8000/

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/logout/` | User logout |
| POST | `/api/auth/refresh/` | Refresh access token |
| POST | `/api/auth/verify/` | Verify access token |
| GET | `/api/auth/profile/` | Get current user profile |
| PUT/PATCH | `/api/auth/profile/` | Update user profile |
| POST | `/api/auth/change-password/` | Change password |

### Article Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/articles/` | List all articles |
| POST | `/api/articles/` | Create new article |
| GET | `/api/articles/{slug}/` | Get article details |
| PUT/PATCH | `/api/articles/{slug}/` | Update article |
| DELETE | `/api/articles/{slug}/` | Delete article |
| POST | `/api/articles/{slug}/publish/` | Publish article |
| POST | `/api/articles/{slug}/unpublish/` | Unpublish article |

### Comment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/comments/` | List all comments |
| POST | `/api/comments/` | Create new comment |
| GET | `/api/comments/{id}/` | Get comment details |
| PUT/PATCH | `/api/comments/{id}/` | Update comment |
| DELETE | `/api/comments/{id}/` | Delete comment |

## Usage Examples

### Using cURL

#### 1. Register a new user

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    ...
  },
  "tokens": {
    "refresh": "<refresh_token>",
    "access": "<access_token>"
  },
  "message": "User registered successfully."
}
```

#### 2. Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'
```

#### 3. Get Profile (Authenticated)

```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer <access_token>"
```

#### 4. Create an Article (Authenticated)

```bash
curl -X POST http://127.0.0.1:8000/api/articles/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Article",
    "slug": "my-first-article",
    "content": "This is the content of my first article.",
    "is_published": true
  }'
```

#### 5. List Articles

```bash
curl -X GET http://127.0.0.1:8000/api/articles/
```

#### 6. Refresh Token

```bash
curl -X POST http://127.0.0.1:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<refresh_token>"
  }'
```

### Using Python (requests library)

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Register
register_data = {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
}
response = requests.post(f"{BASE_URL}/api/auth/register/", json=register_data)
tokens = response.json()["tokens"]
access_token = tokens["access"]
refresh_token = tokens["refresh"]

# Create Article
headers = {"Authorization": f"Bearer {access_token}"}
article_data = {
    "title": "My First Article",
    "slug": "my-first-article",
    "content": "Article content here.",
    "is_published": True
}
response = requests.post(f"{BASE_URL}/api/articles/", json=article_data, headers=headers)
print(response.json())

# Refresh Token
refresh_data = {"refresh": refresh_token}
response = requests.post(f"{BASE_URL}/api/auth/refresh/", json=refresh_data)
new_access = response.json()["access"]
```

### Using JavaScript (fetch API)

```javascript
const BASE_URL = "http://127.0.0.1:8000";

// Register
async function register() {
  const response = await fetch(`${BASE_URL}/api/auth/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'johndoe',
      email: 'john@example.com',
      password: 'SecurePassword123!',
      password_confirm: 'SecurePassword123!',
      first_name: 'John',
      last_name: 'Doe'
    })
  });
  const data = await response.json();
  return data.tokens;
}

// Login
async function login(email, password) {
  const response = await fetch(`${BASE_URL}/api/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  return data.tokens;
}

// Get Articles
async function getArticles(accessToken) {
  const response = await fetch(`${BASE_URL}/api/articles/`, {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  });
  return response.json();
}
```

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Admin Interface

Access the Django admin at: http://127.0.0.1:8000/admin/

## Testing

Run tests with:

```bash
python manage.py test
```

## Security Notes

1. **Change SECRET_KEY** - In production, use a strong, unique secret key
2. **Set DEBUG=False** - Disable debug mode in production
3. **Configure CORS** - Update CORS settings in `core/settings.py` for production
4. **Use HTTPS** - Always use HTTPS in production
5. **Password Requirements** - The API enforces strong password validation

## JWT Token Details

- **Access Token**: Valid for 60 minutes (configurable in settings)
- **Refresh Token**: Valid for 1 day (configurable in settings)
- **Token Type**: Bearer

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License
