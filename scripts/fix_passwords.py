#!/usr/bin/env python3
"""
Script to fix password hashes in the database.
This updates the existing password hashes with correct bcrypt hashes.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
import mysql.connector
from flask_bcrypt import Bcrypt

# Load environment variables
load_dotenv()

# Get database credentials
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'lab_management')

# Initialize bcrypt
bcrypt = Bcrypt()

# Password mappings
STAFF_PASSWORDS = {
    'admin@lab.com': 'adminpass',
    'supervisor@lab.com': 'supervisor123',
    'assistant@lab.com': 'assistant123'
}

STUDENT_PASSWORDS = {
    'student1@email.com': 'student1pass',
    'student2@email.com': 'student2pass',
    'student3@email.com': 'student3pass',
    'student4@email.com': 'student4pass'
}

def update_passwords():
    """Update password hashes in the database."""
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        
        print("Connected to database successfully!")
        print("=" * 60)
        
        # Update Staff passwords
        print("\nUpdating Staff passwords...")
        for email, password in STAFF_PASSWORDS.items():
            new_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute(
                "UPDATE Staff SET password_hash = %s WHERE email = %s",
                (new_hash, email)
            )
            if cursor.rowcount > 0:
                print(f"✓ Updated password for {email}")
            else:
                print(f"✗ Staff member {email} not found")
        
        # Update Student passwords
        print("\nUpdating Student passwords...")
        for email, password in STUDENT_PASSWORDS.items():
            new_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute(
                "UPDATE Student SET password_hash = %s WHERE email = %s",
                (new_hash, email)
            )
            if cursor.rowcount > 0:
                print(f"✓ Updated password for {email}")
            else:
                print(f"✗ Student {email} not found")
        
        # Commit changes
        conn.commit()
        print("\n" + "=" * 60)
        print("✓ All passwords updated successfully!")
        print("\nYou can now login with:")
        print("\nStaff accounts:")
        for email, password in STAFF_PASSWORDS.items():
            print(f"  Email: {email}, Password: {password}")
        print("\nStudent accounts:")
        for email, password in STUDENT_PASSWORDS.items():
            print(f"  Email: {email}, Password: {password}")
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    update_passwords()

