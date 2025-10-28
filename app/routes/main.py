from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import bcrypt
from app.models.user import User  # <-- Import User from app.models.user
from app.decorators import admin_required, supervisor_required
from . import main_routes_blueprint # <-- Import the blueprint from this package

# We use the blueprint to define routes, not 'main'
@main_routes_blueprint.route('/')
@main_routes_blueprint.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard, protected by login."""
    # We must use 'main_routes.dashboard' in url_for
    return render_template('dashboard.html', title='Dashboard')

@main_routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if current_user.is_authenticated:
        return redirect(url_for('main_routes.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            db_conn = current_app.db_pool.get_connection()
            cursor = db_conn.cursor(dictionary=True)
            
            query = """
                SELECT Staff.*, Roles.role_name 
                FROM Staff 
                JOIN Roles ON Staff.role_id = Roles.role_id 
                WHERE Staff.email = %s
            """
            cursor.execute(query, (email,))
            user_data = cursor.fetchone()
            
            cursor.close()
            db_conn.close()
            
            # !! REMEMBER: This checks plaintext.
            # Change to bcrypt.check_password_hash for production
            if user_data and user_data['password_hash'] == password:
                
                user = User(
                    staff_id=user_data['staff_id'],
                    email=user_data['email'],
                    name=user_data['name'],
                    role_name=user_data['role_name'],
                    lab_id=user_data['lab_id']
                )
                
                login_user(user, remember=request.form.get('remember'))
                flash(f'Welcome back, {user.name}!', 'success')
                
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main_routes.dashboard'))
            else:
                flash('Login Unsuccessful. Please check email and password.', 'danger')
                
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')

    return render_template('login.html', title='Login')


@main_routes_blueprint.route('/logout')
def logout():
    """Logs the user out."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main_routes.login'))

# --- Example Protected Routes ---

@main_routes_blueprint.route('/admin_only')
@login_required
@admin_required
def admin_page():
    return "<h1>Admin Page</h1><p>Only admins can see this.</p>"

@main_routes_blueprint.route('/supervisor_stuff')
@login_required
@supervisor_required
def supervisor_page():
    return "<h1>Supervisor Page</h1><p>Supervisors and Admins can see this.</p>"