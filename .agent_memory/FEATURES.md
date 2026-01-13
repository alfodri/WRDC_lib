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
- **Text Search:** Search by publication title (case-insensitive regex)
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
- **Publications by Author:** List with counts
- **Publications by Category:** List with counts
- **Chart:** Bar chart showing number of publications per year

**Author Profile Page:**
- Bar chart showing author's publications per year
- Color scheme: Teal (rgba(75, 192, 192))

**Chart.js Configuration:**
- Y-axis: Number of Publications (starts at 0)
- X-axis: Year
- Interactive hover tooltips

---

### 5. Guidelines Page

**Location:** `/guideline`

**Content:**
- Introduction for new authors
- Step-by-step submission process:
  1. Register as an author
  2. Prepare publication (PDF + cover)
  3. Submit via admin panel
- Required author skills
- Contact information

---

## Admin Features

### Admin Panel Access

**Location:** `/admin`  
**Authentication:** Password-based login (`/login`)  
**Credentials:** Password = `admin` (hardcoded)

**Session Management:**
- Login sets session flag
- All admin routes check authentication
- Logout clears session

---

### Add Publication

**Form Fields:**
- Publication Title (text, required)
- Author (text input with datalist autocomplete from existing authors)
- Category (text, required)
- Publish Date (date picker, required)
- PDF File (file upload, .pdf only, required)
- Cover Image (file upload, images only, required)

**Processing:**
1. Validate file types
2. Secure filenames
3. Save files to `static/uploads/pdfs/` and `static/uploads/covers/`
4. Convert date to ISO string format
5. Insert document into `publications` collection
6. Redirect back to admin panel

**Validation:**
- Required fields enforced
- File extension checking
- Empty file prevention

---

### Add Author

**Form Fields:**
- Author Name (text, required)
- Author Picture (file upload, images only, required)
- Profile (textarea, required)
- Education (textarea, required)
- Experience and Internships (textarea, required)
- Technical Skills (textarea, required)

**Processing:**
1. Validate image file
2. Secure filename
3. Save to `static/uploads/authors/`
4. Insert document into `authors` collection
5. Redirect back to admin panel

**Integration:**
- New authors immediately appear in publication form datalist
- Author names link publications to profiles

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

### Navigation
- Navbar with quick links:
  - Admin Login
  - Authors
  - Guidelines
- Footer with designer/manager credits

### User Feedback
- Flash messages for login errors
- Form validation messages
- Success/error alerts

---

## Data Display Patterns

### Publication Card
```
[Cover Image]
Title by Author
Category
Publish Date (formatted)
[View PDF Button]
```

### Author Card
```
[Profile Picture]
Author Name
```

### Latest Publications Sidebar
```
[Thumbnail] Title
            Publish Date
```

---

## Special Features

### Date Formatting
- Input: `YYYY-MM-DD`
- Display: `Month DD, YYYY` (e.g., "January 15, 2024")
- Custom Jinja2 filter: `format_date`

### Pagination
- Configurable per-page count (default: 9)
- Previous/Next buttons
- Page number links
- Disabled state for boundary pages
- Preserves filter parameters across pages

### Autocomplete
- Author name input has datalist with existing authors
- Prevents duplicate author names
- Easy selection for admin

---

## Error Handling

- Missing publication: 404 error with message
- Missing PDF file: Error message display
- Unauthorized admin access: Redirect to login
- Invalid file uploads: Flash message
- Empty file selection: Flash message "No selected file"
