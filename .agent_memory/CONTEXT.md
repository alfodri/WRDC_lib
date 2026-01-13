# CONTEXT.md

**Last Updated:** 2026-01-13

> **Instructions for AI Agents:**  
> This is a living document. Update this file at the end of each conversation session.  
> Add notes about changes made, issues discovered, user preferences, and next steps.

---

## Session History

### Session: 2026-01-13
**Agent:** Initial setup  
**Changes Made:**
- Created `.agent_memory/` folder structure
- Generated initial documentation files:
  - PROJECT.md (103 lines) - Project overview and setup
  - ARCHITECTURE.md (143 lines) - Routes, schema, file structure
  - FEATURES.md (157 lines) - User and admin features
  - CONVENTIONS.md (177 lines) - Code patterns and conventions
  - CONTEXT.md (this file)
  - README.md (agent instructions)

**Notes:**
- Project is a Flask-based digital library for WRDC (Water Resources Development Center)
- Focus is on water treatment/desalination technical documentation
- Currently serving historical reports from 1972-1980s
- Admin authentication is basic (hardcoded password: 'admin')
- MongoDB running locally at mongodb://localhost:27017/library

**Issues/Observations:**
- ⚠️ Security: Admin password is hardcoded - should be environment variable in production
- ⚠️ Security: Secret key is hardcoded - should be randomized and stored securely
- ⚠️ Debug mode is enabled - should be disabled in production
- No user registration system - admin only
- No edit/delete functionality for publications or authors
- No pagination for authors page
- No search functionality on authors page

---

## Known TODOs / Future Enhancements

### High Priority
- [ ] Implement secure authentication (bcrypt, environment variables)
- [ ] Add edit functionality for publications and authors
- [ ] Add delete functionality with confirmation dialogs
- [ ] Implement proper error pages (404, 500)

### Medium Priority
- [ ] Add search functionality to authors page
- [ ] Implement pagination for authors listing
- [ ] Add thumbnail generation for PDFs (currently using uploaded covers)
- [ ] Add download counters for publications
- [ ] Implement user roles (admin, editor, viewer)

### Low Priority
- [ ] Add export functionality (CSV/Excel of publications)
- [ ] Implement advanced search (full-text search across PDFs)
- [ ] Add tags/keywords to publications
- [ ] Implement favorites/bookmarks for users
- [ ] Add comments/notes system for publications

### Infrastructure
- [ ] Add proper logging system
- [ ] Implement backup system for MongoDB
- [ ] Add file size limits for uploads
- [ ] Implement image compression for uploads
- [ ] Add configuration file (config.py) instead of hardcoded values

---

## User Preferences & Design Decisions

### Technology Choices
- **Frontend:** Bootstrap 4.5.2 (existing in project)
- **Charts:** Chart.js (existing in project)
- **Database:** MongoDB (document-oriented, flexible schema)
- **No ORM:** Direct PyMongo usage for simplicity

### Design Patterns
- Simple MVC pattern via Flask + Jinja2
- File-based storage for uploads (not database)
- Filename-only storage in database (not full paths)
- ISO date strings for compatibility

### UI/UX Decisions
- Kuwait MEW branding (logos, colors)
- Card-based layout for visual appeal
- Embedded PDF viewer (no download required)
- Sidebar analytics on homepage
- Author profiles include publications and statistics

---

## Current Project State

### Working Features ✓
- Publication browsing with search/filter
- PDF viewing with embedded viewer
- Author profiles with statistics
- Admin panel for adding content
- Chart.js visualizations
- Pagination on homepage
- Date formatting
- Session-based authentication

### Database Collections
1. **publications** - Currently populated with 15+ historical reports
2. **authors** - Currently populated with author data

### File Structure
```
Codebase is organized with:
- Single app.py file (222 lines)
- 7 HTML templates with Bootstrap
- Static uploads folder with 3 subfolders
- Requirements.txt with 4 dependencies
- .agent_memory/ folder for AI context
```

---

## Recent Changes Log

**2026-01-13:**
- Initial memory system setup
- No code changes to main application
- Documentation created for agent context

---

## Important Context for Agents

### When Making Changes
1. **Database:** Always use PyMongo syntax (not SQLAlchemy)
2. **Files:** Store only filenames in DB, full files in static/uploads/
3. **Dates:** Use ISO string format (YYYY-MM-DD) for consistency
4. **Authentication:** Check `session.get('logged_in')` before admin operations
5. **File Security:** Always use `secure_filename()` on uploads

### Common Tasks
- **Adding a route:** Follow pattern in app.py, add template if needed
- **Modifying schema:** Update both ARCHITECTURE.md and database
- **Adding features:** Document in FEATURES.md
- **New patterns:** Add to CONVENTIONS.md

### Testing Checklist
- [ ] Test with MongoDB running
- [ ] Test file uploads (size limits, extensions)
- [ ] Test authentication flow
- [ ] Test pagination edge cases
- [ ] Test search with special characters
- [ ] Test with missing data (no author, no cover, etc.)

---

## Notes for Next Session

*Agent: Add notes here about:*
- *What the user requested*
- *What was completed*
- *What remains to be done*
- *Any blockers or issues*
- *User feedback or preferences learned*

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
