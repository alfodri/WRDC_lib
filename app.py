from flask import Flask, render_template
from flask_caching import Cache
from config import Config
from utils.db import init_db
from routes import main_bp, auth_bp, admin_bp, api_bp
from models.user import User
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
init_db(app)

# Initialize cache
cache = Cache(app, config={
    'CACHE_TYPE': Config.CACHE_TYPE,
    'CACHE_DEFAULT_TIMEOUT': Config.CACHE_DEFAULT_TIMEOUT
})

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

# Ensure upload directories exist
os.makedirs(Config.PDF_FOLDER, exist_ok=True)
os.makedirs(Config.COVER_FOLDER, exist_ok=True)
os.makedirs(Config.AUTHOR_FOLDER, exist_ok=True)

# Custom date filter
from datetime import datetime
@app.template_filter('format_date')
def format_date(value, format='%B %d, %Y'):
    try:
        return datetime.strptime(value, '%Y-%m-%d').strftime(format)
    except:
        return value

# Create default admin user if it doesn't exist
def create_default_admin():
    """Create default admin user if no users exist"""
    from utils.db import get_db
    db = get_db()
    
    if db.users.count_documents({}) == 0:
        # Create default admin user
        User.create_user(
            db,
            username='admin',
            email='admin@wrdc.kw',
            password='admin123',  # Change this in production!
            role='admin'
        )
        print("Default admin user created: username='admin', password='admin123'")
        print("⚠️  IMPORTANT: Change the default password in production!")

# Migrate publications from single author to authors array
def migrate_authors_to_array():
    """Convert existing publications with single 'author' field to 'authors' array"""
    from utils.db import get_db
    from datetime import datetime
    db = get_db()
    
    # Find publications that have 'author' field but not 'authors' array
    publications_to_migrate = db.publications.find({
        'author': {'$exists': True},
        'authors': {'$exists': False}
    })
    
    migrated_count = 0
    for pub in publications_to_migrate:
        if pub.get('author') and not pub.get('authors'):
            # Convert single author to authors array
            db.publications.update_one(
                {'_id': pub['_id']},
                {
                    '$set': {
                        'authors': [pub['author']],
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            migrated_count += 1
    
    if migrated_count > 0:
        print(f"✅ Migrated {migrated_count} publication(s) from single author to authors array")

# Note: before_first_request is deprecated in Flask 2.2+
# Using app context instead

if __name__ == '__main__':
    with app.app_context():
        create_default_admin()
        migrate_authors_to_array()
    app.run(host='0.0.0.0', port=2000, debug=True)
