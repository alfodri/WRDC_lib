from functools import wraps
from flask import session, redirect, url_for, flash, request
from models.user import User
from utils.db import get_db

def login_required(f=None, role=None):
    """Decorator to require login, optionally with specific role"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login to access this page')
                return redirect(url_for('auth.login'))
            
            if role:
                db = get_db()
                user = get_current_user(db)
                if not user or user.get('role') != role:
                    flash('You do not have permission to access this page')
                    return redirect(url_for('main.index'))
            
            return func(*args, **kwargs)
        return wrapper
    
    if f is None:
        return decorator
    else:
        return decorator(f)

def user_required(f):
    """Decorator to require any logged-in user (any role)"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    """Decorator to require admin role"""
    return login_required(f, role='admin')

def editor_required(f):
    """Decorator to require editor or admin role"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page')
            return redirect(url_for('auth.login'))
        
        db = get_db()
        user = get_current_user(db)
        if not user or user.get('role') not in ['admin', 'editor']:
            flash('You do not have permission to access this page')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return wrapper

def get_current_user(db):
    """Get current logged-in user"""
    if 'user_id' not in session:
        return None
    return User.get_by_id(db, session['user_id'])
