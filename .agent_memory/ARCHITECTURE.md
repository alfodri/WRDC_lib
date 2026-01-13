# ARCHITECTURE.md

**Last Updated:** 2026-01-13

---

## Application Architecture

**Type:** Monolithic Flask Web Application  
**Pattern:** MVC (Model-View-Controller) via Flask + Jinja2  
**Database:** Document-oriented (MongoDB)

---

## Flask Routes

### Public Routes

| Route | Method | Template | Purpose |
|-------|--------|----------|---------|
| `/` | GET | `index.html` | Homepage with publication grid, search, filters, pagination |
| `/authors` | GET | `author.html` | List all authors with profile pictures |
| `/author/<author_id>` | GET | `author_info.html` | Individual author profile with publications and stats |
| `/view_pdf/<publication_id>` | GET | `view_pdf.html` | PDF viewer with publication metadata |
| `/guideline` | GET | `guideline.html` | Author submission guidelines |
| `/login` | GET, POST | `login.html` | Admin authentication |
| `/logout` | GET | Redirect | Clear session and logout |

### Admin Routes (Requires Login)

| Route | Method | Template | Purpose |
|-------|--------|----------|---------|
| `/admin` | GET, POST | `admin.html` | Admin dashboard with forms |
| `/add_publication` | POST | Redirect | Upload new publication with PDF and cover |
| `/add_author` | POST | Redirect | Create new author profile |

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
  "cover_filename": String      // Filename in static/uploads/covers/
}
```

**Indexes:**
- Text search on `title`
- Aggregation on `author`, `category`, `publish_date`

### Collection: `authors`

```javascript
{
  "_id": ObjectId,
  "name": String,               // Full name (unique identifier)
  "profile": String,            // Short bio/profile text
  "education": String,          // Educational background
  "experience": String,         // Work experience and internships
  "skills": String,             // Technical skills
  "image": String               // Filename in static/uploads/authors/
}
```

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

## Template-to-Route Mapping

### index.html
- **Route:** `/`
- **Context Variables:**
  - `publications` - Paginated publication list
  - `authors` - Aggregated author list with counts
  - `categories` - Aggregated category list with counts
  - `publish_dates` - Distinct publish dates
  - `latest_publications` - 5 most recent publications
  - `years` - Chart.js data (publication years)
  - `counts` - Chart.js data (publications per year)
  - `page`, `total_pages` - Pagination data

### admin.html
- **Route:** `/admin`
- **Context Variables:**
  - `authors` - All authors for datalist autocomplete
- **Forms:**
  - Add Publication Form (multipart/form-data)
  - Add Author Form (multipart/form-data)

### author.html
- **Route:** `/authors`
- **Context Variables:**
  - `authors` - All authors with images

### author_info.html
- **Route:** `/author/<author_id>`
- **Context Variables:**
  - `author` - Single author document
  - `latest_publications` - Author's 5 recent publications
  - `years` - Chart.js data
  - `counts` - Chart.js data

### view_pdf.html
- **Route:** `/view_pdf/<publication_id>`
- **Context Variables:**
  - `publication` - Single publication document
  - `pdf_url` - Flask url_for() generated PDF path
  - `author_image` - Author's profile picture (if exists)

### guideline.html
- **Route:** `/guideline`
- **Context Variables:** None (static content)

### login.html
- **Route:** `/login`
- **Context Variables:** Flash messages on error

---

## Query Patterns

### Homepage Filtering
```python
query = {}
if search:
    query['title'] = {'$regex': search, '$options': 'i'}
if author:
    query['author'] = author
if category:
    query['category'] = category
if publish_date:
    query['publish_date'] = publish_date

publications = mongo.db.publications.find(query).sort(sort).skip((page - 1) * per_page).limit(per_page)
```

### Author Statistics
```python
# Publications per author
mongo.db.publications.aggregate([
    {"$group": {"_id": "$author", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
])

# Publications per year (for author)
mongo.db.publications.aggregate([
    {"$match": {"author": author['name']}},
    {"$group": {"_id": {"$year": {"$dateFromString": {"dateString": "$publish_date"}}}, "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
])
```

---

## Session Management

**Library:** Flask sessions (server-side storage)  
**Secret Key:** `supersecretkey`  
**Session Data:**
- `logged_in` - Boolean flag for admin authentication

**Authentication Flow:**
1. User submits password at `/login`
2. Compare with hardcoded password (`admin`)
3. Set `session['logged_in'] = True`
4. Redirect to `/admin`

**Protected Routes:**
- Check `session.get('logged_in')` before rendering admin pages
- Redirect to `/login` if not authenticated

---

## Custom Filters

### format_date
**Usage:** `{{ publication.publish_date | format_date }}`  
**Input:** `YYYY-MM-DD` string  
**Output:** `Month DD, YYYY` (e.g., "January 15, 2024")

```python
@app.template_filter('format_date')
def format_date(value, format='%B %d, %Y'):
    return datetime.strptime(value, '%Y-%m-%d').strftime(format)
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
