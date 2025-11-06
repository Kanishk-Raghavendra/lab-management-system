import os
from datetime import timedelta
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
import mysql.connector

# Initialize extensions
login_manager = LoginManager()
bcrypt = Bcrypt()

# This tells flask-login which view (route) to redirect to
# if a user tries to access a protected page without being logged in.
login_manager.login_view = 'main_routes.login' # <-- Note: 'main_routes.' prefix
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Setup secret key for sessions
    if not app.config.get('SECRET_KEY'):
            # Production requires real secret key
            if app.config.get('ENV') == 'production':
                raise ValueError("No SECRET_KEY set in production!")
            else:
                # Only use dev key in development
                app.config['SECRET_KEY'] = os.urandom(24)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions with the app
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.refresh_view = 'main_routes.login'
    login_manager.needs_refresh_message = 'Please reauthenticate to access this page.'
    login_manager.needs_refresh_message_category = 'info'
    # Enhanced security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    # Session configuration
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=3600)  # 1 hour
    app.config['SESSION_COOKIE_SECURE'] = app.config.get('ENV') == 'production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    bcrypt.init_app(app)

    # Ensure session directory exists for test environment
    if app.config.get('TESTING') and app.config.get('SESSION_FILE_DIR'):
        os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

    # --- Database Connection Pool ---
    try:
        app.db_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="lab_pool",
            pool_size=10,
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME']
        )
        print("Database connection pool created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating database connection pool: {err}")
        if not app.config.get('TESTING'):
            exit(1) # Only exit if not in testing mode    # --- Import and Register Blueprints ---
    # We import from our new 'app/routes' package
    from app.routes import main_routes_blueprint
    app.register_blueprint(main_routes_blueprint)

    return app