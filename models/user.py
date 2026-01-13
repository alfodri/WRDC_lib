from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson.objectid import ObjectId

class User:
    """User model for authentication and authorization"""
    
    @staticmethod
    def create_user(db, username, email, password, role='viewer'):
        """Create a new user with hashed password"""
        password_hash = generate_password_hash(password)
        user = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'role': role,
            'created_at': datetime.utcnow(),
            'last_login': None,
            'favorites': []
        }
        result = db.users.insert_one(user)
        return result.inserted_id
    
    @staticmethod
    def authenticate(db, username, password):
        """Authenticate user by username and password"""
        user = db.users.find_one({'username': username})
        if user and check_password_hash(user['password_hash'], password):
            # Update last login
            db.users.update_one(
                {'_id': user['_id']},
                {'$set': {'last_login': datetime.utcnow()}}
            )
            return user
        return None
    
    @staticmethod
    def get_by_id(db, user_id):
        """Get user by ID"""
        return db.users.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def get_by_username(db, username):
        """Get user by username"""
        return db.users.find_one({'username': username})
    
    @staticmethod
    def get_by_email(db, email):
        """Get user by email"""
        return db.users.find_one({'email': email})
    
    @staticmethod
    def update_password(db, user_id, new_password):
        """Update user password"""
        password_hash = generate_password_hash(new_password)
        db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'password_hash': password_hash}}
        )
    
    @staticmethod
    def add_favorite(db, user_id, publication_id):
        """Add publication to user's favorites"""
        db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$addToSet': {'favorites': ObjectId(publication_id)}}
        )
    
    @staticmethod
    def remove_favorite(db, user_id, publication_id):
        """Remove publication from user's favorites"""
        db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$pull': {'favorites': ObjectId(publication_id)}}
        )
    
    @staticmethod
    def get_favorites(db, user_id):
        """Get user's favorite publications"""
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if user and 'favorites' in user:
            return list(db.publications.find({'_id': {'$in': user['favorites']}}))
        return []
    
    @staticmethod
    def has_role(user, role):
        """Check if user has a specific role"""
        return user and user.get('role') == role
    
    @staticmethod
    def is_admin(user):
        """Check if user is admin"""
        return User.has_role(user, 'admin')
    
    @staticmethod
    def is_editor(user):
        """Check if user is editor or admin"""
        return user and user.get('role') in ['admin', 'editor']
