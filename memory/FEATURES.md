# FEATURES.md

**Last Updated:** 2026-01-13

---

## User-Facing Features

### 1. Publication Browsing & Search

**Location:** Homepage (`/`)

**Capabilities:**
- Grid view of publications (3 columns, paginated)
- Each card shows: cover image, title, author, category, publish date
- Click to view full PDF
- 9 publications per page with pagination controls

**Search & Filter Options:**
- **Text Search:** Enhanced search across title, author, and category (case-insensitive regex)
- **Author Filter:** Dropdown with publication counts per author
- **Category Filter:** Dropdown with publication counts per category
- **Publish Date Filter:** Dropdown with all available dates
- **Sort Options:** 
  - By Title (default)
  - By Author
  - By Category
  - By Publish Date
- **Reset Filter:** Button to clear all filters

---

### 2. PDF Viewer

**Location:** `/view_pdf/<publication_id>`

**Features:**
- Full-screen embedded PDF viewer
- Publication metadata display:
  - Title
  - Author with profile picture (if available)
  - Publish date (formatted)
- Automatic view count increment
- Native browser PDF controls (zoom, download, print)
- "Back to Library" button

---

### 3. Author Profiles

**Author Listing** (`/authors`):
- Grid of author cards with profile pictures
- Click to view detailed profile

**Author Detail Page** (`/author/<author_id>`):
- Profile picture
- Four information sections:
  - Profile (bio)
  - Education
  - Experience and Internships
  - Technical Skills
- Latest 5 publications by author
- Chart.js bar chart: Publications per year
- "Back to Authors" button

---

### 4. Analytics & Visualizations

**Homepage Sidebar:**
- **Latest Publications:** 5 most recent publications with thumbnails
- **Publications by Author:** List with counts (cached)
- **Publications by Category:** List with counts (cached)
- **Chart:** Bar chart showing number of publications per year (cached)

**Author Profile Page:**
- Bar chart showing author's publications per year
- Color scheme: Teal (rgba(75, 192, 192))

**Chart.js Configuration:**
- Y-axis: Number of Publications (starts at 0)
- X-axis: Year
- Interactive hover tooltips

---

### 5. User Authentication & Registration

**Registration** (`/auth/register`):
- Username (unique)
- Email (unique)
- Password (minimum 6 characters)
- Password confirmation
- Automatic role assignment: "viewer"

**Login** (`/auth/login`):
- Username/password authentication
- Secure password verification with bcrypt
- Session creation with user_id, username, role
- Redirect to homepage after login

**Profile & Favorites:**
- User profile page (shows username and role)
- Favorites system (add/remove publications)
- Last login tracking

---

### 6. Content Addition (All Logged-In Users)

**Location:** `/admin/add`

**Features:**
- **Add Publication Form:**
  - Publication Title
  - Author (with autocomplete from existing authors)
  - Category
  - Publish Date
  - PDF File upload
  - Cover Image upload
- **Add Author Form:**
  - Author Name
  - Author Picture
  - Profile
  - Education
  - Experience and Internships
  - Technical Skills

**Access:** All logged-in users (any role) can add publications and authors

---

## Admin Features

### Admin Dashboard

**Location:** `/admin/dashboard` (admin only)

**Statistics Display:**
- Total Publications
- Total Authors
- Total Users
- Recent Publications (5 most recent)
- Recent Authors (5 most recent)

---

### Publication Management (Editor/Admin)

**List Publications** (`/admin/publications`):
- Table view of all publications
- Pagination (20 per page)
- Edit and Delete buttons for each publication

**Edit Publication** (`/admin/edit_publication/<id>`):
- Edit all publication fields
- Optional file replacement (PDF and cover)
- If files not provided, keeps existing files

**Delete Publication** (`/admin/delete_publication/<id>`):
- Confirmation dialog
- Deletes publication document
- Removes associated PDF and cover files from filesystem

---

### Author Management (Editor/Admin)

**List Authors** (`/admin/authors`):
- Table view of all authors
- Author images displayed
- Edit and Delete buttons

**Edit Author** (`/admin/edit_author/<id>`):
- Edit all author fields
- Optional image replacement
- If image not provided, keeps existing image

**Delete Author** (`/admin/delete_author/<id>`):
- Confirmation dialog
- Deletes author document
- Removes author image from filesystem

---

### User Management (Admin Only)

**Location:** `/admin/users`

**Features:**
- View all registered users
- Display username, email, role
- Role badges (admin=red, editor=yellow, viewer=blue)
- Account creation date

---

## REST API Features

**Base URL:** `/api/v1/`

### Authentication
- JWT token-based authentication
- Token obtained via `POST /api/v1/auth/login`
- Token included in `Authorization: Bearer <token>` header
- Token expires after 7 days

### Endpoints

**Publications:**
- `GET /api/v1/publications` - List publications (paginated, filterable)
- `GET /api/v1/publications/<id>` - Get single publication
- `POST /api/v1/publications` - Create publication (auth: editor/admin)
- `PUT /api/v1/publications/<id>` - Update publication (auth: editor/admin)
- `DELETE /api/v1/publications/<id>` - Delete publication (auth: editor/admin)

**Authors:**
- `GET /api/v1/authors` - List all authors
- `GET /api/v1/authors/<id>` - Get single author

**Categories:**
- `GET /api/v1/categories` - List all categories with counts

**Search:**
- `GET /api/v1/search?q=<query>` - Search publications

**Statistics:**
- `GET /api/v1/stats` - Get library statistics

**Response Format:**
```json
{
  "status": "success",
  "data": { ... },
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8
  }
}
```

---

## UI/UX Features

### Responsive Design
- Bootstrap 4 responsive grid system
- Mobile-friendly navigation
- Adaptive image sizing

### Visual Elements
- Kuwait MEW official logos in header
- Professional color scheme
- Card-based layout for content
- Hover effects on cards
- Role-based button visibility

### Navigation
- Navbar with quick links:
  - "Add Book" button (visible to all logged-in users)
  - Login/Logout buttons
  - Authors link
  - Guidelines link
  - Admin Panel link (admin/editor only)
- Footer with designer/manager credits

### User Feedback
- Flash messages for all actions
- Form validation messages
- Success/error alerts
- Confirmation dialogs for destructive actions

---

## Permission Summary

| Action | Viewer | Editor | Admin |
|--------|--------|--------|-------|
| Browse publications | ✓ | ✓ | ✓ |
| Search & filter | ✓ | ✓ | ✓ |
| View PDFs | ✓ | ✓ | ✓ |
| Add publications | ✓ | ✓ | ✓ |
| Add authors | ✓ | ✓ | ✓ |
| Edit publications | ✗ | ✓ | ✓ |
| Delete publications | ✗ | ✓ | ✓ |
| Edit authors | ✗ | ✓ | ✓ |
| Delete authors | ✗ | ✓ | ✓ |
| View admin dashboard | ✗ | ✗ | ✓ |
| Manage users | ✗ | ✗ | ✓ |

---

## Error Handling

- Missing publication: Flash message, redirect to index
- Missing PDF file: Flash message, redirect to index
- Unauthorized access: Flash message, redirect to login or index
- Invalid file uploads: Flash message with error details
- Empty file selection: Flash message "No selected file"
- Database errors: Graceful error handling with user-friendly messages

---

## Performance Features

- **Caching:** Flask-Caching for aggregation queries (5-minute timeout)
- **Database Indexes:** 
  - Text index for full-text search
  - Indexes on frequently queried fields
- **Lazy Loading:** Images load on demand
- **Optimized Queries:** Efficient MongoDB queries with proper indexing
