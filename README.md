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

## Installation & Setup

### 1. Install MySQL

**Windows:**  
Download MySQL Installer from the official website.

**MacOS:**  
```bash
brew install mysql
brew services start mysql
```
**MacOS:**  
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```
### 2. Create Database

**Log in to MySQL:**
```bash
mysql -u root -p
```
**Run the schema script:**
```bash
SOURCE /path/to/database/schema.sql;
```
**Run the seed script:**
```bash
SOURCE /path/to/database/seed.sql;
```
**Run triggers, procedures, and functions:**
```bash
SOURCE /path/to/database/triggers.sql;
SOURCE /path/to/database/procedures.sql;
SOURCE /path/to/database/functions.sql;
```

## Notes

- Ensure the MySQL server is running before starting the Flask app.  
- Database user must have privileges to create tables, insert, update, and execute procedures/triggers.  
- `docs/ER_diagrams/` contains ER diagrams for reference.  
- `tests/` folder can be used to write test scripts for backend functionality.
