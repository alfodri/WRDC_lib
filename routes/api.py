from flask import jsonify, request
from functools import wraps
from bson.objectid import ObjectId
from bson.errors import InvalidId
from . import api_bp
from models.publication import Publication
from models.author import Author
from models.user import User
from utils.db import get_db
import jwt
from datetime import datetime, timedelta
from config import Config

def token_required(f):
    """Decorator for API token authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'status': 'error', 'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            db = get_db()
            current_user = User.get_by_id(db, data['user_id'])
            
            if not current_user:
                return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'status': 'error', 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@api_bp.route('/publications', methods=['GET'])
def get_publications():
    """Get list of publications"""
    db = get_db()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    search = request.args.get('search')
    author = request.args.get('author')
    category = request.args.get('category')
    
    query = {}
    if search:
        query['title'] = {'$regex': search, '$options': 'i'}
    if author:
        query['author'] = author
    if category:
        query['category'] = category
    
    skip = (page - 1) * per_page
    publications = list(db.publications.find(query).skip(skip).limit(per_page))
    total = db.publications.count_documents(query)
    
    # Convert ObjectId to string
    for pub in publications:
        pub['_id'] = str(pub['_id'])
        if 'created_at' in pub:
            pub['created_at'] = pub['created_at'].isoformat() if isinstance(pub['created_at'], datetime) else str(pub['created_at'])
        if 'updated_at' in pub:
            pub['updated_at'] = pub['updated_at'].isoformat() if isinstance(pub['updated_at'], datetime) else str(pub['updated_at'])
    
    return jsonify({
        'status': 'success',
        'data': publications,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    })

@api_bp.route('/publications/<publication_id>', methods=['GET'])
def get_publication(publication_id):
    """Get single publication"""
    try:
        db = get_db()
        publication = Publication.get_by_id(db, publication_id)
        
        if not publication:
            return jsonify({'status': 'error', 'message': 'Publication not found'}), 404
        
        publication['_id'] = str(publication['_id'])
        if 'created_at' in publication:
            publication['created_at'] = publication['created_at'].isoformat() if isinstance(publication['created_at'], datetime) else str(publication['created_at'])
        if 'updated_at' in publication:
            publication['updated_at'] = publication['updated_at'].isoformat() if isinstance(publication['updated_at'], datetime) else str(publication['updated_at'])
        
        return jsonify({'status': 'success', 'data': publication})
    except InvalidId:
        return jsonify({'status': 'error', 'message': 'Invalid publication ID'}), 400

@api_bp.route('/publications', methods=['POST'])
@token_required
def create_publication(current_user):
    """Create new publication (requires authentication)"""
    if current_user.get('role') not in ['admin', 'editor']:
        return jsonify({'status': 'error', 'message': 'Permission denied'}), 403
    
    data = request.json
    required_fields = ['title', 'author', 'category', 'publish_date']
    
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    db = get_db()
    publication_id = Publication.create(
        db,
        data['title'],
        data['author'],
        data['category'],
        data['publish_date'],
        data.get('pdf_filename', ''),
        data.get('cover_filename', '')
    )
    
    return jsonify({
        'status': 'success',
        'message': 'Publication created',
        'data': {'id': str(publication_id)}
    }), 201

@api_bp.route('/publications/<publication_id>', methods=['PUT'])
@token_required
def update_publication(current_user, publication_id):
    """Update publication (requires authentication)"""
    if current_user.get('role') not in ['admin', 'editor']:
        return jsonify({'status': 'error', 'message': 'Permission denied'}), 403
    
    try:
        db = get_db()
        publication = Publication.get_by_id(db, publication_id)
        
        if not publication:
            return jsonify({'status': 'error', 'message': 'Publication not found'}), 404
        
        data = request.json
        Publication.update(db, publication_id, **data)
        
        return jsonify({'status': 'success', 'message': 'Publication updated'})
    except InvalidId:
        return jsonify({'status': 'error', 'message': 'Invalid publication ID'}), 400

@api_bp.route('/publications/<publication_id>', methods=['DELETE'])
@token_required
def delete_publication(current_user, publication_id):
    """Delete publication (requires authentication)"""
    if current_user.get('role') not in ['admin', 'editor']:
        return jsonify({'status': 'error', 'message': 'Permission denied'}), 403
    
    try:
        db = get_db()
        publication = Publication.get_by_id(db, publication_id)
        
        if not publication:
            return jsonify({'status': 'error', 'message': 'Publication not found'}), 404
        
        Publication.delete(db, publication_id)
        return jsonify({'status': 'success', 'message': 'Publication deleted'})
    except InvalidId:
        return jsonify({'status': 'error', 'message': 'Invalid publication ID'}), 400

@api_bp.route('/authors', methods=['GET'])
def get_authors():
    """Get list of authors"""
    db = get_db()
    authors = list(db.authors.find())
    
    for author in authors:
        author['_id'] = str(author['_id'])
        if 'created_at' in author:
            author['created_at'] = author['created_at'].isoformat() if isinstance(author['created_at'], datetime) else str(author['created_at'])
        if 'updated_at' in author:
            author['updated_at'] = author['updated_at'].isoformat() if isinstance(author['updated_at'], datetime) else str(author['updated_at'])
    
    return jsonify({'status': 'success', 'data': authors})

@api_bp.route('/authors/<author_id>', methods=['GET'])
def get_author(author_id):
    """Get single author"""
    try:
        db = get_db()
        author = Author.get_by_id(db, author_id)
        
        if not author:
            return jsonify({'status': 'error', 'message': 'Author not found'}), 404
        
        author['_id'] = str(author['_id'])
        if 'created_at' in author:
            author['created_at'] = author['created_at'].isoformat() if isinstance(author['created_at'], datetime) else str(author['created_at'])
        if 'updated_at' in author:
            author['updated_at'] = author['updated_at'].isoformat() if isinstance(author['updated_at'], datetime) else str(author['updated_at'])
        
        return jsonify({'status': 'success', 'data': author})
    except InvalidId:
        return jsonify({'status': 'error', 'message': 'Invalid author ID'}), 400

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get list of categories"""
    db = get_db()
    categories = list(db.publications.aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]))
    
    return jsonify({
        'status': 'success',
        'data': [{'name': cat['_id'], 'count': cat['count']} for cat in categories]
    })

@api_bp.route('/search', methods=['GET'])
def search():
    """Search publications"""
    db = get_db()
    query_text = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    if not query_text:
        return jsonify({'status': 'error', 'message': 'Query parameter q is required'}), 400
    
    # Use MongoDB text search if index exists, otherwise use regex
    try:
        query = {"$text": {"$search": query_text}}
        publications = list(db.publications.find(query).skip((page - 1) * per_page).limit(per_page))
        total = db.publications.count_documents(query)
    except:
        # Fallback to regex search
        query = {
            "$or": [
                {"title": {"$regex": query_text, "$options": "i"}},
                {"author": {"$regex": query_text, "$options": "i"}},
                {"category": {"$regex": query_text, "$options": "i"}}
            ]
        }
        publications = list(db.publications.find(query).skip((page - 1) * per_page).limit(per_page))
        total = db.publications.count_documents(query)
    
    for pub in publications:
        pub['_id'] = str(pub['_id'])
    
    return jsonify({
        'status': 'success',
        'data': publications,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    })

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get library statistics"""
    db = get_db()
    
    stats = {
        'total_publications': db.publications.count_documents({}),
        'total_authors': db.authors.count_documents({}),
        'total_users': db.users.count_documents({}),
        'publications_by_year': list(db.publications.aggregate([
            {"$group": {"_id": {"$year": {"$dateFromString": {"dateString": "$publish_date"}}}, "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ])),
        'publications_by_category': list(db.publications.aggregate([
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]))
    }
    
    return jsonify({'status': 'success', 'data': stats})

@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    """API login endpoint - returns JWT token"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400
    
    db = get_db()
    user = User.authenticate(db, username, password)
    
    if user:
        token = jwt.encode({
            'user_id': str(user['_id']),
            'username': user['username'],
            'role': user['role'],
            'exp': datetime.utcnow() + timedelta(days=7)
        }, Config.SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'status': 'success',
            'data': {
                'token': token,
                'user': {
                    'id': str(user['_id']),
                    'username': user['username'],
                    'role': user['role']
                }
            }
        })
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
