from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import os
from . import admin_bp
from models.publication import Publication
from models.author import Author
from models.user import User
from utils.auth import admin_required, editor_required, user_required, get_current_user
from utils.db import get_db
from config import Config
from utils.pdf_helper import generate_pdf_thumbnail

@admin_bp.route('/')
@admin_required
def admin_redirect():
    """Redirect old /admin route to dashboard"""
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard overview"""
    db = get_db()
    
    stats = {
        'total_publications': db.publications.count_documents({}),
        'total_authors': db.authors.count_documents({}),
        'total_users': db.users.count_documents({}),
        'recent_publications': list(db.publications.find().sort('created_at', -1).limit(5)),
        'recent_authors': list(db.authors.find().sort('created_at', -1).limit(5))
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/add')
@user_required
def add_content_page():
    """Page for any logged-in user to add publications/authors"""
    db = get_db()
    authors = db.authors.find()
    categories = db.publications.distinct("category")
    return render_template('admin/add_content.html', authors=authors, categories=categories)

@admin_bp.route('/publications')
@editor_required
def publications():
    """List all publications with edit/delete options"""
    db = get_db()
    page = int(request.args.get('page', 1))
    per_page = 20
    
    publications = db.publications.find().sort('created_at', -1).skip((page - 1) * per_page).limit(per_page)
    total = db.publications.count_documents({})
    total_pages = (total + per_page - 1) // per_page
    
    return render_template('admin/publications.html', 
                         publications=publications, 
                         page=page, 
                         total_pages=total_pages)

@admin_bp.route('/add_publication', methods=['POST'])
@user_required
def add_publication():
    """Add new publication"""
    db = get_db()
    
    title = request.form.get('title')
    author = request.form.get('author')
    category = request.form.get('category')
    publish_date = request.form.get('publish_date')
    pdf = request.files.get('pdf')
    cover = request.files.get('cover')

    if not all([title, author, category, publish_date, pdf]):
        flash('Publication title, author, category, publish_date, and PDF are required')
        return redirect(url_for('admin.dashboard'))

    if pdf.filename == '':
        flash('Please select a PDF file')
        return redirect(url_for('admin.dashboard'))

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    if pdf and allowed_file(pdf.filename):
        pdf_filename = secure_filename(pdf.filename)
        os.makedirs(Config.PDF_FOLDER, exist_ok=True)
        pdf_path = os.path.join(Config.PDF_FOLDER, pdf_filename)
        pdf.save(pdf_path)
        
        # Handle cover image
        if cover and cover.filename != '' and allowed_file(cover.filename):
            cover_filename = secure_filename(cover.filename)
            os.makedirs(Config.COVER_FOLDER, exist_ok=True)
            cover.save(os.path.join(Config.COVER_FOLDER, cover_filename))
        else:
            # Generate cover from PDF
            cover_filename = pdf_filename.rsplit('.', 1)[0] + "_cover.jpg"
            os.makedirs(Config.COVER_FOLDER, exist_ok=True)
            cover_path = os.path.join(Config.COVER_FOLDER, cover_filename)
            if generate_pdf_thumbnail(pdf_path, cover_path):
                flash('Cover image automatically generated from PDF first page.')
            else:
                cover_filename = "default_cover.jpg" # Fallback if generation fails

        Publication.create(db, title, author, category, publish_date, pdf_filename, cover_filename)
        flash('Publication added successfully!')
    else:
        flash('Invalid file type')

    # Redirect based on user role
    db = get_db()
    user = get_current_user(db)
    if user and user.get('role') in ['admin', 'editor']:
        return redirect(url_for('admin.publications'))
    return redirect(url_for('admin.add_content_page'))

@admin_bp.route('/edit_publication/<publication_id>', methods=['GET', 'POST'])
@editor_required
def edit_publication(publication_id):
    """Edit publication"""
    db = get_db()
    publication = Publication.get_by_id(db, publication_id)
    
    if not publication:
        flash('Publication not found')
        return redirect(url_for('admin.publications'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        category = request.form.get('category')
        publish_date = request.form.get('publish_date')
        pdf = request.files.get('pdf')
        cover = request.files.get('cover')
        
        update_data = {
            'title': title,
            'author': author,
            'category': category,
            'publish_date': publish_date
        }
        
        if pdf and pdf.filename:
            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
            
            if allowed_file(pdf.filename):
                pdf_filename = secure_filename(pdf.filename)
                os.makedirs(Config.PDF_FOLDER, exist_ok=True)
                pdf_path = os.path.join(Config.PDF_FOLDER, pdf_filename)
                pdf.save(pdf_path)
                update_data['pdf_filename'] = pdf_filename
                
                # If cover is not provided, regenerate it from the new PDF
                if not (cover and cover.filename):
                    cover_filename = pdf_filename.rsplit('.', 1)[0] + "_cover.jpg"
                    os.makedirs(Config.COVER_FOLDER, exist_ok=True)
                    cover_path = os.path.join(Config.COVER_FOLDER, cover_filename)
                    if generate_pdf_thumbnail(pdf_path, cover_path):
                        update_data['cover_filename'] = cover_filename
        
        if cover and cover.filename:
            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
            
            if allowed_file(cover.filename):
                cover_filename = secure_filename(cover.filename)
                os.makedirs(Config.COVER_FOLDER, exist_ok=True)
                cover.save(os.path.join(Config.COVER_FOLDER, cover_filename))
                update_data['cover_filename'] = cover_filename
        
        Publication.update(db, publication_id, **update_data)
        flash('Publication updated successfully!')
        return redirect(url_for('admin.publications'))
    
    authors = db.authors.find()
    categories = db.publications.distinct("category")
    return render_template('admin/edit_publication.html', publication=publication, authors=authors, categories=categories)

@admin_bp.route('/delete_publication/<publication_id>', methods=['POST'])
@editor_required
def delete_publication(publication_id):
    """Delete publication"""
    db = get_db()
    publication = Publication.get_by_id(db, publication_id)
    
    if not publication:
        flash('Publication not found')
        return redirect(url_for('admin.publications'))
    
    # Delete files
    try:
        if 'pdf_filename' in publication:
            pdf_path = os.path.join(Config.PDF_FOLDER, publication['pdf_filename'])
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        if 'cover_filename' in publication:
            cover_path = os.path.join(Config.COVER_FOLDER, publication['cover_filename'])
            if os.path.exists(cover_path):
                os.remove(cover_path)
    except Exception as e:
        flash(f'Error deleting files: {str(e)}')
    
    Publication.delete(db, publication_id)
    flash('Publication deleted successfully!')
    return redirect(url_for('admin.publications'))

@admin_bp.route('/authors')
@editor_required
def authors():
    """List all authors"""
    db = get_db()
    authors = db.authors.find()
    return render_template('admin/authors.html', authors=authors)

@admin_bp.route('/add_author', methods=['POST'])
@user_required
def add_author():
    """Add new author"""
    db = get_db()
    
    author_name = request.form.get('author_name')
    author_picture = request.files.get('author_picture')
    author_profile = request.form.get('author_profile')
    author_education = request.form.get('author_education')
    author_experience = request.form.get('author_experience')
    author_skills = request.form.get('author_skills')

    if not all([author_name, author_profile, author_education, author_experience, author_skills]):
        flash('All fields are required')
        return redirect(url_for('admin.dashboard'))

    if not author_picture or author_picture.filename == '':
        flash('Please select an author picture')
        return redirect(url_for('admin.dashboard'))

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    if author_picture and allowed_file(author_picture.filename):
        author_picture_filename = secure_filename(author_picture.filename)
        os.makedirs(Config.AUTHOR_FOLDER, exist_ok=True)
        author_picture.save(os.path.join(Config.AUTHOR_FOLDER, author_picture_filename))

        Author.create(db, author_name, author_picture_filename, author_profile, 
                     author_education, author_experience, author_skills)
        flash('Author added successfully!')
    else:
        flash('Invalid file type')

    # Redirect based on user role
    user = get_current_user(db)
    if user and user.get('role') in ['admin', 'editor']:
        return redirect(url_for('admin.authors'))
    return redirect(url_for('admin.add_content_page'))

@admin_bp.route('/edit_author/<author_id>', methods=['GET', 'POST'])
@editor_required
def edit_author(author_id):
    """Edit author"""
    db = get_db()
    author = Author.get_by_id(db, author_id)
    
    if not author:
        flash('Author not found')
        return redirect(url_for('admin.authors'))
    
    if request.method == 'POST':
        author_name = request.form.get('author_name')
        author_picture = request.files.get('author_picture')
        author_profile = request.form.get('author_profile')
        author_education = request.form.get('author_education')
        author_experience = request.form.get('author_experience')
        author_skills = request.form.get('author_skills')
        
        update_data = {
            'name': author_name,
            'profile': author_profile,
            'education': author_education,
            'experience': author_experience,
            'skills': author_skills
        }
        
        if author_picture and author_picture.filename:
            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
            
            if allowed_file(author_picture.filename):
                author_picture_filename = secure_filename(author_picture.filename)
                os.makedirs(Config.AUTHOR_FOLDER, exist_ok=True)
                author_picture.save(os.path.join(Config.AUTHOR_FOLDER, author_picture_filename))
                update_data['image'] = author_picture_filename
        
        Author.update(db, author_id, **update_data)
        flash('Author updated successfully!')
        return redirect(url_for('admin.authors'))
    
    return render_template('admin/edit_author.html', author=author)

@admin_bp.route('/delete_author/<author_id>', methods=['POST'])
@editor_required
def delete_author(author_id):
    """Delete author"""
    db = get_db()
    author = Author.get_by_id(db, author_id)
    
    if not author:
        flash('Author not found')
        return redirect(url_for('admin.authors'))
    
    # Delete image file
    try:
        if 'image' in author:
            image_path = os.path.join(Config.AUTHOR_FOLDER, author['image'])
            if os.path.exists(image_path):
                os.remove(image_path)
    except Exception as e:
        flash(f'Error deleting image: {str(e)}')
    
    Author.delete(db, author_id)
    flash('Author deleted successfully!')
    return redirect(url_for('admin.authors'))

@admin_bp.route('/users')
@admin_required
def users():
    """List all users"""
    db = get_db()
    users = db.users.find()
    return render_template('admin/users.html', users=users)
