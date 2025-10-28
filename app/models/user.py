from flask_login import UserMixin
from app import login_manager  # Import from the main __init__.py
from flask import current_app

class User(UserMixin):
    """
    Custom User class for Flask-Login that maps to our 'Staff' table.
    """
    def __init__(self, staff_id, email, name, role_name, lab_id):
        self.id = staff_id
        self.email = email
        self.name = name
        self.role_name = role_name
        self.lab_id = lab_id

    def is_admin(self):
        return self.role_name == 'Admin'

    def is_supervisor(self):
        return self.role_name == 'Supervisor'

    def is_assistant(self):
        return self.role_name == 'Assistant'

@login_manager.user_loader
def load_user(staff_id):
    """
    Flask-Login's callback function to load a user from the session.
    """
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True) # dictionary=True is key!
        
        query = """
            SELECT Staff.*, Roles.role_name 
            FROM Staff 
            JOIN Roles ON Staff.role_id = Roles.role_id 
            WHERE Staff.staff_id = %s
        """
        cursor.execute(query, (staff_id,))
        user_data = cursor.fetchone()
        
        cursor.close()
        db_conn.close()
        
        if user_data:
            return User(
                staff_id=user_data['staff_id'],
                email=user_data['email'],
                name=user_data['name'],
                role_name=user_data['role_name'],
                lab_id=user_data['lab_id']
            )
        return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None