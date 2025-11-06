#!/usr/bin/env python3
"""
Apply SQL files in the database/ directory to the configured MySQL instance.
Reads DB credentials from environment (via python-dotenv if .env present).

Usage:
  python3 scripts/apply_sql.py [file1.sql file2.sql ...]
  If no files specified, applies: schema.sql, functions.sql, procedures.sql, triggers.sql, seed.sql
"""
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    import mysql.connector
except Exception as e:
    print("Missing dependency:", e)
    print("Please install requirements: pip3 install mysql-connector-python python-dotenv")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
DB_DIR = ROOT / 'database'

# Load .env if present
load_dotenv(dotenv_path=ROOT / '.env')

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')

if not all([DB_HOST, DB_USER, DB_NAME]):
    print('Missing DB configuration. Ensure DB_HOST, DB_USER and DB_NAME are set in environment or .env.')
    sys.exit(1)

files_order = [
    'schema.sql',
    'functions.sql',
    'procedures.sql',
    'triggers.sql',
    'seed.sql'
]

def execute_sql(cursor, sql):
    """Execute SQL statements with proper handling of results and delimiters."""
    # First handle any USE statements at the start
    lines = sql.split('\n')
    for i, line in enumerate(lines):
        if line.strip().lower().startswith('use'):
            cursor.execute(line.strip())
            lines = lines[i+1:]  # Remove processed lines
            break

    # Join remaining lines back
    sql = '\n'.join(lines)
    
    # Now split and execute statements based on delimiters
    delimiter = ';'
    current_statement = []
    
    for line in sql.split('\n'):
        line = line.strip()
        if not line or line.startswith('--'):
            continue
            
        if line.upper().startswith('DELIMITER'):
            # Execute any pending statement with previous delimiter
            if current_statement:
                stmt = '\n'.join(current_statement).strip()
                if stmt:
                    cursor.execute(stmt)
                    while cursor.nextset() is not None:
                        pass  # Consume any additional result sets
                current_statement = []
                
            # Set new delimiter
            delimiter = line.split()[1]
            continue
            
        if line.endswith(delimiter):
            current_statement.append(line[:-len(delimiter)])
            stmt = '\n'.join(current_statement).strip()
            if stmt:
                cursor.execute(stmt)
                while cursor.nextset() is not None:
                    pass  # Consume any additional result sets
            current_statement = []
        else:
            current_statement.append(line)
    
    # Execute any remaining statement
    if current_statement:
        stmt = '\n'.join(current_statement).strip()
        if stmt:
            cursor.execute(stmt)
            while cursor.nextset() is not None:
                pass  # Consume any additional result sets

def main():
    # Connect to MySQL server without database
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD or '',
        )
    except Exception as e:
        print('Error connecting to MySQL server:', e)
        sys.exit(1)

    cursor = conn.cursor()

    # Create database if it doesn't exist and use it
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
    except mysql.connector.Error as err:
        print(f"Error creating/using database {DB_NAME}:", err)
        cursor.close()
        conn.close()
        sys.exit(1)

    # Determine files to apply
    if len(sys.argv) > 1:
        files_to_apply = [Path(f) for f in sys.argv[1:]]
    else:
        files_to_apply = [DB_DIR / fname for fname in files_order]

    # Process each SQL file
    for path in files_to_apply:
        if not path.exists():
            print(f"Skipping {path}: file not found")
            continue

        print(f"Applying {path.name}...")
        sql = path.read_text()
        
        try:
            execute_sql(cursor, sql)
            conn.commit()
            print(f"Applied {path.name} successfully.")
        except mysql.connector.Error as err:
            print(f"Error applying {path.name}: {err}")
            conn.rollback()
            cursor.close()
            conn.close()
            sys.exit(1)

    cursor.close()
    conn.close()
    print('All done.')

if __name__ == '__main__':
    main()
