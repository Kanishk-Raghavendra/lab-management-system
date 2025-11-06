from flask_login import UserMixin
from app import login_manager
from flask import current_app

class User(UserMixin):
    """
    Custom User class for Flask-Login.
    Can represent EITHER a 'Staff' or 'Student' user.
    """
    def __init__(self, user_id, user_type, email, name, lab_id, role_name=None):
        self.id = user_id        # Will be staff_id OR student_id
        self.user_type = user_type  # 'Staff' or 'Student'
        self.email = email
        self.name = name
        self.lab_id = lab_id
        self.role_name = role_name  # Only for Staff members

    # --- Role Check Methods ---
    def is_admin(self):
        return self.user_type == 'Staff' and self.role_name == 'Admin'

    def is_supervisor(self):
        return self.user_type == 'Staff' and self.role_name == 'Supervisor'

    def is_assistant(self):
        return self.user_type == 'Staff' and self.role_name == 'Assistant'
    
    def is_student(self):
        return self.user_type == 'Student'


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login's callback function to load a user from the session.
    The user_id is now stored as a string: "staff_XX" or "student_XX".
    """
    try:
        # Verify the user_id format
        if not user_id or '_' not in user_id:
            return None

        user_type, user_id_int = user_id.split('_')
        user_id_int = int(user_id_int)

        # Verify user type is valid
        if user_type not in ['staff', 'student']:
            return None
        
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)
        
        user_obj = None

        if user_type == 'staff':
            query = """
                SELECT Staff.*, Roles.role_name 
                FROM Staff 
                JOIN Roles ON Staff.role_id = Roles.role_id 
                WHERE Staff.staff_id = %s
            """
            cursor.execute(query, (user_id_int,))
            user_data = cursor.fetchone()
            if user_data:
                user_obj = User(
                    user_id=f"staff_{user_data['staff_id']}",
                    user_type='Staff',
                    email=user_data['email'],
                    name=user_data['name'],
                    role_name=user_data['role_name'],
                    lab_id=user_data['lab_id']
                )
        
        elif user_type == 'student':
            query = "SELECT * FROM Student WHERE student_id = %s"
            cursor.execute(query, (user_id_int,))
            user_data = cursor.fetchone()
            if user_data:
                user_obj = User(
                    user_id=f"student_{user_data['student_id']}",
                    user_type='Student',
                    email=user_data['email'],
                    name=user_data['name'],
                    lab_id=user_data['lab_id']
                )
        
        cursor.close()
        db_conn.close()

        # If user was not found in database, return None to invalidate session
        if not user_obj:
            return None

        return user_obj
        
    except Exception as e:
        print(f"Error loading user: {e}")
        return None