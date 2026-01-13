from flask import render_template, request, redirect, url_for, flash, current_app
from . import main_bp
from models.publication import Publication
from models.author import Author
from utils.db import get_db

@main_bp.route('/')
def index():
    """Homepage with publication grid, search, filters, pagination"""
    db = get_db()
    search = request.args.get('search')
    author = request.args.get('author')
    category = request.args.get('category')
    publish_date = request.args.get('publish_date')
    sort = request.args.get('sort', 'title')
    page = int(request.args.get('page', 1))
    per_page = 9
    
    query = {}
    # Enhanced search: Use regex for now (text search requires proper setup)
    if search:
        query['$or'] = [
            {'title': {'$regex': search, '$options': 'i'}},
            {'author': {'$regex': search, '$options': 'i'}},
            {'category': {'$regex': search, '$options': 'i'}}
        ]
    if author:
        query['author'] = author
    if category:
        query['category'] = category
    if publish_date:
        query['publish_date'] = publish_date
    
    # If we have both search ($or) and filters, combine them
    if '$or' in query and len([k for k in query.keys() if k != '$or']) > 0:
        filters = {k: v for k, v in query.items() if k != '$or'}
        query = {'$and': [{'$or': query['$or']}, filters]}
    
    publications = db.publications.find(query).sort(sort).skip((page - 1) * per_page).limit(per_page)
    total_publications = db.publications.count_documents(query)
    total_pages = (total_publications + per_page - 1) // per_page

    # Use cache for aggregation queries (cache is optional, works without it too)
    try:
        cache = current_app.cache
        authors = cache.get('authors_list')
        if authors is None:
            authors = list(db.publications.aggregate([
                {"$group": {"_id": "$author", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ]))
            cache.set('authors_list', authors, timeout=300)
        
        categories = cache.get('categories_list')
        if categories is None:
            categories = list(db.publications.aggregate([
                {"$group": {"_id": "$category", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ]))
            cache.set('categories_list', categories, timeout=300)
        
        publish_date_counts = cache.get('publish_date_counts')
        if publish_date_counts is None:
            publish_date_counts = list(db.publications.aggregate([
                {"$group": {"_id": {"$year": {"$dateFromString": {"dateString": "$publish_date"}}}, "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ]))
            cache.set('publish_date_counts', publish_date_counts, timeout=300)
    except:
        # Fallback if cache is not available
        authors = list(db.publications.aggregate([
            {"$group": {"_id": "$author", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]))
        categories = list(db.publications.aggregate([
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]))
        publish_date_counts = list(db.publications.aggregate([
            {"$group": {"_id": {"$year": {"$dateFromString": {"dateString": "$publish_date"}}}, "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]))
    
    publish_dates = list(db.publications.distinct("publish_date"))
    latest_publications = list(db.publications.find().sort("publish_date", -1).limit(5))
    
    years = [str(pd['_id']) for pd in publish_date_counts]
    counts = [pd['count'] for pd in publish_date_counts]

    return render_template('index.html', 
                         publications=publications, 
                         authors=authors, 
                         categories=categories, 
                         publish_dates=publish_dates, 
                         latest_publications=latest_publications, 
                         years=years, 
                         counts=counts, 
                         page=page, 
                         total_pages=total_pages)

@main_bp.route('/authors')
def authors():
    """List all authors"""
    db = get_db()
    authors = db.authors.find()
    return render_template('author.html', authors=authors)

@main_bp.route('/author/<author_id>')
def author_info(author_id):
    """Individual author profile with publications and stats"""
    db = get_db()
    author = Author.get_by_id(db, author_id)
    if not author:
        flash('Author not found')
        return redirect(url_for('main.authors'))
    
    latest_publications = db.publications.find({'author': author['name']}).sort("publish_date", -1).limit(5)
    
    publish_date_counts = list(db.publications.aggregate([
        {"$match": {"author": author['name']}},
        {"$group": {"_id": {"$year": {"$dateFromString": {"dateString": "$publish_date"}}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]))
    
    years = [str(pd['_id']) for pd in publish_date_counts]
    counts = [pd['count'] for pd in publish_date_counts]

    return render_template('author_info.html', 
                         author=author, 
                         latest_publications=latest_publications, 
                         years=years, 
                         counts=counts)

@main_bp.route('/view_pdf/<publication_id>')
def view_pdf(publication_id):
    """PDF viewer with publication metadata"""
    from flask import url_for
    from bson.objectid import ObjectId
    db = get_db()
    try:
        publication = Publication.get_by_id(db, publication_id)
    except:
        flash('Invalid publication ID')
        return redirect(url_for('main.index'))
    if not publication:
        flash('Publication not found')
        return redirect(url_for('main.index'))

    if 'pdf_filename' not in publication:
        flash('PDF file not found for this publication')
        return redirect(url_for('main.index'))

    Publication.increment_view_count(db, publication_id)
    
    author_info = Author.get_by_name(db, publication['author'])
    if author_info:
        publication['author_image'] = author_info.get('image', None)
    else:
        publication['author_image'] = None

    pdf_url = url_for('static', filename='uploads/pdfs/' + publication['pdf_filename'])
    return render_template('view_pdf.html', publication=publication, pdf_url=pdf_url)

@main_bp.route('/guideline')
def guideline():
    """Author submission guidelines"""
    return render_template('guideline.html')
