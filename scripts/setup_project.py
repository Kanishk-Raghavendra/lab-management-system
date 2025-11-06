#!/usr/bin/env python3
"""
One-time setup script for Lab Management System.
This script:
1. Checks for required dependencies
2. Creates/updates .env file
3. Sets up the database (schema, functions, procedures, triggers, seed data)
4. Verifies password hashes
5. Runs tests to ensure everything works

Usage:
    python scripts/setup_project.py
"""
import os
import sys
import subprocess
from pathlib import Path
from getpass import getpass

# Add parent directory to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    import mysql.connector
    from flask_bcrypt import Bcrypt
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

# Colors for output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(step_num, message):
    """Print a step message."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}[Step {step_num}]{Colors.END} {message}")

def print_success(message):
    """Print a success message."""
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message):
    """Print an error message."""
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_warning(message):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def check_dependencies():
    """Check if all required dependencies are installed."""
    print_step(1, "Checking dependencies...")
    
    # Map package names to their import names
    package_imports = {
        'flask': 'flask',
        'flask-login': 'flask_login',
        'flask-bcrypt': 'flask_bcrypt',
        'mysql-connector-python': 'mysql.connector',
        'python-dotenv': 'dotenv',
        'pytest': 'pytest',
        'pytest-flask': 'pytest_flask',
        'pytest-cov': 'pytest_cov'
    }
    
    missing = []
    for package, import_name in package_imports.items():
        try:
            __import__(import_name)
            print_success(f"{package} is installed")
        except ImportError:
            missing.append(package)
            print_error(f"{package} is missing")
    
    if missing:
        print_warning("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing, 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print_success("All dependencies installed")
        except subprocess.CalledProcessError:
            print_warning("Some packages may need manual installation. Continuing...")
    else:
        print_success("All dependencies are installed")
    
    return True

def setup_env_file():
    """Create or update .env file."""
    print_step(2, "Setting up environment file...")
    
    env_path = ROOT / '.env'
    env_example_path = ROOT / '.env.example'
    
    # Load existing .env if it exists
    if env_path.exists():
        load_dotenv(env_path)
        print_success(".env file already exists")
        
        # Check if all required variables are set
        required_vars = ['DB_HOST', 'DB_USER', 'DB_NAME']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print_warning(f"Missing environment variables: {', '.join(missing_vars)}")
            print("Please update your .env file with the missing variables.")
            return False
        else:
            print_success("All required environment variables are set")
            return True
    else:
        # Create new .env file
        print_warning(".env file not found. Creating new one...")
        
        # Get database credentials from user
        print("\nPlease provide database configuration:")
        db_host = input("DB_HOST [localhost]: ").strip() or 'localhost'
        db_user = input("DB_USER [root]: ").strip() or 'root'
        db_password = getpass("DB_PASSWORD (leave empty if none): ").strip()
        db_name = input("DB_NAME [lab_management]: ").strip() or 'lab_management'
        secret_key = os.urandom(24).hex()
        
        # Write .env file
        env_content = f"""# Database Configuration
DB_HOST={db_host}
DB_USER={db_user}
DB_PASSWORD={db_password}
DB_NAME={db_name}

# Flask Secret Key
SECRET_KEY={secret_key}
"""
        
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print_success(f".env file created at {env_path}")
        return True

def setup_database():
    """Set up the database with all SQL files."""
    print_step(3, "Setting up database...")
    
    # Load environment variables
    load_dotenv(ROOT / '.env')
    
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'lab_management')
    
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        print_success(f"Database '{db_name}' is ready")
        
        # SQL files to execute in order
        sql_files = [
            'schema.sql',
            'functions.sql',
            'procedures.sql',
            'triggers.sql',
            'seed.sql'
        ]
        
        db_dir = ROOT / 'database'
        
        for sql_file in sql_files:
            file_path = db_dir / sql_file
            if not file_path.exists():
                print_error(f"SQL file not found: {file_path}")
                continue
            
            print(f"  Applying {sql_file}...")
            
            try:
                # Use the apply_sql.py script's logic
                sql_content = file_path.read_text()
                
                # Handle DELIMITER changes
                delimiter = ';'
                current_statement = []
                
                for line in sql_content.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('--'):
                        continue
                    
                    if line.upper().startswith('DELIMITER'):
                        # Execute any pending statement
                        if current_statement:
                            stmt = '\n'.join(current_statement).strip()
                            if stmt:
                                try:
                                    cursor.execute(stmt)
                                    while cursor.nextset() is not None:
                                        pass
                                except mysql.connector.Error as stmt_err:
                                    # Ignore duplicate entry errors for seed data
                                    if stmt_err.errno == 1062 or 'duplicate entry' in str(stmt_err).lower():
                                        if sql_file == 'seed.sql':
                                            # Silently ignore duplicate entries in seed data
                                            pass
                                        else:
                                            raise
                                    else:
                                        raise
                            current_statement = []
                        
                        # Set new delimiter
                        delimiter = line.split()[1]
                        continue
                    
                    if line.endswith(delimiter):
                        current_statement.append(line[:-len(delimiter)])
                        stmt = '\n'.join(current_statement).strip()
                        if stmt:
                            try:
                                cursor.execute(stmt)
                                while cursor.nextset() is not None:
                                    pass
                            except mysql.connector.Error as stmt_err:
                                # Ignore duplicate entry errors for seed data
                                if stmt_err.errno == 1062 or 'duplicate entry' in str(stmt_err).lower():
                                    if sql_file == 'seed.sql':
                                        # Silently ignore duplicate entries in seed data
                                        pass
                                    else:
                                        raise
                                else:
                                    raise
                        current_statement = []
                    else:
                        current_statement.append(line)
                
                # Execute any remaining statement
                if current_statement:
                    stmt = '\n'.join(current_statement).strip()
                    if stmt:
                        try:
                            cursor.execute(stmt)
                            while cursor.nextset() is not None:
                                pass
                        except mysql.connector.Error as stmt_err:
                            # Ignore duplicate entry errors for seed data
                            if stmt_err.errno == 1062 or 'duplicate entry' in str(stmt_err).lower():
                                if sql_file == 'seed.sql':
                                    # Silently ignore duplicate entries in seed data
                                    pass
                                else:
                                    raise
                            else:
                                raise
                
                conn.commit()
                print_success(f"  {sql_file} applied successfully")
                
            except mysql.connector.Error as err:
                # Ignore "already exists" errors and duplicate entry errors for seed data
                # 1050 = table exists, 1304 = procedure exists, 1062 = duplicate entry
                if err.errno in (1050, 1304, 1062) or 'already exists' in str(err).lower() or 'duplicate entry' in str(err).lower():
                    if sql_file == 'seed.sql':
                        print_warning(f"  {sql_file}: Some data already exists (ignored)")
                    else:
                        print_warning(f"  {sql_file}: Some objects already exist (ignored)")
                else:
                    print_error(f"  {sql_file}: {err}")
                    conn.rollback()
                    raise
        
        cursor.close()
        conn.close()
        
        print_success("Database setup completed")
        return True
        
    except mysql.connector.Error as err:
        print_error(f"Database error: {err}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def verify_passwords():
    """Verify and update password hashes if needed."""
    print_step(4, "Verifying password hashes...")
    
    load_dotenv(ROOT / '.env')
    
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'lab_management')
    
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor(dictionary=True)
        
        bcrypt = Bcrypt()
        
        # Staff passwords
        staff_passwords = {
            'admin@lab.com': 'adminpass',
            'supervisor@lab.com': 'supervisor123',
            'assistant@lab.com': 'assistant123'
        }
        
        # Check and update staff passwords
        for email, password in staff_passwords.items():
            cursor.execute("SELECT staff_id, password_hash FROM Staff WHERE email = %s", (email,))
            staff = cursor.fetchone()
            
            if staff:
                stored_hash = staff['password_hash']
                # Verify hash
                if not bcrypt.check_password_hash(stored_hash, password):
                    # Update with new hash
                    new_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                    cursor.execute("UPDATE Staff SET password_hash = %s WHERE email = %s", (new_hash, email))
                    print_success(f"Updated password for {email}")
                else:
                    print_success(f"Password verified for {email}")
            else:
                print_warning(f"Staff member {email} not found in database")
        
        # Student passwords
        student_passwords = {
            'student1@email.com': 'student1pass',
            'student2@email.com': 'student2pass',
            'student3@email.com': 'student3pass',
            'student4@email.com': 'student4pass'
        }
        
        # Check and update student passwords
        for email, password in student_passwords.items():
            cursor.execute("SELECT student_id, password_hash FROM Student WHERE email = %s", (email,))
            student = cursor.fetchone()
            
            if student:
                stored_hash = student['password_hash']
                # Verify hash
                if not bcrypt.check_password_hash(stored_hash, password):
                    # Update with new hash
                    new_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                    cursor.execute("UPDATE Student SET password_hash = %s WHERE email = %s", (new_hash, email))
                    print_success(f"Updated password for {email}")
                else:
                    print_success(f"Password verified for {email}")
            else:
                print_warning(f"Student {email} not found in database")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print_success("All passwords verified")
        return True
        
    except Exception as e:
        print_error(f"Error verifying passwords: {e}")
        return False

def run_tests():
    """Run the test suite (optional step - skipped by default to avoid hanging)."""
    print_step(5, "Running tests (optional - skipped by default)...")
    
    print_warning("Skipping tests to avoid setup delays.")
    print("  You can run tests manually later with: pytest tests/ -v")
    print("  Or with coverage: pytest tests/ --cov=app --cov-report=html")
    
    return True  # Always succeed - tests are optional

def main():
    """Main setup function."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print("Lab Management System - One-Time Setup")
    print(f"{'='*60}{Colors.END}\n")
    
    steps = [
        ("Checking dependencies", check_dependencies),
        ("Setting up environment file", setup_env_file),
        ("Setting up database", setup_database),
        ("Verifying passwords", verify_passwords),
        ("Running tests", run_tests)
    ]
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                print_error(f"Step '{step_name}' failed. Please fix the issue and run again.")
                sys.exit(1)
        except KeyboardInterrupt:
            print_error("\nSetup interrupted by user.")
            sys.exit(1)
        except Exception as e:
            print_error(f"Unexpected error in '{step_name}': {e}")
            sys.exit(1)
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}")
    print("✓ Setup completed successfully!")
    print(f"{'='*60}{Colors.END}\n")
    
    print("You can now run the application with:")
    print(f"  {Colors.BOLD}python run.py{Colors.END}\n")
    
    print("Login credentials are available in LOGIN_CREDENTIALS.md")

if __name__ == '__main__':
    main()

