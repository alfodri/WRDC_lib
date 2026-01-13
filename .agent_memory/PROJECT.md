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
- Enable admin management of publications and author data

---

## Tech Stack

### Backend
- **Framework:** Flask 2.x (Python web framework)
- **Database:** MongoDB (local instance at `mongodb://localhost:27017/library`)
- **Extensions:** Flask-PyMongo (MongoDB integration)
- **File Handling:** Werkzeug (secure file uploads)

### Frontend
- **UI Framework:** Bootstrap 4.5.2
- **Visualization:** Chart.js (publication statistics)
- **PDF Rendering:** Native browser `<embed>` tag

### Dependencies
```
Flask
Flask-PyMongo
Werkzeug
pymongo
```

---

## Database

**MongoDB Database:** `library`

**Collections:**
1. `publications` - Technical reports and documents
2. `authors` - Author profiles and information

---

## File Structure

```
WRDC_lib/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── static/uploads/           # Uploaded files storage
│   ├── pdfs/                 # PDF documents
│   ├── covers/               # Publication cover images
│   └── authors/              # Author profile pictures
├── templates/                # Jinja2 HTML templates
│   ├── index.html            # Homepage with publication grid
│   ├── admin.html            # Admin panel for adding content
│   ├── author.html           # Authors listing page
│   ├── author_info.html      # Individual author profile
│   ├── view_pdf.html         # PDF viewer page
│   ├── guideline.html        # Author submission guidelines
│   └── login.html            # Admin login
└── .agent_memory/            # AI agent context files
```

---

## How to Run

### Prerequisites
1. MongoDB installed and running locally
2. Python 3.7+ installed

### Installation Steps
```bash
# Install dependencies
pip install -r requirements.txt

# Ensure MongoDB is running
# Default connection: mongodb://localhost:27017/library

# Run the application
python app.py
```

### Access Points
- **Application:** http://0.0.0.0:5001
- **Admin Login:** http://0.0.0.0:5001/login (password: `admin`)

---

## Key Features

1. **Publication Management** - Upload, store, and display technical PDFs
2. **Advanced Search** - Filter by title, author, category, publish date
3. **Author Profiles** - Detailed author information with publication history
4. **Analytics** - Publication statistics with Chart.js visualizations
5. **PDF Viewer** - In-browser PDF reading experience
6. **Admin Panel** - Secure content management system

---

## Configuration

### Upload Settings
- **Upload Folder:** `static/uploads/`
- **Allowed Extensions:** pdf, png, jpg, jpeg, gif
- **MongoDB URI:** `mongodb://localhost:27017/library`
- **Secret Key:** `supersecretkey` (⚠️ Change in production)

### Security Notes
- Simple password authentication (hardcoded: `admin`)
- Flask sessions for login state
- File upload validation with secure_filename()

---

## Environment

- **Host:** 0.0.0.0 (accessible from network)
- **Port:** 5001
- **Debug Mode:** Enabled (disable in production)
