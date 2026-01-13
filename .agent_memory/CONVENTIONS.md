# CONVENTIONS.md

**Last Updated:** 2026-01-13

---

## Code Conventions

### Flask Route Patterns

**Standard Route Structure:**
```python
@app.route('/path')
def function_name():
    # Query database
    # Process data
    return render_template('template.html', variables=data)
```

**Protected Routes:**
```python
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Admin logic here
```

**Form Handling:**
```python
@app.route('/add_something', methods=['POST'])
def add_something():
    # 1. Check authentication
    # 2. Get form data
    # 3. Validate files
    # 4. Process and save
    # 5. Redirect
    return redirect(url_for('admin'))
```

---

## Naming Conventions

### Python
- **Functions:** `snake_case` (e.g., `add_publication`, `view_pdf`)
- **Variables:** `snake_case` (e.g., `pdf_filename`, `author_name`)
- **Config Keys:** `UPPER_SNAKE_CASE` (e.g., `UPLOAD_FOLDER`, `ALLOWED_EXTENSIONS`)

### Templates
- **Files:** `lowercase.html` (e.g., `index.html`, `author_info.html`)
- **Multi-word files:** `underscore_separated.html` (e.g., `author_info.html`)

### Database
- **Collections:** `lowercase` (e.g., `publications`, `authors`)
- **Fields:** `snake_case` (e.g., `pdf_filename`, `publish_date`)

---

## File Upload Pattern

**Standard Process:**
```python
# 1. Get file from request
file = request.files['field_name']

# 2. Check if file exists
if file.filename == '':
    flash('No selected file')
    return redirect(url_for('admin'))

# 3. Validate file type
if file and allowed_file(file.filename):
    # 4. Secure the filename
    filename = secure_filename(file.filename)
    
    # 5. Save to appropriate folder
    file.save(os.path.join(app.config['FOLDER_NAME'], filename))
    
    # 6. Store filename (not path) in database
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
    <div class="container">
        <!-- Page content -->
    </div>
    <script>
        /* Page-specific JavaScript */
    </script>
</body>
</html>
```

---

## Data Aggregation Pattern

**MongoDB Aggregation Pipeline:**
```python
# Group and count pattern
results = list(mongo.db.collection.aggregate([
    {"$group": {"_id": "$field_name", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
]))

# Filter and group pattern
results = list(mongo.db.collection.aggregate([
    {"$match": {"field": "value"}},
    {"$group": {"_id": "$grouping_field", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
]))
```

---

## URL Generation Pattern

**Static Files:**
```python
url_for('static', filename='uploads/subfolder/' + filename)
```

**Routes:**
```python
url_for('route_function_name', parameter=value)
```

**In Templates:**
```jinja
{{ url_for('view_pdf', publication_id=publication._id) }}
{{ url_for('static', filename='uploads/covers/' + publication.cover_filename) }}
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
publish_date = datetime.strptime(date_input, '%Y-%m-%d').date().isoformat()
```

**Display:** Use custom filter
```jinja
{{ publication.publish_date | format_date }}
```

---

## Directory Creation Pattern

**Ensure directories exist:**
```python
os.makedirs(app.config['FOLDER_NAME'], exist_ok=True)
```

---

## Session Check Pattern

**Authentication Check:**
```python
if not session.get('logged_in'):
    return redirect(url_for('login'))
```

**Login:**
```python
session['logged_in'] = True
```

**Logout:**
```python
session.pop('logged_in', None)
```
