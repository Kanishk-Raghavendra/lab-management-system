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

    # Initialize extensions with the app
    login_manager.init_app(app)
    bcrypt.init_app(app)

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
        exit(1) # Exit if we can't connect to the DB

    # --- Import and Register Blueprints ---
    # We import from our new 'app/routes' package
    from app.routes import main_routes_blueprint
    app.register_blueprint(main_routes_blueprint)

    return app