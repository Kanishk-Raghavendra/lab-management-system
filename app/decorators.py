from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main_routes.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def supervisor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Admin can do everything a supervisor can do
        if not current_user.is_authenticated or \
           (not current_user.is_supervisor() and not current_user.is_admin()):

            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main_routes.dashboard'))
        return f(*args, **kwargs)
    return decorated_function