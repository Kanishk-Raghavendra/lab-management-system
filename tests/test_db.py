"""
Test database operations including:
- CRUD operations for inventory
- Stored procedures
- Triggers
- Functions
"""
import pytest
import mysql.connector
from pathlib import Path

def test_database_connection(db):
    """Test that we can connect to the test database."""
    cursor = db.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    assert result[0] == 1
    cursor.close()

def test_schema_creation(db):
    """Test that we can create the database schema."""
    cursor = db.cursor()
    
    # Read and execute schema.sql
    schema_path = Path(__file__).resolve().parent.parent / 'database' / 'schema.sql'
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    for statement in schema_sql.split(';'):
        if statement.strip():
            cursor.execute(statement)
    
    # Verify some key tables exist
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    assert 'Staff' in tables
    assert 'Student' in tables
    assert 'Lab' in tables
    assert 'Inventory' in tables
    
    cursor.close()

def test_stored_procedures(db):
    """Test that stored procedures work correctly."""
    cursor = db.cursor()
    
    # Read and execute procedures.sql
    procedures_path = Path(__file__).resolve().parent.parent / 'database' / 'procedures.sql'
    with open(procedures_path, 'r') as f:
        procedures_sql = f.read()
    
    # Split on DELIMITER and execute
    delimiter = ';'
    current_statement = []
    
    for line in procedures_sql.split('\n'):
        line = line.strip()
        if not line or line.startswith('--'):
            continue
            
        if line.upper().startswith('DELIMITER'):
            if current_statement:
                stmt = '\n'.join(current_statement)
                if stmt.strip():
                    cursor.execute(stmt)
            delimiter = line.split()[1]
            current_statement = []
            continue
            
        if line.endswith(delimiter):
            current_statement.append(line[:-len(delimiter)])
            stmt = '\n'.join(current_statement)
            if stmt.strip():
                cursor.execute(stmt)
            current_statement = []
        else:
            current_statement.append(line)
    
    # Test that we can call a stored procedure
    cursor.callproc('Get_Low_Stock_Items')
    for result in cursor.stored_results():
        assert isinstance(result.fetchall(), list)
    
    cursor.close()

def test_triggers(db):
    """Test that triggers work correctly."""
    cursor = db.cursor()
    
    # Read and execute triggers.sql
    triggers_path = Path(__file__).resolve().parent.parent / 'database' / 'triggers.sql'
    with open(triggers_path, 'r') as f:
        triggers_sql = f.read()
    
    # Execute triggers SQL (similar to procedures)
    delimiter = ';'
    current_statement = []
    
    for line in triggers_sql.split('\n'):
        line = line.strip()
        if not line or line.startswith('--'):
            continue
            
        if line.upper().startswith('DELIMITER'):
            if current_statement:
                stmt = '\n'.join(current_statement)
                if stmt.strip():
                    cursor.execute(stmt)
            delimiter = line.split()[1]
            current_statement = []
            continue
            
        if line.endswith(delimiter):
            current_statement.append(line[:-len(delimiter)])
            stmt = '\n'.join(current_statement)
            if stmt.strip():
                cursor.execute(stmt)
            current_statement = []
        else:
            current_statement.append(line)
    
    # Test insert trigger
    cursor.execute("""
        INSERT INTO Inventory(item_id, lab_id, quantity, status)
        VALUES (1, 1, 1, 'Available')
    """)
    
    # Verify low stock alert was created
    cursor.execute("SELECT COUNT(*) FROM Low_Stock_Alert WHERE inventory_id = LAST_INSERT_ID()")
    count = cursor.fetchone()[0]
    assert count == 1
    
    cursor.close()

def test_functions(db):
    """Test that user-defined functions work correctly."""
    cursor = db.cursor()
    
    # Read and execute functions.sql
    functions_path = Path(__file__).resolve().parent.parent / 'database' / 'functions.sql'
    with open(functions_path, 'r') as f:
        functions_sql = f.read()
    
    # Execute functions SQL (similar to procedures)
    delimiter = ';'
    current_statement = []
    
    for line in functions_sql.split('\n'):
        line = line.strip()
        if not line or line.startswith('--'):
            continue
            
        if line.upper().startswith('DELIMITER'):
            if current_statement:
                stmt = '\n'.join(current_statement)
                if stmt.strip():
                    cursor.execute(stmt)
            delimiter = line.split()[1]
            current_statement = []
            continue
            
        if line.endswith(delimiter):
            current_statement.append(line[:-len(delimiter)])
            stmt = '\n'.join(current_statement)
            if stmt.strip():
                cursor.execute(stmt)
            current_statement = []
        else:
            current_statement.append(line)
    
    # Test a function
    cursor.execute("SELECT Get_Total_Item_Quantity(1)")
    result = cursor.fetchone()[0]
    assert isinstance(result, int)
    
    cursor.close()