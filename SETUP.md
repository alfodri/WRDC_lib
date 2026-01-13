# WRDC Library Setup Guide

## Prerequisites

- Python 3.7+
- MongoDB installed and running locally
- pip (Python package manager)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
SECRET_KEY=your-secret-key-here-change-this-in-production
CSRF_SECRET_KEY=your-csrf-secret-key-here
MONGO_URI=mongodb://localhost:27017/library
SESSION_COOKIE_SECURE=False
CACHE_TYPE=simple
```

**Important:** Change the `SECRET_KEY` and `CSRF_SECRET_KEY` to random strings in production!

### 3. Ensure MongoDB is Running

Make sure MongoDB is running on `localhost:27017`. The application will connect to the `library` database.

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://0.0.0.0:5001`

### 5. Default Admin Account

On first run, a default admin account is created:
- **Username:** `admin`
- **Password:** `admin123`

**⚠️ IMPORTANT:** Change this password immediately in production!

## Features

### User Roles

- **Admin**: Full access to all features including user management
- **Editor**: Can add/edit/delete publications and authors
- **Viewer**: Can browse, search, and favorite publications

### API Access

The REST API is available at `/api/v1/`. See API documentation for endpoints.

To get an API token:
```bash
POST /api/v1/auth/login
{
  "username": "admin",
  "password": "admin123"
}
```

Use the returned token in the `Authorization` header:
```
Authorization: Bearer <token>
```

## Project Structure

```
WRDC_lib/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── models/                # Data models
│   ├── user.py
│   ├── publication.py
│   └── author.py
├── routes/                # Route blueprints
│   ├── main.py           # Public routes
│   ├── auth.py           # Authentication routes
│   ├── admin.py          # Admin routes
│   └── api.py            # REST API routes
├── utils/                # Utility functions
│   ├── auth.py          # Authentication helpers
│   └── db.py            # Database helpers
├── templates/           # Jinja2 templates
├── static/             # Static files
└── memory/             # Project documentation
```

## Troubleshooting

### MongoDB Connection Error

If you get a connection error:
1. Ensure MongoDB is running: `mongod --version`
2. Check the `MONGO_URI` in `.env` file
3. Verify MongoDB is accessible on the specified port

### Import Errors

If you get import errors:
1. Ensure you're in the project root directory
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Check Python version: `python --version` (should be 3.7+)

### Port Already in Use

If port 5001 is already in use:
1. Change the port in `app.py`: `app.run(host='0.0.0.0', port=5002)`
2. Or stop the process using port 5001

## Production Deployment

Before deploying to production:

1. **Change all default passwords**
2. **Set strong SECRET_KEY** in `.env`
3. **Set SESSION_COOKIE_SECURE=True** (requires HTTPS)
4. **Disable debug mode** in `app.py`: `debug=False`
5. **Use a production WSGI server** (e.g., Gunicorn)
6. **Set up proper MongoDB authentication**
7. **Configure proper file upload limits**
8. **Set up SSL/TLS certificates**

## Support

For issues or questions, refer to the documentation in the `memory/` folder.
