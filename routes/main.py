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
    
    # Handle sort field - if sorting by author, use authors array (MongoDB sorts by first element)
    # For backward compatibility, also check author field
    if sort == 'author':
        # MongoDB will sort by first element of array, or fallback to author field
        sort = [('authors', 1), ('author', 1)]
    
    query = {}
    query_parts = []
    
    # Enhanced search: Use regex for now (text search requires proper setup)
    if search:
        search_query = {
            '$or': [
                {'title': {'$regex': search, '$options': 'i'}},
                {'authors': {'$regex': search, '$options': 'i'}},  # Search in authors array
                {'author': {'$regex': search, '$options': 'i'}},  # Backward compatibility
                {'category': {'$regex': search, '$options': 'i'}}
            ]
        }
        query_parts.append(search_query)
    
    if author:
        # Support both old format (author string) and new format (authors array)
        author_query = {
            '$or': [
                {'authors': {'$in': [author]}},  # New format: author in array
                {'author': author}  # Old format: exact match
            ]
        }
        query_parts.append(author_query)
    
    # Add simple filters
    if category:
        query_parts.append({'category': category})
    
    if publish_date:
        query_parts.append({'publish_date': publish_date})
    
    # Combine all query parts
    if len(query_parts) > 1:
        query = {'$and': query_parts}
    elif len(query_parts) == 1:
        query = query_parts[0]
    
    publications_cursor = db.publications.find(query).sort(sort).skip((page - 1) * per_page).limit(per_page)
    publications = []
    for pub in publications_cursor:
        # Get authors list (handle both old and new format)
        authors_list = Publication.get_authors_display(pub)
        pub['authors_list'] = authors_list
        
        # Get author images for all authors
        author_images = {}
        for author_name in authors_list:
            author_info = Author.get_by_name(db, author_name)
            if author_info and author_info.get('image'):
                author_images[author_name] = author_info['image']
        pub['author_images'] = author_images
        publications.append(pub)
    
    total_publications = db.publications.count_documents(query)
    total_pages = (total_publications + per_page - 1) // per_page

    # Use cache for aggregation queries (cache is optional, works without it too)
    try:
        cache = current_app.cache
        authors = cache.get('authors_list')
        if authors is None:
            # Unwind authors array to get individual authors, handle both old and new format
            authors = list(db.publications.aggregate([
                {"$project": {
                    "author": 1,
                    "authors": 1,
                    "all_authors": {
                        "$cond": {
                            "if": {"$isArray": "$authors"},
                            "then": "$authors",
                            "else": {"$cond": {
                                "if": {"$ne": ["$author", None]},
                                "then": ["$author"],
                                "else": []
                            }}
                        }
                    }
                }},
                {"$unwind": "$all_authors"},
                {"$group": {"_id": "$all_authors", "count": {"$sum": 1}}},
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
            {"$project": {
                "author": 1,
                "authors": 1,
                "all_authors": {
                    "$cond": {
                        "if": {"$isArray": "$authors"},
                        "then": "$authors",
                        "else": {"$cond": {
                            "if": {"$ne": ["$author", None]},
                            "then": ["$author"],
                            "else": []
                        }}
                    }
                }
            }},
            {"$unwind": "$all_authors"},
            {"$group": {"_id": "$all_authors", "count": {"$sum": 1}}},
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
    
    # Find publications where author is in authors array or matches old author field
    latest_publications = list(db.publications.find({
        "$or": [
            {"authors": {"$in": [author['name']]}},
            {"author": author['name']}
        ]
    }).sort("publish_date", -1).limit(5))
    
    publish_date_counts = list(db.publications.aggregate([
        {"$match": {
            "$or": [
                {"authors": {"$in": [author['name']]}},
                {"author": author['name']}
            ]
        }},
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
    
    # Get authors list (handle both old and new format)
    authors_list = Publication.get_authors_display(publication)
    publication['authors_list'] = authors_list
    
    # Get author images for all authors
    author_images = {}
    for author_name in authors_list:
        author_info = Author.get_by_name(db, author_name)
        if author_info and author_info.get('image'):
            author_images[author_name] = author_info['image']
    publication['author_images'] = author_images

    pdf_url = url_for('static', filename='uploads/pdfs/' + publication['pdf_filename'])
    return render_template('view_pdf.html', publication=publication, pdf_url=pdf_url)

@main_bp.route('/guideline')
def guideline():
    """Author submission guidelines"""
    return render_template('guideline.html')
