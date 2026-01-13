from flask import current_app, g
from flask_pymongo import PyMongo

mongo = PyMongo()

def get_db():
    """Get MongoDB database instance"""
    if 'db' not in g:
        g.db = mongo.db
    return g.db

def init_db(app):
    """Initialize database connection"""
    mongo.init_app(app)
    
    # Create indexes for better performance
    db = mongo.db
    
    # Text index for full-text search (MongoDB allows only one text index per collection)
    try:
        # Drop existing text index if it exists
        try:
            db.publications.drop_index("title_text_category_text_author_text")
        except:
            pass
        # Create new text index
        db.publications.create_index([
            ("title", "text"),
            ("category", "text"),
            ("author", "text")
        ], name="title_text_category_text_author_text")
    except Exception as e:
        print(f"Note: Text index creation: {e}")
    
    # Regular indexes for performance
    try:
        db.publications.create_index("author")
        db.publications.create_index("category")
        db.publications.create_index("publish_date")
        db.publications.create_index("created_at")
        db.users.create_index("username", unique=True)
        db.users.create_index("email", unique=True)
        db.authors.create_index("name")
    except Exception as e:
        print(f"Note: Index creation: {e}")
