# CONVENTIONS.md

**Last Updated:** 2026-01-13

---

## Code Conventions

### Flask Route Patterns (Blueprints)

**Blueprint Route Structure:**
```python
from flask import Blueprint
from utils.auth import user_required

bp = Blueprint('name', __name__)

@bp.route('/path')
@user_required
def function_name():
    from utils.db import get_db
    db = get_db()
    # Query database
    # Process data
    return render_template('template.html', variables=data)
```

**Route Registration:**
```python
# In app.py
from routes import main_bp, auth_bp, admin_bp, api_bp
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)
```

**Protected Routes with Decorators:**
```python
from utils.auth import user_required, editor_required, admin_required

@admin_bp.route('/admin/dashboard')
@admin_required
def dashboard():
    # Only admins can access
    pass

@admin_bp.route('/admin/add')
@user_required
def add_content():
    # Any logged-in user can access
    pass
```

**Form Handling:**
```python
@admin_bp.route('/add_publication', methods=['POST'])
@user_required
def add_publication():
    # 1. Authentication checked by decorator
    # 2. Get form data
    title = request.form.get('title')
    pdf = request.files.get('pdf')
    
    # 3. Validate files
    if not pdf or pdf.filename == '':
        flash('Please select a file')
        return redirect(url_for('admin.add_content_page'))
    
    # 4. Process and save
    # 5. Redirect based on user role
    user = get_current_user(db)
    if user.get('role') in ['admin', 'editor']:
        return redirect(url_for('admin.publications'))
    return redirect(url_for('admin.add_content_page'))
```

---

## Naming Conventions

### Python
- **Functions:** `snake_case` (e.g., `add_publication`, `view_pdf`)
- **Variables:** `snake_case` (e.g., `pdf_filename`, `author_name`)
- **Config Keys:** `UPPER_SNAKE_CASE` (e.g., `UPLOAD_FOLDER`, `ALLOWED_EXTENSIONS`)
- **Classes:** `PascalCase` (e.g., `User`, `Publication`, `Author`)
- **Blueprints:** `snake_case` with `_bp` suffix (e.g., `main_bp`, `auth_bp`)

### Templates
- **Files:** `lowercase.html` (e.g., `index.html`, `author_info.html`)
- **Multi-word files:** `underscore_separated.html` (e.g., `author_info.html`)
- **Folders:** `lowercase` (e.g., `auth/`, `admin/`)

### Database
- **Collections:** `lowercase` (e.g., `publications`, `authors`, `users`)
- **Fields:** `snake_case` (e.g., `pdf_filename`, `publish_date`, `password_hash`)

### Routes
- **Blueprint names:** `main`, `auth`, `admin`, `api`
- **Route functions:** `snake_case` matching route purpose
- **URL patterns:** Use blueprint prefix (e.g., `/auth/login`, `/admin/dashboard`)

---

## Authentication Patterns

### User Authentication
```python
from models.user import User
from utils.db import get_db
from utils.auth import get_current_user

# Authenticate user
db = get_db()
user = User.authenticate(db, username, password)
if user:
    session['user_id'] = str(user['_id'])
    session['username'] = user['username']
    session['role'] = user['role']
```

### Password Hashing
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Create user with hashed password
password_hash = generate_password_hash(password)
# Store password_hash in database

# Verify password
if check_password_hash(user['password_hash'], password):
    # Password correct
```

### Permission Decorators
```python
from utils.auth import user_required, editor_required, admin_required

@user_required      # Any logged-in user
@editor_required    # Editor or admin
@admin_required     # Admin only
```

---

## File Upload Pattern

**Standard Process:**
```python
from werkzeug.utils import secure_filename
from config import Config

# 1. Get file from request
file = request.files.get('field_name')

# 2. Check if file exists
if not file or file.filename == '':
    flash('No selected file')
    return redirect(url_for('admin.add_content_page'))

# 3. Validate file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

if file and allowed_file(file.filename):
    # 4. Secure the filename
    filename = secure_filename(file.filename)
    
    # 5. Ensure directory exists
    os.makedirs(Config.PDF_FOLDER, exist_ok=True)
    
    # 6. Save to appropriate folder
    file.save(os.path.join(Config.PDF_FOLDER, filename))
    
    # 7. Store filename (not path) in database
    Publication.create(db, title, author, category, date, filename, cover_filename)
```

---

## Model Pattern

**Model Class Structure:**
```python
class Publication:
    """Publication model"""
    
    @staticmethod
    def create(db, title, author, category, publish_date, pdf_filename, cover_filename):
        """Create a new publication"""
        publication = {
            'title': title,
            'author': author,
            # ... other fields
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = db.publications.insert_one(publication)
        return result.inserted_id
    
    @staticmethod
    def get_by_id(db, publication_id):
        """Get publication by ID"""
        return db.publications.find_one({'_id': ObjectId(publication_id)})
    
    @staticmethod
    def update(db, publication_id, **kwargs):
        """Update publication fields"""
        kwargs['updated_at'] = datetime.utcnow()
        db.publications.update_one(
            {'_id': ObjectId(publication_id)},
            {'$set': kwargs}
        )
```

---

## Template Structure Pattern

**Standard HTML Template:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        /* Page-specific CSS */
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('main.index') }}">Library</a>
            {% if session.get('user_id') %}
            <span class="navbar-text">Welcome, {{ session.get('username') }}</span>
            {% endif %}
        </div>
    </nav>
    <div class="container">
        <!-- Page content -->
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="alert alert-info">
                    {% for message in messages %}
                        <p>{{ message }}</p>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
    </div>
</body>
</html>
```

---

## URL Generation Pattern (Blueprints)

**Static Files:**
```python
url_for('static', filename='uploads/subfolder/' + filename)
```

**Blueprint Routes:**
```python
# In Python
url_for('main.index')
url_for('auth.login')
url_for('admin.dashboard')
url_for('admin.edit_publication', publication_id=pub_id)
```

**In Templates:**
```jinja
{{ url_for('main.view_pdf', publication_id=publication._id) }}
{{ url_for('admin.add_content_page') }}
{{ url_for('static', filename='uploads/covers/' + publication.cover_filename) }}
```

---

## Data Aggregation Pattern

**MongoDB Aggregation Pipeline:**
```python
from utils.db import get_db

db = get_db()

# Group and count pattern
results = list(db.publications.aggregate([
    {"$group": {"_id": "$author", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
]))

# Filter and group pattern
results = list(db.publications.aggregate([
    {"$match": {"author": author_name}},
    {"$group": {"_id": "$category", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
]))
```

---

## Caching Pattern

**Using Flask-Caching:**
```python
from flask import current_app

cache = current_app.cache

# Get cached data
data = cache.get('cache_key')
if data is None:
    # Compute data
    data = expensive_operation()
    # Cache for 5 minutes
    cache.set('cache_key', data, timeout=300)
```

---

## Chart.js Pattern

**JavaScript Implementation:**
```javascript
document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('chartId').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: {{ years|tojson }},  // From Flask
            datasets: [{
                label: 'Label Text',
                data: {{ counts|tojson }},  // From Flask
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});
```

---

## Bootstrap Grid Pattern

**Card Grid (3 columns):**
```html
<div class="row">
    {% for item in items %}
    <div class="col-md-4">
        <div class="card mb-4">
            <!-- Card content -->
        </div>
    </div>
    {% endfor %}
</div>
```

---

## Date Handling Pattern

**Storage:** Always store as ISO string (`YYYY-MM-DD`)
```python
from datetime import datetime
publish_date = datetime.strptime(date_input, '%Y-%m-%d').date().isoformat()
```

**Display:** Use custom filter
```jinja
{{ publication.publish_date | format_date }}
```

**Filter Implementation:**
```python
@app.template_filter('format_date')
def format_date(value, format='%B %d, %Y'):
    try:
        return datetime.strptime(value, '%Y-%m-%d').strftime(format)
    except:
        return value
```

---

## Configuration Pattern

**Using config.py:**
```python
from config import Config

# Access configuration
app.config.from_object(Config)
pdf_folder = Config.PDF_FOLDER
allowed_extensions = Config.ALLOWED_EXTENSIONS
```

**Environment Variables:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
secret_key = os.environ.get('SECRET_KEY') or 'default-value'
```

---

## Session Management Pattern

**New Session Pattern:**
```python
# Login
session['user_id'] = str(user['_id'])
session['username'] = user['username']
session['role'] = user['role']

# Check session
if 'user_id' not in session:
    return redirect(url_for('auth.login'))

# Get current user
from utils.auth import get_current_user
db = get_db()
user = get_current_user(db)

# Logout
session.clear()
```

---

## Error Handling Pattern

**Flash Messages:**
```python
from flask import flash

# Success
flash('Publication added successfully!')

# Error
flash('Publication not found')
flash('You do not have permission to access this page')

# In template
{% with messages = get_flashed_messages() %}
    {% if messages %}
        <div class="alert alert-info">
            {% for message in messages %}
                <p>{{ message }}</p>
            {% endfor %}
        </div>
    {% endif %}
{% endwith %}
```

**Redirects:**
```python
from flask import redirect, url_for

# Simple redirect
return redirect(url_for('main.index'))

# Redirect with flash
flash('Error message')
return redirect(url_for('admin.add_content_page'))
```
