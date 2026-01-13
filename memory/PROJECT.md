# PROJECT.md

**Last Updated:** 2026-01-13

---

## Project Overview

**Project Name:** WRDC_lib (Water Resources Development Center Digital Library)

**Purpose:** A web-based digital library system for managing and accessing technical publications related to water resources, desalination, and water treatment equipment at the Kuwait Ministry of Electricity and Water (MEW).

**Primary Use Case:** 
- Store and organize technical reports on water treatment equipment (evaporators, heat exchangers, MSF systems)
- Provide searchable access to historical technical documentation (1972-1980+)
- Showcase author profiles and their contributions
- Enable user-contributed content (all logged-in users can add publications)
- Admin management of content and users

---

## Tech Stack

### Backend
- **Framework:** Flask 3.0.0 (Python web framework)
- **Database:** MongoDB (local instance at `mongodb://localhost:27017/library`)
- **Extensions:** 
  - Flask-PyMongo 2.3.0 (MongoDB integration)
  - Flask-WTF 1.2.1 (CSRF protection)
  - Flask-Caching 2.1.0 (Performance caching)
  - Flask-Login 0.6.3 (Session management)
- **Authentication:** bcrypt 4.1.2 (Password hashing)
- **API:** PyJWT 2.8.0 (JWT tokens)
- **File Handling:** Werkzeug 3.0.1 (secure file uploads)
- **Configuration:** python-dotenv 1.0.0 (Environment variables)

### Frontend
- **UI Framework:** Bootstrap 4.5.2
- **Visualization:** Chart.js (publication statistics)
- **PDF Rendering:** Native browser `<embed>` tag

### Dependencies
```
Flask==3.0.0
Flask-PyMongo==2.3.0
Flask-WTF==1.2.1
Flask-Caching==2.1.0
Flask-Login==0.6.3
python-dotenv==1.0.0
bcrypt==4.1.2
PyJWT==2.8.0
email-validator>=2.1.1
Werkzeug==3.0.1
pymongo==4.6.1
```

---

## Database

**MongoDB Database:** `library`

**Collections:**
1. `publications` - Technical reports and documents
2. `authors` - Author profiles and information
3. `users` - User accounts with roles and authentication

---

## File Structure

```
WRDC_lib/
├── app.py                    # Main Flask application (refactored)
├── config.py                 # Configuration management
├── .env                      # Environment variables (not in git)
├── requirements.txt          # Python dependencies
├── SETUP.md                  # Setup instructions
├── IMPLEMENTATION_SUMMARY.md # Implementation details
├── models/                   # Data models
│   ├── __init__.py
│   ├── user.py              # User model
│   ├── publication.py       # Publication model
│   └── author.py            # Author model
├── routes/                   # Route blueprints
│   ├── __init__.py
│   ├── main.py              # Public routes
│   ├── auth.py              # Authentication routes
│   ├── admin.py             # Admin routes
│   └── api.py               # REST API routes
├── utils/                    # Utility functions
│   ├── __init__.py
│   ├── auth.py              # Authentication helpers
│   └── db.py                # Database helpers
├── static/                   # Static files
│   ├── css/                 # CSS files
│   ├── js/                  # JavaScript files
│   └── uploads/             # Uploaded files
│       ├── pdfs/            # PDF documents
│       ├── covers/          # Publication covers
│       └── authors/         # Author pictures
├── templates/               # Jinja2 HTML templates
│   ├── auth/
│   │   └── register.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── add_content.html
│   │   ├── publications.html
│   │   ├── edit_publication.html
│   │   ├── authors.html
│   │   ├── edit_author.html
│   │   └── users.html
│   ├── index.html
│   ├── author.html
│   ├── author_info.html
│   ├── view_pdf.html
│   ├── guideline.html
│   ├── login.html
│   └── admin.html           # Legacy admin form
└── memory/                  # Project documentation
```

---

## How to Run

### Prerequisites
1. MongoDB installed and running locally
2. Python 3.7+ installed
3. Virtual environment (recommended)

### Installation Steps
```bash
# Create virtual environment (if not exists)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example or use generated one)
# Ensure MongoDB is running
# Default connection: mongodb://localhost:27017/library

# Run the application
python app.py
```

### Access Points
- **Application:** http://0.0.0.0:5001
- **Login:** http://0.0.0.0:5001/auth/login
- **Register:** http://0.0.0.0:5001/auth/register
- **Add Content:** http://0.0.0.0:5001/admin/add (requires login)
- **Admin Dashboard:** http://0.0.0.0:5001/admin/dashboard (admin only)
- **API Base:** http://0.0.0.0:5001/api/v1/

### Default Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- ⚠️ **IMPORTANT:** Change this password in production!

---

## Key Features

1. **User Management** - Registration, authentication, role-based access
2. **Publication Management** - Upload, store, display, edit, delete technical PDFs
3. **Author Management** - Create and manage author profiles
4. **Advanced Search** - Enhanced search across title, author, category
5. **Analytics** - Publication statistics with Chart.js visualizations
6. **PDF Viewer** - In-browser PDF reading experience
7. **Content Contribution** - All logged-in users can add publications
8. **Admin Panel** - Comprehensive content and user management
9. **REST API** - Full API with JWT authentication
10. **Performance** - Caching and database optimization

---

## Configuration

### Environment Variables (.env)
- **SECRET_KEY** - Flask secret key (auto-generated)
- **CSRF_SECRET_KEY** - CSRF protection key (auto-generated)
- **MONGO_URI** - MongoDB connection string (default: `mongodb://localhost:27017/library`)
- **SESSION_COOKIE_SECURE** - Set to `True` in production with HTTPS
- **CACHE_TYPE** - Cache backend (`simple` for development)

### Upload Settings
- **Upload Folder:** `static/uploads/`
- **Allowed Extensions:** pdf, png, jpg, jpeg, gif
- **Subfolders:** pdfs/, covers/, authors/

### Security Notes
- ✅ Secure password hashing with bcrypt
- ✅ Environment-based configuration
- ✅ Session security with configurable cookies
- ✅ CSRF protection enabled
- ✅ File upload validation
- ⚠️ Change default admin password in production
- ⚠️ Set SESSION_COOKIE_SECURE=True in production
- ⚠️ Disable debug mode in production

---

## Environment

- **Host:** 0.0.0.0 (accessible from network)
- **Port:** 5001
- **Debug Mode:** Enabled (disable in production)
- **Cache:** Simple in-memory cache (can upgrade to Redis)

---

## Permission Model

**Viewer (default):**
- Browse, search, view publications
- Add publications and authors
- Manage favorites

**Editor:**
- All viewer permissions
- Edit/delete publications and authors

**Admin:**
- All editor permissions
- Access admin dashboard
- Manage users
