# CONTEXT.md

**Last Updated:** 2026-01-13

> **Instructions for AI Agents:**  
> This is a living document. Update this file at the end of each conversation session.  
> Add notes about changes made, issues discovered, user preferences, and next steps.

---

## Session History

### Session: 2026-01-13 (GitHub Repository Setup)
**Agent:** Claude  
**Changes Made:**
- Initialized Git repository
- Created comprehensive `.gitignore` file
- Excluded uploaded files (PDFs, covers, author images) from repository
- Excluded sensitive files (.env, venv, cache files)
- Pushed project to GitHub: `git@github.com:alfodri/WRDC_lib.git`
- Committed 39 files with all source code and documentation
- Set up main branch tracking

**Repository Details:**
- **URL:** git@github.com:alfodri/WRDC_lib.git
- **Branch:** main
- **Files Committed:** 39 files, 4,912+ lines
- **Excluded:** static/uploads/, .env, venv/, __pycache__/

**Notes:**
- Repository is ready for collaboration
- All important source files included
- Uploaded books/publications excluded (as requested)
- Sensitive data (.env) excluded for security
- Documentation fully included

---

### Session: 2026-01-13 (Major Enhancement)
**Agent:** Claude  
**Changes Made:**
- **Phase 1 - Security:** Implemented secure authentication with bcrypt, environment variables (.env), CSRF protection foundation
- **Phase 2 - User System:** Added user registration, role-based access (admin/editor/viewer), favorites system
- **Phase 3 - CRUD Operations:** Added edit/delete functionality for publications and authors with file cleanup
- **Phase 5 - Enhanced Search:** Implemented MongoDB text search with regex fallback
- **Phase 6 - Performance:** Added Flask-Caching, database indexes, optimized queries
- **Phase 7 - REST API:** Built complete REST API with JWT authentication
- **Permission Update:** Changed system so ALL logged-in users can add books/publications (not just editors/admins)

**New Files Created:**
- `config.py` - Configuration management
- `.env` - Environment variables (SECRET_KEY, MONGO_URI, etc.) - NOT in git
- `.gitignore` - Git ignore rules (excludes uploads, .env, venv)
- `models/` - User, Publication, Author models
- `routes/` - Modular route blueprints (main, auth, admin, api)
- `utils/` - Authentication and database utilities
- `templates/auth/register.html` - Registration form
- `templates/admin/` - Admin dashboard and management pages
- `SETUP.md` - Setup instructions
- `IMPLEMENTATION_SUMMARY.md` - Detailed implementation summary

**Key Changes:**
- Refactored monolithic `app.py` into modular structure with blueprints
- Replaced hardcoded password with bcrypt-hashed passwords
- Added user registration system
- Created admin dashboard with statistics
- Implemented full CRUD for publications and authors
- Added REST API with JWT authentication
- Implemented caching for performance
- Created permission system: all users can add, only editors/admins can edit/delete

**Default Admin Account:**
- Username: `admin`
- Password: `admin123` (⚠️ Change in production!)

**Notes:**
- User requested that all logged-in users should be able to add books
- Permission system updated: viewers can add, only editors/admins can edit/delete
- MongoDB text index created for enhanced search
- Caching implemented for aggregation queries (5-minute timeout)
- All existing functionality preserved and enhanced

---

### Session: 2026-01-13 (Initial Setup)
**Agent:** Initial setup  
**Changes Made:**
- Created `.agent_memory/` folder structure
- Generated initial documentation files

**Notes:**
- Project is a Flask-based digital library for WRDC (Water Resources Development Center)
- Focus is on water treatment/desalination technical documentation
- Currently serving historical reports from 1972-1980s

---

## Known TODOs / Future Enhancements

### High Priority
- [x] ~~Implement secure authentication (bcrypt, environment variables)~~ ✅ DONE
- [x] ~~Add edit functionality for publications and authors~~ ✅ DONE
- [x] ~~Add delete functionality with confirmation dialogs~~ ✅ DONE
- [ ] Implement proper error pages (404, 500)
- [ ] Add password change functionality for users
- [ ] Add email verification for registration

### Medium Priority
- [ ] Add search functionality to authors page
- [ ] Implement pagination for authors listing
- [ ] Add thumbnail generation for PDFs (currently using uploaded covers)
- [ ] Add download counters for publications (view counter implemented)
- [x] ~~Implement user roles (admin, editor, viewer)~~ ✅ DONE
- [ ] Add user profile editing page
- [ ] Implement favorites UI (currently backend only)

### Low Priority
- [ ] Add export functionality (CSV/Excel of publications)
- [ ] Implement advanced search (full-text search across PDFs)
- [ ] Add tags/keywords to publications
- [x] ~~Implement favorites/bookmarks for users~~ ✅ DONE (backend)
- [ ] Add comments/notes system for publications
- [ ] Implement UI redesign with Tailwind CSS (Phase 4 - optional)

### Infrastructure
- [ ] Add proper logging system
- [ ] Implement backup system for MongoDB
- [ ] Add file size limits for uploads
- [ ] Implement image compression for uploads
- [x] ~~Add configuration file (config.py) instead of hardcoded values~~ ✅ DONE

---

## User Preferences & Design Decisions

### Technology Choices
- **Frontend:** Bootstrap 4.5.2 (existing in project, kept for compatibility)
- **Charts:** Chart.js (existing in project)
- **Database:** MongoDB (document-oriented, flexible schema)
- **No ORM:** Direct PyMongo usage for simplicity
- **Caching:** Flask-Caching with simple backend (can upgrade to Redis)

### Design Patterns
- Modular Flask application with blueprints
- Model classes for data operations
- Utility functions for common operations
- Environment-based configuration
- File-based storage for uploads (not database)
- Filename-only storage in database (not full paths)
- ISO date strings for compatibility

### UI/UX Decisions
- Kuwait MEW branding (logos, colors)
- Card-based layout for visual appeal
- Embedded PDF viewer (no download required)
- Sidebar analytics on homepage
- Author profiles include publications and statistics
- "Add Book" button visible to all logged-in users
- Role-based UI elements (admin panel visible to admins/editors only)

### Permission Model
- **All logged-in users** can add publications and authors
- **Editors and Admins** can edit/delete content
- **Admins only** can manage users and access dashboard
- This allows community contribution while maintaining content quality control

---

## Current Project State

### Working Features ✓
- User registration and authentication
- Role-based access control
- Publication browsing with enhanced search/filter
- PDF viewing with view counter
- Author profiles with statistics
- Add content (publications/authors) for all logged-in users
- Edit/delete publications (editors/admins)
- Edit/delete authors (editors/admins)
- Admin dashboard with statistics
- User management (admin only)
- REST API with JWT authentication
- Caching for performance
- Chart.js visualizations
- Pagination on homepage
- Date formatting
- Secure session management

### Database Collections
1. **publications** - Enhanced with timestamps and counters
2. **authors** - Enhanced with timestamps
3. **users** - NEW: User accounts with roles and favorites

### File Structure
```
Codebase is now modular with:
- app.py (66 lines) - Main application entry point
- config.py - Configuration management
- .gitignore - Git ignore rules
- models/ - Data models (User, Publication, Author)
- routes/ - Route blueprints (main, auth, admin, api)
- utils/ - Utility functions (auth, db)
- templates/ - Organized templates (auth/, admin/)
- requirements.txt - 12 dependencies
- .env - Environment variables (NOT in git)
- memory/ - Project documentation
- SETUP.md - Setup instructions
- IMPLEMENTATION_SUMMARY.md - Implementation details
```

### Version Control
- **Repository:** git@github.com:alfodri/WRDC_lib.git
- **Branch:** main
- **Status:** Initial commit pushed
- **Excluded from Git:**
  - `static/uploads/` - All uploaded PDFs, covers, author images
  - `.env` - Environment variables with secrets
  - `venv/` - Virtual environment
  - `__pycache__/` - Python cache files

---

## Recent Changes Log

**2026-01-13 (GitHub Repository):**
- Git repository initialized
- Project pushed to GitHub (git@github.com:alfodri/WRDC_lib.git)
- Created .gitignore to exclude uploaded files and sensitive data
- Repository ready for collaboration

**2026-01-13 (Major Enhancement):**
- Complete system refactoring and enhancement
- Security improvements (bcrypt, env variables)
- User registration and authentication system
- Full CRUD operations
- REST API implementation
- Performance optimizations
- Permission system update (all users can add books)

**2026-01-13 (Initial):**
- Initial memory system setup
- Documentation created for agent context

---

## Important Context for Agents

### When Making Changes
1. **Database:** Always use PyMongo syntax (not SQLAlchemy)
2. **Files:** Store only filenames in DB, full files in static/uploads/
3. **Dates:** Use ISO string format (YYYY-MM-DD) for consistency
4. **Authentication:** Use decorators: `@user_required`, `@editor_required`, `@admin_required`
5. **File Security:** Always use `secure_filename()` on uploads
6. **Configuration:** Use `config.py` and `.env` file (never hardcode secrets)
7. **Routes:** Use blueprint route names: `main.index`, `auth.login`, `admin.dashboard`, etc.

### Common Tasks
- **Adding a route:** Add to appropriate blueprint in `routes/` folder
- **Modifying schema:** Update model class in `models/`, update ARCHITECTURE.md
- **Adding features:** Document in FEATURES.md
- **New patterns:** Add to CONVENTIONS.md
- **Permission changes:** Update decorators in `utils/auth.py`

### Testing Checklist
- [ ] Test with MongoDB running
- [ ] Test file uploads (size limits, extensions)
- [ ] Test authentication flow (login, register, logout)
- [ ] Test role-based access (viewer, editor, admin)
- [ ] Test CRUD operations
- [ ] Test pagination edge cases
- [ ] Test search with special characters
- [ ] Test with missing data (no author, no cover, etc.)
- [ ] Test API endpoints with JWT tokens
- [ ] Test caching behavior

---

## Notes for Next Session

**Completed:**
- ✅ All major enhancement phases implemented
- ✅ Permission system updated: all users can add books
- ✅ Security improvements completed
- ✅ REST API fully functional
- ✅ Project pushed to GitHub repository
- ✅ Git repository configured with proper exclusions

**Remaining Work:**
- UI redesign with Tailwind CSS (optional Phase 4)
- User profile editing page
- Favorites UI implementation
- Error pages (404, 500)
- Password change functionality

**User Preferences Learned:**
- User wants all logged-in users to be able to add books/publications
- Keep admin permissions for editing/deleting and user management
- Maintain existing Bootstrap UI (Tailwind redesign can be optional)

---

## Agent Update Instructions

**Before closing a chat session:**
1. Update the "Session History" section with today's date
2. Log all changes made in "Recent Changes Log"
3. Add any new issues to "Known TODOs"
4. Update "Current Project State" if significant changes
5. Add notes in "Notes for Next Session"
6. Update "Last Updated" timestamp at top of file

**Keep this file concise:** If session history grows beyond 10 entries, archive old sessions to a separate file.
