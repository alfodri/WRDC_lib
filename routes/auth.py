from flask import render_template, request, redirect, url_for, flash, session
from . import auth_bp
from models.user import User
from utils.db import get_db

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required')
            return render_template('login.html')
        
        db = get_db()
        user = User.authenticate(db, username, password)
        
        if user:
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome back, {username}!')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('All fields are required')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long')
            return render_template('auth/register.html')
        
        db = get_db()
        
        # Check if username already exists
        if User.get_by_username(db, username):
            flash('Username already exists')
            return render_template('auth/register.html')
        
        # Check if email already exists
        if User.get_by_email(db, email):
            flash('Email already registered')
            return render_template('auth/register.html')
        
        # Create user
        user_id = User.create_user(db, username, email, password, role='viewer')
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
def profile():
    """User profile page"""
    from utils.auth import login_required, get_current_user
    login_required()
    db = get_db()
    user = get_current_user(db)
    
    if not user:
        flash('User not found')
        return redirect(url_for('auth.login'))
    
    favorites = User.get_favorites(db, user['_id'])
    
    # For now, redirect to index - will create profile template later
    flash(f'Profile: {user["username"]} ({user["role"]})')
    return redirect(url_for('main.index'))

@auth_bp.route('/favorites', methods=['GET', 'POST', 'DELETE'])
def favorites():
    """Manage favorite publications"""
    from utils.auth import login_required, get_current_user
    from bson.objectid import ObjectId
    
    login_required()
    db = get_db()
    user = get_current_user(db)
    
    if request.method == 'POST':
        publication_id = request.form.get('publication_id')
        if publication_id:
            User.add_favorite(db, user['_id'], publication_id)
            flash('Added to favorites')
    
    elif request.method == 'DELETE':
        publication_id = request.json.get('publication_id')
        if publication_id:
            User.remove_favorite(db, user['_id'], publication_id)
            return {'status': 'success', 'message': 'Removed from favorites'}
    
    favorites = User.get_favorites(db, user['_id'])
    # For now, redirect to index - will create favorites template later
    flash(f'You have {len(favorites)} favorite publications')
    return redirect(url_for('main.index'))
