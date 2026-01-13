from datetime import datetime
from bson.objectid import ObjectId

class Publication:
    """Publication model"""
    
    @staticmethod
    def create(db, title, authors, category, publish_date, pdf_filename, cover_filename):
        """Create a new publication
        
        Args:
            authors: List of author names (can be single-item list for backward compatibility)
        """
        # Ensure authors is a list
        if isinstance(authors, str):
            authors = [authors]
        elif not isinstance(authors, list):
            authors = list(authors) if authors else []
        
        # Ensure at least one author
        if not authors or len(authors) == 0:
            raise ValueError("At least one author is required")
        
        publication = {
            'title': title,
            'authors': authors,
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
        """Update publication fields
        
        If 'authors' is provided as a string, it will be converted to a list.
        """
        # Ensure authors is a list if provided
        if 'authors' in kwargs:
            if isinstance(kwargs['authors'], str):
                kwargs['authors'] = [kwargs['authors']]
            elif not isinstance(kwargs['authors'], list):
                kwargs['authors'] = list(kwargs['authors']) if kwargs['authors'] else []
        
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
    
    @staticmethod
    def get_authors_display(publication):
        """Get formatted authors display string
        
        Handles both old format (author string) and new format (authors array)
        """
        if 'authors' in publication and isinstance(publication['authors'], list):
            return publication['authors']
        elif 'author' in publication:
            # Backward compatibility: convert old single author to list
            return [publication['author']]
        return []
