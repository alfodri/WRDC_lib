from datetime import datetime
from bson.objectid import ObjectId

class Author:
    """Author model"""
    
    @staticmethod
    def create(db, name, image, profile, education, experience, skills):
        """Create a new author"""
        author = {
            'name': name,
            'image': image,
            'profile': profile,
            'education': education,
            'experience': experience,
            'skills': skills,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = db.authors.insert_one(author)
        return result.inserted_id
    
    @staticmethod
    def update(db, author_id, **kwargs):
        """Update author fields"""
        kwargs['updated_at'] = datetime.utcnow()
        db.authors.update_one(
            {'_id': ObjectId(author_id)},
            {'$set': kwargs}
        )
    
    @staticmethod
    def delete(db, author_id):
        """Delete an author"""
        return db.authors.delete_one({'_id': ObjectId(author_id)})
    
    @staticmethod
    def get_by_id(db, author_id):
        """Get author by ID"""
        return db.authors.find_one({'_id': ObjectId(author_id)})
    
    @staticmethod
    def get_by_name(db, name):
        """Get author by name"""
        return db.authors.find_one({'name': name})
