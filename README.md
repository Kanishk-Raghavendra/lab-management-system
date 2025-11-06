# Lab Management System

## Project Overview
The Lab Management System is designed to manage lab inventories, experiments, staff, students, and maintenance. It supports tracking equipment, consumables, orders from suppliers, and experiment management in chemistry and physics labs.

## Project Setup

### Frontend
- **Technologies:** HTML, CSS, JavaScript
- **Location:** 
  - Templates: `app/templates`
  - Static files: `app/static`

### Backend
- **Framework:** Flask
- **Main application file:** `run.py`
- **Models and routes:** `app/models` and `app/routes`

### Database
- **DBMS:** MySQL
- **Database scripts:** `database/` folder
  - `schema.sql` → Database schema
  - `seed.sql` → Initial data insertion
  - `queries.sql` → Example queries
  - `triggers.sql` → Database triggers
  - `procedures.sql` → Stored procedures
  - `functions.sql` → User-defined functions

## Folder Structure

```bash
app/
├── models/
├── routes/
├── static/
│ ├── css/
│ └── js/
└── templates/
database/
├── schema.sql
├── seed.sql
├── queries.sql
├── triggers.sql
├── procedures.sql
└── functions.sql
docs/
├── README.md
└── ER_diagrams/
tests/
run.py
requirements.txt
```

## Quick Start (One-Time Setup)

### Automated Setup (Recommended)

Run the one-time setup script that handles everything:

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the setup script
python scripts/setup_project.py
```

This script will:
1. ✅ Check and install all required dependencies
2. ✅ Create/update `.env` file with database configuration
3. ✅ Set up the database (schema, functions, procedures, triggers, seed data)
4. ✅ Verify and update password hashes
5. ✅ Run tests to ensure everything works

### Manual Setup

If you prefer manual setup:

#### 1. Install MySQL

**Windows:**  
Download MySQL Installer from the official website.

**macOS:**  
```bash
brew install mysql
brew services start mysql
```

**Linux:**  
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

#### 2. Install Python Dependencies

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

#### 3. Configure Environment

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=lab_management
SECRET_KEY=your_secret_key_here
```

#### 4. Set Up Database

**Option A: Using the setup script**
```bash
python scripts/setup_project.py
```

**Option B: Manual SQL execution**
```bash
# Log in to MySQL
mysql -u root -p

# Run SQL files in order
SOURCE database/schema.sql;
SOURCE database/functions.sql;
SOURCE database/procedures.sql;
SOURCE database/triggers.sql;
SOURCE database/seed.sql;
```

#### 5. Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Login Credentials

See `LOGIN_CREDENTIALS.md` for default login credentials.

**Default Staff Accounts:**
- Admin: `admin@lab.com` / `adminpass`
- Supervisor: `supervisor@lab.com` / `supervisor123`
- Assistant: `assistant@lab.com` / `assistant123`

**Default Student Accounts:**
- Student One: `student1@email.com` / `student1pass`
- Student Two: `student2@email.com` / `student2pass`
- Student Three: `student3@email.com` / `student3pass`
- Student Four: `student4@email.com` / `student4pass`

## Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## Project Structure

```
lab-management-system/
├── app/                    # Flask application
│   ├── models/            # Data models
│   ├── routes/             # Route handlers
│   ├── static/             # CSS, JS files
│   └── templates/          # HTML templates
├── database/               # SQL scripts
│   ├── schema.sql          # Database schema
│   ├── seed.sql            # Initial data
│   ├── functions.sql       # SQL functions
│   ├── procedures.sql      # Stored procedures
│   └── triggers.sql        # Database triggers
├── tests/                  # Test suite
├── scripts/                # Utility scripts
│   ├── setup_project.py    # One-time setup script
│   ├── apply_sql.py        # SQL file executor
│   └── fix_passwords.py    # Password hash updater
├── config.py               # Configuration
├── run.py                  # Application entry point
└── requirements.txt        # Python dependencies
```

## Notes

- ✅ Ensure the MySQL server is running before starting the Flask app
- ✅ Database user must have privileges to create tables, insert, update, and execute procedures/triggers
- ✅ The setup script only needs to be run once
- ✅ All password hashes are automatically verified and updated during setup
- ✅ `docs/` contains ER diagrams and documentation
- ✅ `tests/` folder contains comprehensive test suite
