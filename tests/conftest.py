import os
import sys
import pytest
import tempfile
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the app
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from config import TestConfig

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Load test environment variables from the tests directory
    test_env_path = Path(__file__).parent / '.env.test'
    load_dotenv(test_env_path)

    # Ensure the test database is being used
    os.environ['DB_NAME'] = 'lab_management_test'
    
    # Create the Flask app with test config
    app = create_app(TestConfig)
    
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def db():
    """Create a new test database and return the connection."""
    # Get test database configuration
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'lab_management_test')
    }
        
    # Create a connection without database specified
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password']
    )
    cursor = conn.cursor()
    
    # Drop and recreate test database
    try:
        # Force drop all connections to the test database first
        cursor.execute(f"SELECT CONCAT('KILL ', id, ';') FROM INFORMATION_SCHEMA.PROCESSLIST WHERE DB = '{db_config['database']}' AND User <> 'root'")
        kill_statements = cursor.fetchall()
        for (kill_statement,) in kill_statements:
            try:
                cursor.execute(kill_statement)
            except:
                pass
        
        cursor.execute(f"DROP DATABASE IF EXISTS {db_config['database']}")
        cursor.execute(f"CREATE DATABASE {db_config['database']}")
        cursor.execute(f"USE {db_config['database']}")
    finally:
        cursor.close()
        conn.commit()
        conn.close()
    
    # Create new connection for schema setup
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Get base directory path
    base_dir = Path(__file__).resolve().parent.parent
    
    # Drop all stored procedures, functions, and triggers
    cursor.execute("SHOW PROCEDURE STATUS WHERE Db = %s", (db_config['database'],))
    for (proc,) in cursor.fetchall():
        cursor.execute(f"DROP PROCEDURE IF EXISTS {proc[0]}")
        
    cursor.execute("SHOW FUNCTION STATUS WHERE Db = %s", (db_config['database'],))
    for (func,) in cursor.fetchall():
        cursor.execute(f"DROP FUNCTION IF EXISTS {func[0]}")
        
    cursor.execute(f"SHOW TRIGGERS FROM {db_config['database']}")
    for (trig,) in cursor.fetchall():
        cursor.execute(f"DROP TRIGGER IF EXISTS {trig[0]}")
        
    conn.commit()
    
    # Function to execute SQL file
    def execute_sql_file(file_path, delimiter=';'):
        with open(file_path, 'r') as f:
            sql = f.read()
            
        # Split by delimiter while respecting DELIMITER changes
        statements = []
        current_delimiter = delimiter
        current_statement = []
        
        for line in sql.split('\n'):
            line = line.strip()
            if not line or line.startswith('--'):
                continue
                
            if line.upper().startswith('DELIMITER'):
                if current_statement:
                    statements.append(('\n'.join(current_statement), current_delimiter))
                    current_statement = []
                current_delimiter = line.split()[1]
                continue
                
            if line.endswith(current_delimiter):
                current_statement.append(line[:-len(current_delimiter)])
                statements.append(('\n'.join(current_statement), current_delimiter))
                current_statement = []
            else:
                current_statement.append(line)
                
        if current_statement:
            statements.append(('\n'.join(current_statement), current_delimiter))
            
        # Execute statements (be idempotent: ignore 'already exists' errors)
        for statement, delim in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                    conn.commit()
                except Exception as e:
                    # MySQL error codes: 1050 = table exists, 1304 = procedure exists, 1317/1360 may appear
                    err_no = getattr(e, 'errno', None)
                    msg = str(e)
                    if err_no in (1050, 1304) or 'already exists' in msg.lower():
                        print(f"Ignored existing object error: {e}\n{statement}")
                        # continue to next statement
                        continue
                    print(f"Error executing statement: {e}\n{statement}")
                    raise

    # Load files in order
    files = [
        ('schema.sql', ';'),
        ('procedures.sql', '//'),
        ('functions.sql', '//'),
        ('triggers.sql', '//'),
        ('seed.sql', ';')
    ]
    # Always attempt to (re)create schema, procedures, functions, triggers and seed data.
    for filename, delimiter in files:
        file_path = base_dir / 'database' / filename
        execute_sql_file(file_path, delimiter)
    
    yield conn
    
    # Cleanup after tests
    conn.close()
    cleanup_conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password']
    )
    cleanup_cursor = cleanup_conn.cursor()
    cleanup_cursor.execute(f"DROP DATABASE IF EXISTS {db_config['database']}")
    cleanup_cursor.close()
    cleanup_conn.close()

@pytest.fixture
def auth(client):
    """Authentication helper class for tests."""
    class Auth:
        def login(self, email='admin@lab.com', password='adminpass'):
            with client.session_transaction() as session:
                session.clear()
            return client.post('/login', data={
                'email': email, 
                'password': password,
                'remember': True
            }, follow_redirects=True)
            
        def logout(self):
            return client.get('/logout', follow_redirects=True)
    
    return Auth()