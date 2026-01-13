# Agent Memory System - README

**Last Updated:** 2026-01-13

---

## Purpose

This folder contains structured documentation for AI agents to quickly understand the WRDC_lib project. Each file serves as persistent memory across chat sessions, limited to ~500 total lines for fast reading.

---

## File Guide

| File | Lines | Purpose | Update Frequency |
|------|-------|---------|------------------|
| **PROJECT.md** | ~100 | Project overview, tech stack, setup instructions | Rarely (major changes only) |
| **ARCHITECTURE.md** | ~120 | Routes, database schema, file structure | When adding routes or changing DB |
| **FEATURES.md** | ~80 | User and admin features documentation | When adding/removing features |
| **CONVENTIONS.md** | ~50 | Code patterns and naming conventions | When establishing new patterns |
| **CONTEXT.md** | ~100 | Session notes, recent changes, TODOs | **Every session** |
| **README.md** | ~50 | Instructions for agents (this file) | Rarely |

**Total:** ~500 lines

---

## Quick Start for AI Agents

### 1. First Time Reading the Project
Read files in this order:
1. **PROJECT.md** - Understand what this project is
2. **ARCHITECTURE.md** - Learn the structure and routes
3. **FEATURES.md** - Know what it can do
4. **CONVENTIONS.md** - Follow the patterns used
5. **CONTEXT.md** - Check recent changes and known issues

**Time to read:** ~2-3 minutes

---

### 2. When User Asks to Add/Modify Features

**Before coding:**
- Check **ARCHITECTURE.md** for existing routes and schema
- Check **CONVENTIONS.md** for patterns to follow
- Check **CONTEXT.md** for known issues or TODOs

**After coding:**
- Update **ARCHITECTURE.md** if routes/schema changed
- Update **FEATURES.md** if user-facing features added
- Update **CONTEXT.md** with what you changed

---

### 3. When User Asks Questions

**For "How does X work?" questions:**
- Check **FEATURES.md** for feature descriptions
- Check **ARCHITECTURE.md** for implementation details
- Check **CONVENTIONS.md** for patterns used

**For "Why is it done this way?" questions:**
- Check **CONVENTIONS.md** for established patterns
- Check **CONTEXT.md** for user preferences and design decisions

---

### 4. Before Ending a Chat Session

**ALWAYS update CONTEXT.md:**
1. Add session entry with date
2. List all changes made
3. Add any new issues discovered
4. Note user preferences learned
5. Add "Notes for Next Session" if work is incomplete
6. Update timestamp at top

**Example session entry:**
```markdown
### Session: 2026-01-13
**Agent:** Claude
**Changes Made:**
- Added edit functionality for publications
- Updated publications schema to include last_modified field

**Notes:**
- User prefers minimal UI changes
- Keep Bootstrap 4 (don't upgrade to 5)
- Next: Add delete functionality with confirmation dialog
```

---

## Update Guidelines

### When to Update Each File

**PROJECT.md:**
- New dependencies added
- Major tech stack changes
- Setup instructions change
- Port or configuration changes

**ARCHITECTURE.md:**
- New routes added
- Database schema modified
- New collections created
- File structure reorganized
- Query patterns changed

**FEATURES.md:**
- New user-facing features
- Removed features
- Significant feature modifications
- New admin capabilities

**CONVENTIONS.md:**
- New code patterns established
- Naming conventions changed
- Template structure modified
- New best practices adopted

**CONTEXT.md:**
- **EVERY SESSION** - add session notes
- New TODOs discovered
- Issues resolved
- User preferences learned
- Design decisions made

---

## Best Practices for Agents

### ✅ DO:
- Read relevant files before making changes
- Update documentation alongside code changes
- Keep entries concise and scannable
- Use bullet points and tables
- Include code examples in CONVENTIONS.md
- Mark completed TODOs in CONTEXT.md
- Timestamp your updates

### ❌ DON'T:
- Write essays - keep it brief
- Duplicate information across files
- Skip updating CONTEXT.md at session end
- Remove information - archive instead
- Use vague descriptions - be specific
- Forget to update "Last Updated" timestamps

---

## File Size Management

**Target:** Each file stays under its line limit

**If a file grows too large:**
- **PROJECT.md / ARCHITECTURE.md / FEATURES.md / CONVENTIONS.md:**  
  Keep only current, relevant information. Archive old patterns/removed features.

- **CONTEXT.md:**  
  When session history exceeds 10 entries, create `ARCHIVE_YYYY.md` and move old sessions there.

---

## Integration with Code

### In Code Comments
When adding complex logic, reference memory files:
```python
# Pattern from CONVENTIONS.md - File Upload Pattern
filename = secure_filename(file.filename)
```

### In Commit Messages
Reference memory updates:
```
feat: Add edit publication functionality

- Updated ARCHITECTURE.md with new /edit_publication route
- Updated FEATURES.md with edit feature description
- Updated CONTEXT.md with session notes
```

---

## Emergency Recovery

**If memory files are lost or corrupted:**

1. Read the actual codebase (`app.py`, templates)
2. Regenerate memory files based on code
3. Check git history for recent changes
4. Review CONTEXT.md backup (if available)

**Prevention:**
- Keep files in version control
- Update regularly to stay in sync with code

---

## Memory File Structure

All files follow this structure:
```markdown
# FILENAME.md

**Last Updated:** YYYY-MM-DD

---

## Section 1
Content...

---

## Section 2
Content...
```

**Consistent formatting makes scanning easier for agents.**

---

## Questions?

If you're an AI agent and these instructions are unclear:
1. Check **CONTEXT.md** for project-specific notes
2. Read the actual code in `app.py` as ground truth
3. Ask the user for clarification
4. Update this README with the answer for future agents

---

**Remember:** These files are your persistent memory. Keep them accurate, concise, and up-to-date! 🧠
