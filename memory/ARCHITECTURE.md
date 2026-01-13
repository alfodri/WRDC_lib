# ARCHITECTURE.md

**Last Updated:** 2026-01-13

---

## Application Architecture

**Type:** Modular Flask Web Application with Blueprints  
**Pattern:** MVC (Model-View-Controller) via Flask + Jinja2 + Blueprints  
**Database:** Document-oriented (MongoDB)  
**Authentication:** bcrypt password hashing, session-based with role-based access control

---

## Flask Routes

### Public Routes (main_bp)

| Route | Method | Template | Purpose |
|-------|--------|----------|---------|
| `/` | GET | `index.html` | Homepage with publication grid, search, filters, pagination |
| `/authors` | GET | `author.html` | List all authors with profile pictures |
| `/author/<author_id>` | GET | `author_info.html` | Individual author profile with publications and stats |
| `/view_pdf/<publication_id>` | GET | `view_pdf.html` | PDF viewer with publication metadata |
| `/guideline` | GET | `guideline.html` | Author submission guidelines |

### Authentication Routes (auth_bp)

| Route | Method | Template | Purpose |
|-------|--------|----------|---------|
| `/auth/login` | GET, POST | `login.html` | User login with username/password |
| `/auth/register` | GET, POST | `auth/register.html` | User registration |
| `/auth/logout` | GET | Redirect | Clear session and logout |
| `/auth/profile` | GET | Redirect | User profile (redirects to index) |
| `/auth/favorites` | GET, POST, DELETE | Redirect | Manage favorite publications |

### Admin Routes (admin_bp)

| Route | Method | Template | Purpose |
|-------|--------|----------|---------|
| `/admin/` | GET | Redirect | Redirects to dashboard |
| `/admin/dashboard` | GET | `admin/dashboard.html` | Admin dashboard with statistics (admin only) |
| `/admin/add` | GET | `admin/add_content.html` | Add content page (all logged-in users) |
| `/admin/publications` | GET | `admin/publications.html` | List all publications (editor/admin) |
| `/admin/add_publication` | POST | Redirect | Add new publication (all logged-in users) |
| `/admin/edit_publication/<id>` | GET, POST | `admin/edit_publication.html` | Edit publication (editor/admin) |
| `/admin/delete_publication/<id>` | POST | Redirect | Delete publication (editor/admin) |
| `/admin/authors` | GET | `admin/authors.html` | List all authors (editor/admin) |
| `/admin/add_author` | POST | Redirect | Add new author (all logged-in users) |
| `/admin/edit_author/<id>` | GET, POST | `admin/edit_author.html` | Edit author (editor/admin) |
| `/admin/delete_author/<id>` | POST | Redirect | Delete author (editor/admin) |
| `/admin/users` | GET | `admin/users.html` | List all users (admin only) |

### API Routes (api_bp)

| Route | Method | Purpose |
|-------|--------|---------|
| `/api/v1/publications` | GET, POST | List/create publications |
| `/api/v1/publications/<id>` | GET, PUT, DELETE | Single publication CRUD |
| `/api/v1/authors` | GET | List authors |
| `/api/v1/authors/<id>` | GET | Get single author |
| `/api/v1/categories` | GET | List categories |
| `/api/v1/search` | GET | Search publications |
| `/api/v1/stats` | GET | Library statistics |
| `/api/v1/auth/login` | POST | Get JWT token for API access |

---

## MongoDB Schema

### Collection: `publications`

```javascript
{
  "_id": ObjectId,
  "title": String,              // Publication title
  "author": String,             // Author name (references authors.name)
  "category": String,           // e.g., "Evaporator", "Heat Exchanger"
  "publish_date": String,       // ISO format date string (YYYY-MM-DD)
  "pdf_filename": String,       // Filename in static/uploads/pdfs/
  "cover_filename": String,     // Filename in static/uploads/covers/
  "created_at": DateTime,       // Creation timestamp
  "updated_at": DateTime,       // Last update timestamp
  "download_count": Number,     // Download counter
  "view_count": Number          // View counter
}
```

**Indexes:**
- Text index on `title`, `category`, `author` (for full-text search)
- Regular indexes on `author`, `category`, `publish_date`, `created_at`

### Collection: `authors`

```javascript
{
  "_id": ObjectId,
  "name": String,               // Full name (unique identifier)
  "profile": String,            // Short bio/profile text
  "education": String,          // Educational background
  "experience": String,         // Work experience and internships
  "skills": String,             // Technical skills
  "image": String,              // Filename in static/uploads/authors/
  "created_at": DateTime,       // Creation timestamp
  "updated_at": DateTime         // Last update timestamp
}
```

**Indexes:**
- Index on `name`

### Collection: `users` (NEW)

```javascript
{
  "_id": ObjectId,
  "username": String,           // Unique username
  "email": String,              // Unique email
  "password_hash": String,       // bcrypt hashed password
  "role": String,                // "admin" | "editor" | "viewer"
  "created_at": DateTime,        // Account creation date
  "last_login": DateTime,        // Last login timestamp
  "favorites": [ObjectId]       // Array of publication IDs
}
```

**Indexes:**
- Unique index on `username`
- Unique index on `email`

---

## Permission System

### Role-Based Access Control

**Viewer (default role):**
- Browse publications
- Search and filter
- View PDFs
- Add publications (books)
- Add authors
- Manage favorites

**Editor:**
- All viewer permissions
- Edit publications
- Delete publications
- Edit authors
- Delete authors
- View publication/author management lists

**Admin:**
- All editor permissions
- Access admin dashboard
- Manage users
- View system statistics

---

## File Upload Structure

```
static/uploads/
├── pdfs/                 # PDF documents
│   └── [secure_filename].pdf
├── covers/               # Publication cover images
│   └── [secure_filename].png|jpg|jpeg
└── authors/              # Author profile pictures
    └── [secure_filename].png|jpg|jpeg
```

**Upload Processing:**
1. Validate file extension (allowed: pdf, png, jpg, jpeg, gif)
2. Secure filename using `werkzeug.utils.secure_filename()`
3. Save to appropriate subfolder
4. Store filename in MongoDB (not full path)

---

## Project Structure

```
WRDC_lib/
├── app.py                    # Main Flask application (refactored)
├── config.py                 # Configuration management
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
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
├── templates/               # Jinja2 templates
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

## Session Management

**Library:** Flask sessions (server-side storage)  
**Secret Key:** Loaded from `.env` file (SECRET_KEY)  
**Session Data:**
- `user_id` - User ObjectId as string
- `username` - Username string
- `role` - User role ("admin", "editor", "viewer")

**Authentication Flow:**
1. User submits username/password at `/auth/login`
2. Password verified using bcrypt
3. Set session: `user_id`, `username`, `role`
4. Redirect based on role

**Protected Routes:**
- `@user_required` - Any logged-in user
- `@editor_required` - Editor or admin
- `@admin_required` - Admin only

---

## Query Patterns

### Enhanced Search
```python
query = {}
if search:
    query['$or'] = [
        {'title': {'$regex': search, '$options': 'i'}},
        {'author': {'$regex': search, '$options': 'i'}},
        {'category': {'$regex': search, '$options': 'i'}}
    ]
# Combine with filters using $and if needed
```

### Cached Aggregations
```python
# Authors list (cached 5 minutes)
authors = cache.get('authors_list')
if authors is None:
    authors = list(db.publications.aggregate([...]))
    cache.set('authors_list', authors, timeout=300)
```

---

## Custom Filters

### format_date
**Usage:** `{{ publication.publish_date | format_date }}`  
**Input:** `YYYY-MM-DD` string  
**Output:** `Month DD, YYYY` (e.g., "January 15, 2024")

```python
@app.template_filter('format_date')
def format_date(value, format='%B %d, %Y'):
    try:
        return datetime.strptime(value, '%Y-%m-%d').strftime(format)
    except:
        return value
```

---

## Static Asset Dependencies

### CDN Resources
- Bootstrap 4.5.2 CSS: `https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css`
- Chart.js: `https://cdn.jsdelivr.net/npm/chart.js`
- Kuwait MEW logos: `https://www.mew.gov.kw/images/...`

### Local Assets
- Uploaded files served via Flask's `static` blueprint
- URL generation: `url_for('static', filename='uploads/pdfs/...')`
