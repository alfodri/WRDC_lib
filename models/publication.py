from datetime import datetime
from bson.objectid import ObjectId

class Publication:
    """Publication model"""
    
    @staticmethod
    def create(db, title, author, category, publish_date, pdf_filename, cover_filename):
        """Create a new publication"""
        publication = {
            'title': title,
            'author': author,
            'category': category,
            'publish_date': datetime.strptime(publish_date, '%Y-%m-%d').date().isoformat(),
            'pdf_filename': pdf_filename,
            'cover_filename': cover_filename,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'download_count': 0,
            'view_count': 0
        }
        result = db.publications.insert_one(publication)
        return result.inserted_id
    
    @staticmethod
    def update(db, publication_id, **kwargs):
        """Update publication fields"""
        kwargs['updated_at'] = datetime.utcnow()
        db.publications.update_one(
            {'_id': ObjectId(publication_id)},
            {'$set': kwargs}
        )
    
    @staticmethod
    def delete(db, publication_id):
        """Delete a publication"""
        return db.publications.delete_one({'_id': ObjectId(publication_id)})
    
    @staticmethod
    def get_by_id(db, publication_id):
        """Get publication by ID"""
        return db.publications.find_one({'_id': ObjectId(publication_id)})
    
    @staticmethod
    def increment_view_count(db, publication_id):
        """Increment view count"""
        db.publications.update_one(
            {'_id': ObjectId(publication_id)},
            {'$inc': {'view_count': 1}}
        )
    
    @staticmethod
    def increment_download_count(db, publication_id):
        """Increment download count"""
        db.publications.update_one(
            {'_id': ObjectId(publication_id)},
            {'$inc': {'download_count': 1}}
        )
