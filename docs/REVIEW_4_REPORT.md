# Lab Management System
## Final Project Report - Review 4

**Course:** DATABASE MANAGEMENT SYSTEM UE23CS351A  
**Experiential Learning:** Level 2 (Orange problem) - 10 Marks  
**Project Title:** Lab Management System  
**Team Members:** [Add your team member names here]  
**Date:** [Add submission date]

---

## Table of Contents

1. [Cover Page](#1-cover-page)
2. [Abstract](#2-abstract)
3. [User Requirement Specification](#3-user-requirement-specification)
4. [Software/Tools/Programming Languages](#4-softwaretoolsprogramming-languages-used)
5. [ER Diagram](#5-er-diagram)
6. [Relational Schema](#6-relational-schema)
7. [DDL Commands](#7-ddl-commands)
8. [CRUD Operations](#8-crud-operations)
9. [Application Features and Screenshots](#9-application-features-and-screenshots)
10. [Triggers, Procedures, Functions, Queries](#10-triggers-procedures-functions-nested-queries-joins-aggregate-queries)
11. [Code Snippets](#11-code-snippets-for-invoking-proceduresfunctions-triggers)
12. [SQL Files](#12-sql-queries-in-sql-file-format)
13. [GitHub Repository](#13-github-repository-link)

---

## 1. Cover Page

### Lab Management System

**Team Details:**
- Team Member 1: [Name] - [USN]
- Team Member 2: [Name] - [USN]

**Course:** DATABASE MANAGEMENT SYSTEM UE23CS351A  
**Institution:** PES University  
**Academic Year:** 2024-2025  
**Submission Date:** [Date]

---

## 2. Abstract

The Lab Management System is a comprehensive web-based application designed to manage laboratory operations in educational institutions. The system facilitates efficient tracking and management of laboratory inventory, experiments, staff, students, suppliers, and maintenance activities. Built using Flask (Python) for the backend and MySQL for database management, the application provides role-based access control with three distinct user roles: Admin, Supervisor, and Assistant. Students can also access the system to view their assigned labs and experiments.

The system addresses critical needs in laboratory management including inventory tracking, automatic stock alerts, experiment management, order processing, and maintenance logging. It implements complex database operations including stored procedures, triggers, functions, and various types of SQL queries (nested queries, joins, aggregate queries) to ensure data integrity and automate business logic.

---

## 3. User Requirement Specification

### 3.1 Purpose of the Project

The Lab Management System is designed to digitize and streamline laboratory management operations in educational institutions. The system aims to eliminate manual record-keeping, reduce errors, improve inventory visibility, and automate critical processes such as stock alerts, order processing, and maintenance tracking. By providing a centralized platform for managing labs, the system enables efficient resource allocation, better tracking of experiments, and improved coordination between staff and students.

### 3.2 Scope of the Project

The Lab Management System covers the complete lifecycle of laboratory management including:
- **Inventory Management:** Track equipment and consumables across multiple labs with real-time quantity updates
- **Experiment Management:** Assign and track experiments conducted in labs with inventory usage tracking
- **Order Management:** Process orders from suppliers and automatically update inventory upon receipt
- **Maintenance Management:** Log and track maintenance activities for equipment
- **User Management:** Manage staff (Admin, Supervisor, Assistant) and students with role-based access
- **Supplier Management:** Maintain supplier information and track which suppliers provide which items
- **Automated Alerts:** Low stock alerts triggered automatically when inventory falls below minimum levels

The system is designed for use in chemistry and physics laboratories, supporting multiple labs simultaneously with role-based access control ensuring data security and proper authorization.

### 3.3 Detailed Description

The Lab Management System manages laboratory operations for educational institutions. The system handles multiple laboratories (Chemistry and Physics labs), each containing various inventory items (equipment and consumables). Staff members (Admins, Supervisors, and Assistants) are assigned to labs and can manage experiments, inventory, and maintenance activities.

**Key Entities:**
- **Labs:** Physical laboratory spaces (e.g., Chem Lab 1, Physics Lab 2) with specific locations
- **Items:** Master catalog of equipment (microscopes, Bunsen burners) and consumables (test tubes, beakers)
- **Inventory:** Actual stock of items in each lab with quantities and status (Available, In Use, Maintenance)
- **Staff:** Lab personnel with different roles and permissions
- **Students:** Assigned to labs and supervised by staff members
- **Experiments:** Activities conducted in labs using inventory items
- **Orders:** Purchase orders from suppliers that automatically update inventory when received
- **Maintenance Logs:** Records of equipment maintenance activities
- **Suppliers:** External vendors providing items to labs

**Workflow:**
1. Admins create master items, labs, staff accounts, and supplier records
2. Supervisors manage inventory, create experiments, and process orders
3. When experiments use inventory, quantities are automatically reduced
4. Orders from suppliers automatically update inventory when marked as "Received"
5. Maintenance logs track equipment servicing and automatically update inventory status
6. Low stock alerts are generated automatically when inventory falls below minimum levels
7. Students can view their assigned labs and experiments

### 3.4 Functional Requirements

#### System Functionality 1: User Authentication and Role-Based Access Control
**Description:** Secure login system supporting Staff (Admin, Supervisor, Assistant) and Students with role-based permissions. Admins have full access, Supervisors manage their assigned labs, Assistants support supervisors, and Students can only view their assigned lab information.

#### System Functionality 2: Inventory Management
**Description:** Complete CRUD operations for inventory items across labs. Track quantities, status (Available/In Use/Maintenance), and automatically update when items are used in experiments or received from orders.

#### System Functionality 3: Experiment Management
**Description:** Create, view, and manage experiments. Assign experiments to labs and staff, track inventory usage, and automatically reduce inventory quantities when items are used.

#### System Functionality 4: Order Management
**Description:** Create orders from suppliers, add items to orders, and process order receipt. Automatically update inventory quantities when orders are marked as "Received" using triggers.

#### System Functionality 5: Maintenance Management
**Description:** Log maintenance activities for equipment, track maintenance status (Pending/Completed), and automatically update inventory status to "Maintenance" when logged and back to "Available" when completed.

#### System Functionality 6: Staff and Student Management
**Description:** Admin functionality to create, update, and manage staff accounts and student records. Assign students to labs and supervisors, manage roles and permissions.

#### System Functionality 7: Supplier Management
**Description:** Maintain supplier information, assign items to suppliers, and view supplier-item relationships. Track which suppliers provide which items.

#### System Functionality 8: Low Stock Alerts
**Description:** Automatic generation of low stock alerts when inventory quantities fall below minimum stock levels. View alerts in a dedicated dashboard section.

#### System Functionality 9: Dashboard and Reporting
**Description:** Role-specific dashboards showing relevant statistics, pending maintenance, low stock items, and recent activities. Different views for Admin, Supervisor, and Students.

#### System Functionality 10: Item Master Management
**Description:** Admin functionality to manage master item catalog including equipment and consumables. Set minimum stock levels, prices, and descriptions.

---

## 4. Software/Tools/Programming Languages Used

### Backend Technologies
- **Python 3.12** - Programming language
- **Flask 3.1.2** - Web framework
- **Flask-Login 0.6.3** - User session management
- **Flask-Bcrypt 1.0.1** - Password hashing
- **MySQL Connector Python 9.5.0** - Database connectivity

### Database
- **MySQL 8.0+** - Relational Database Management System

### Frontend Technologies
- **HTML5** - Markup language
- **CSS3** - Styling (including dark theme support)
- **JavaScript** - Client-side interactivity
- **Jinja2** - Template engine

### Development Tools
- **Git** - Version control
- **GitHub** - Repository hosting
- **VS Code / PyCharm** - IDE
- **pytest** - Testing framework
- **python-dotenv** - Environment variable management

### Additional Libraries
- **pytest-flask** - Flask testing utilities
- **pytest-cov** - Code coverage

---

## 5. ER Diagram

The ER Diagram is available in the `docs/` folder as `ER_Diagram.png`.

**Key Relationships:**
- Staff → Roles (Many-to-One)
- Staff → Lab (Many-to-One)
- Lab → Inventory (One-to-Many)
- Item → Inventory (One-to-Many)
- Staff → Experiment (One-to-Many)
- Experiment → Inventory (Many-to-Many via Experiment_Inventory)
- Student → Lab (Many-to-One)
- Student → Staff (Many-to-One, supervisor relationship)
- Inventory → Maintenance_Log (One-to-Many)
- Supplier → Item (Many-to-Many via Supplier_Item)
- Supplier → Order (One-to-Many)
- Order → Item (Many-to-Many via Order_Item)

**See:** `docs/ER_Diagram.png` for visual representation.

---

## 6. Relational Schema

### Tables and Relationships

1. **Roles** (role_id PK, role_name, description)
2. **Supplier** (supplier_id PK, name, contact_no, email, address)
3. **Item** (item_id PK, item_name, item_type, description, unit_price, min_stock_level)
4. **Lab** (lab_id PK, lab_name, lab_type, location)
5. **Staff** (staff_id PK, name, role_id FK→Roles, contact_no, email, lab_id FK→Lab, password_hash)
6. **Inventory** (inventory_id PK, item_id FK→Item, lab_id FK→Lab, quantity, status, last_updated)
   - UNIQUE KEY (item_id, lab_id)
7. **Order** (order_id PK, supplier_id FK→Supplier, lab_id FK→Lab, order_date, delivery_date, total_cost, status)
8. **Order_Item** (order_id FK→Order, item_id FK→Item, quantity_ordered, cost_per_unit)
   - PRIMARY KEY (order_id, item_id)
9. **Experiment** (experiment_id PK, experiment_name, lab_id FK→Lab, staff_id FK→Staff, description, experiment_date)
10. **Student** (student_id PK, name, email, password_hash, lab_id FK→Lab, assigned_staff_id FK→Staff)
11. **Experiment_Inventory** (experiment_id FK→Experiment, inventory_id FK→Inventory, quantity_used)
    - PRIMARY KEY (experiment_id, inventory_id)
12. **Maintenance_Log** (maintenance_id PK, inventory_id FK→Inventory, staff_id FK→Staff, log_date, description, status)
13. **Supplier_Item** (supplier_id FK→Supplier, item_id FK→Item)
    - PRIMARY KEY (supplier_id, item_id)
14. **Low_Stock_Alert** (alert_id PK, item_id FK→Item, inventory_id FK→Inventory, quantity, alert_date)

**Complete schema available in:** `database/schema.sql`

---

## 7. DDL Commands

All DDL (Data Definition Language) commands are in `database/schema.sql`.

**Key DDL Operations:**
- CREATE DATABASE
- CREATE TABLE with constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK)
- ENUM types for status fields
- AUTO_INCREMENT for primary keys
- NOT NULL constraints
- UNIQUE constraints for email fields

**See:** `database/schema.sql` for complete DDL commands.

---

## 8. CRUD Operations

### CREATE Operations
- Create new inventory items
- Create new experiments
- Create new orders
- Create maintenance logs
- Create staff accounts
- Create student accounts
- Create suppliers
- Create master items

**Screenshots:** See Section 9 for frontend screenshots of CRUD operations.

### READ Operations
- View inventory list (with search and filters)
- View experiments
- View orders
- View maintenance logs
- View staff list
- View student list
- View suppliers
- View low stock alerts
- View dashboard statistics

**Screenshots:** See Section 9 for frontend screenshots.

### UPDATE Operations
- Update inventory quantities and status
- Update order status (triggers inventory update)
- Update maintenance log status (triggers inventory status change)
- Update staff information
- Update student information
- Update item details
- Update supplier information

**Screenshots:** See Section 9 for frontend screenshots.

### DELETE Operations
- Delete inventory items (with foreign key constraint checks)
- Delete experiments (if no inventory used)
- Delete staff accounts (with constraint checks)
- Delete student accounts
- Delete items (with constraint checks)
- Delete suppliers (with constraint checks)

**Screenshots:** See Section 9 for frontend screenshots.

**Note:** All CRUD operations are implemented in `app/routes/main.py` and accessible through the web interface. Screenshots should be taken during application demonstration.

---

## 9. Application Features and Screenshots

### Feature 1: Login System
**Description:** Secure authentication with role-based access. Supports Staff and Student login with bcrypt password hashing.

**Screenshot Location:** `app/templates/login.html`

### Feature 2: Admin Dashboard
**Description:** Comprehensive dashboard showing staff count, student count, low stock alerts, and system statistics.

**Screenshot Location:** `app/templates/admin_dashboard.html`

### Feature 3: Supervisor Dashboard
**Description:** Lab-specific dashboard showing pending maintenance, pending orders, and lab statistics.

**Screenshot Location:** `app/templates/supervisor_dashboard.html`

### Feature 4: Student Dashboard
**Description:** Student view showing assigned lab information and available experiments.

**Screenshot Location:** `app/templates/student_dashboard.html`

### Feature 5: Inventory Management
**Description:** Full CRUD operations for inventory with search, filter by lab, and status filtering.

**Screenshot Location:** `app/templates/inventory_list.html`, `app/templates/inventory_edit.html`

### Feature 6: Experiment Management
**Description:** Create experiments, assign to labs, and track inventory usage.

**Screenshot Location:** `app/templates/experiment_list.html`, `app/templates/experiment_form.html`, `app/templates/experiment_view.html`

### Feature 7: Order Management
**Description:** Create orders, add items, and process order receipt with automatic inventory updates.

**Screenshot Location:** `app/templates/order_list.html`, `app/templates/order_form.html`, `app/templates/order_view.html`

### Feature 8: Maintenance Management
**Description:** Log maintenance activities and track completion status with automatic inventory status updates.

**Screenshot Location:** `app/templates/maintenance_list.html`, `app/templates/maintenance_form.html`

### Feature 9: Staff Management
**Description:** Admin functionality to manage staff accounts, roles, and lab assignments.

**Screenshot Location:** `app/templates/staff_list.html`, `app/templates/staff_form.html`

### Feature 10: Student Management
**Description:** Admin functionality to manage student accounts and lab assignments.

**Screenshot Location:** `app/templates/student_list.html`, `app/templates/student_form.html`

### Feature 11: Supplier Management
**Description:** Manage suppliers and assign items to suppliers.

**Screenshot Location:** `app/templates/supplier_list.html`, `app/templates/supplier_form.html`, `app/templates/supplier_view.html`

### Feature 12: Low Stock Alerts
**Description:** View items that are below minimum stock levels.

**Screenshot Location:** `app/templates/low_stock_list.html`

**Note:** Screenshots should be captured during application demonstration and included in the final report document.

---

## 10. Triggers, Procedures, Functions, Nested Queries, Joins, Aggregate Queries

### 10.1 Triggers

#### Trigger 1: `trg_update_inventory_on_order_receive`
**Type:** AFTER UPDATE on `Order` table  
**Purpose:** Automatically updates inventory when an order status changes to "Received"  
**Location:** `database/triggers.sql` (lines 6-44)

#### Trigger 2: `trg_reduce_inventory_after_experiment`
**Type:** AFTER INSERT on `Experiment_Inventory` table  
**Purpose:** Automatically reduces inventory quantity when items are used in experiments  
**Location:** `database/triggers.sql` (lines 48-56)

#### Trigger 3: `trg_update_inventory_after_maintenance`
**Type:** AFTER UPDATE on `Maintenance_Log` table  
**Purpose:** Sets inventory status to "Available" when maintenance is completed  
**Location:** `database/triggers.sql` (lines 60-71)

#### Trigger 4: `trg_prevent_negative_stock`
**Type:** BEFORE UPDATE on `Inventory` table  
**Purpose:** Prevents inventory quantity from becoming negative  
**Location:** `database/triggers.sql` (lines 75-82)

#### Trigger 5: `trg_low_stock_alert`
**Type:** AFTER UPDATE on `Inventory` table  
**Purpose:** Automatically creates low stock alerts when quantity falls below minimum level  
**Location:** `database/triggers.sql` (lines 86-98)

### 10.2 Stored Procedures

#### Procedure 1: `Assign_Experiment`
**Purpose:** Creates a new experiment and assigns it to a lab and staff member  
**Parameters:** experiment_name, lab_id, staff_id, description  
**Location:** `database/procedures.sql` (lines 6-15)

#### Procedure 2: `Add_Order`
**Purpose:** Creates a new order from a supplier  
**Parameters:** supplier_id, lab_id, order_date, delivery_date, total_cost  
**Location:** `database/procedures.sql` (lines 19-29)

#### Procedure 3: `Log_Maintenance`
**Purpose:** Logs a maintenance activity and sets inventory status to "Maintenance"  
**Parameters:** inventory_id, staff_id, description  
**Location:** `database/procedures.sql` (lines 33-47)

#### Procedure 4: `Complete_Maintenance`
**Purpose:** Marks a maintenance log as completed (triggers inventory status update)  
**Parameters:** maintenance_id, staff_id  
**Location:** `database/procedures.sql` (lines 51-61)

#### Procedure 5: `Get_Staff_Experiment_Details` (JOIN QUERY)
**Purpose:** Retrieves staff details with their role, lab, and experiments using JOINs  
**Parameters:** staff_id  
**Location:** `database/procedures.sql` (lines 65-80)

#### Procedure 6: `Get_Items_Nearing_Restock` (NESTED QUERY)
**Purpose:** Finds items below minimum stock level using nested subqueries  
**Location:** `database/procedures.sql` (lines 84-101)

#### Procedure 7: `Assign_Item_To_Supplier`
**Purpose:** Assigns a master item to a supplier  
**Parameters:** supplier_id, item_id  
**Location:** `database/procedures.sql` (lines 105-114)

#### Procedure 8: `Get_Supplier_Items` (JOIN QUERY)
**Purpose:** Retrieves all items provided by a supplier using JOINs  
**Parameters:** supplier_id  
**Location:** `database/procedures.sql` (lines 118-130)

### 10.3 Functions

#### Function 1: `Is_Inventory_Available`
**Purpose:** Checks if required quantity of an inventory item is available  
**Returns:** BOOLEAN  
**Location:** `database/functions.sql` (lines 6-20)

#### Function 2: `Get_Total_Item_Quantity` (AGGREGATE)
**Purpose:** Returns total quantity of an item across all labs using SUM aggregate  
**Returns:** INT  
**Location:** `database/functions.sql` (lines 24-35)

#### Function 3: `Can_Assign_Student`
**Purpose:** Checks if a student can be assigned to a lab  
**Returns:** BOOLEAN  
**Location:** `database/functions.sql` (lines 39-55)

#### Function 4: `Get_Lab_Total_Item_Count` (AGGREGATE)
**Purpose:** Returns total number of items in a lab using SUM aggregate  
**Returns:** INT  
**Location:** `database/functions.sql` (lines 60-71)

#### Function 5: `Get_Supplier_Item_Count` (AGGREGATE)
**Purpose:** Returns number of items a supplier provides using COUNT aggregate  
**Returns:** INT  
**Location:** `database/functions.sql` (lines 75-86)

### 10.4 Join Queries

Multiple JOIN queries are used throughout the application:

1. **Staff with Roles and Lab** (INNER JOIN, LEFT JOIN)
   ```sql
   SELECT Staff.*, Roles.role_name, Lab.lab_name
   FROM Staff
   JOIN Roles ON Staff.role_id = Roles.role_id
   LEFT JOIN Lab ON Staff.lab_id = Lab.lab_id
   ```

2. **Inventory with Item and Lab** (INNER JOIN)
   ```sql
   SELECT inv.*, i.item_name, l.lab_name
   FROM Inventory inv
   JOIN Item i ON inv.item_id = i.item_id
   JOIN Lab l ON inv.lab_id = l.lab_id
   ```

3. **Order with Supplier and Lab** (INNER JOIN)
   ```sql
   SELECT o.*, s.name as supplier_name, l.lab_name
   FROM `Order` o
   JOIN Supplier s ON o.supplier_id = s.supplier_id
   JOIN Lab l ON o.lab_id = l.lab_id
   ```

4. **Experiment with Lab and Staff** (INNER JOIN)
   ```sql
   SELECT e.*, l.lab_name, s.name as staff_name
   FROM Experiment e
   JOIN Lab l ON e.lab_id = l.lab_id
   JOIN Staff s ON e.staff_id = s.staff_id
   ```

5. **Maintenance Log with Inventory, Item, Lab, and Staff** (Multiple JOINs)
   ```sql
   SELECT m.*, i.item_name, l.lab_name, s.name as staff_name
   FROM Maintenance_Log m
   JOIN Inventory inv ON m.inventory_id = inv.inventory_id
   JOIN Item i ON inv.item_id = i.item_id
   JOIN Lab l ON inv.lab_id = l.lab_id
   JOIN Staff s ON m.staff_id = s.staff_id
   ```

### 10.5 Aggregate Queries

1. **Count Staff, Students, Labs**
   ```sql
   SELECT COUNT(*) AS count FROM Staff;
   SELECT COUNT(*) AS count FROM Student;
   SELECT COUNT(*) AS count FROM Lab;
   ```

2. **Sum Inventory Quantities**
   ```sql
   SELECT SUM(quantity) FROM Inventory WHERE lab_id = 1;
   ```

3. **Count Low Stock Alerts**
   ```sql
   SELECT COUNT(*) AS count FROM Low_Stock_Alert;
   ```

4. **Get Total Item Quantity** (Function using SUM)
   ```sql
   SELECT Get_Total_Item_Quantity(2);
   ```

5. **Get Lab Total Item Count** (Function using SUM)
   ```sql
   SELECT Get_Lab_Total_Item_Count(1);
   ```

### 10.6 Nested Queries

1. **Get Items Nearing Restock** (Nested Subquery)
   ```sql
   SELECT i.item_name, inv.quantity, i.min_stock_level
   FROM Item i
   JOIN Inventory inv ON i.item_id = inv.item_id
   WHERE inv.item_id IN (
       SELECT item_id 
       FROM Inventory 
       WHERE quantity < (SELECT min_stock_level FROM Item WHERE item_id = Inventory.item_id)
   );
   ```

2. **Get Items Not Yet Assigned to Supplier** (Nested Subquery)
   ```sql
   SELECT item_id, item_name FROM Item
   WHERE item_id NOT IN (
       SELECT item_id FROM Supplier_Item WHERE supplier_id = 1
   );
   ```

**All queries available in:** `database/queries.sql`

---

## 11. Code Snippets for Invoking Procedures/Functions/Triggers

### 11.1 Invoking Stored Procedures (Python/Flask)

#### Example 1: Assign_Experiment
```python
# From app/routes/main.py (line 932)
cursor.callproc('Assign_Experiment', [name, lab_id, staff_id_int, description])
db_conn.commit()
```

#### Example 2: Add_Order
```python
# From app/routes/main.py (line 744)
cursor.callproc('Add_Order', [supplier_id, lab_id, order_date, delivery_date, total_cost])
db_conn.commit()
```

#### Example 3: Log_Maintenance
```python
# From app/routes/main.py (line 1144)
cursor.callproc('Log_Maintenance', [inventory_id, staff_id_int, description])
db_conn.commit()
```

#### Example 4: Complete_Maintenance
```python
# From app/routes/main.py (line 1202)
cursor.callproc('Complete_Maintenance', [maintenance_id, staff_id_int])
db_conn.commit()
```

#### Example 5: Get_Staff_Experiment_Details
```python
# Example usage
cursor.callproc('Get_Staff_Experiment_Details', [staff_id])
for result in cursor.stored_results():
    details = result.fetchall()
```

#### Example 6: Get_Supplier_Items
```python
# From app/routes/main.py (line 1468)
cursor.callproc('Get_Supplier_Items', [supplier_id])
for result in cursor.stored_results():
    supplier_items = result.fetchall()
```

### 11.2 Invoking Functions (Python/Flask)

#### Example 1: Is_Inventory_Available
```python
# From app/routes/main.py (line 1038)
cursor.execute("SELECT Is_Inventory_Available(%s, %s)", (inventory_id, quantity_used))
is_available = cursor.fetchone()[0]
```

#### Example 2: Get_Supplier_Item_Count
```python
# From app/routes/main.py (line 1359)
query = """
    SELECT s.*, Get_Supplier_Item_Count(s.supplier_id) AS item_count
    FROM Supplier s
    ORDER BY s.name
"""
cursor.execute(query)
```

### 11.3 Triggers (Automatic Execution)

Triggers are automatically executed by MySQL when specific events occur:

#### Trigger 1: Order Received (Automatic)
```python
# From app/routes/main.py (line 875)
# When order status is updated to 'Received', trigger fires automatically
query = "UPDATE `Order` SET status = 'Received', delivery_date = CURDATE() WHERE order_id = %s"
cursor.execute(query, (order_id,))
db_conn.commit()
# Trigger trg_update_inventory_on_order_receive automatically fires
```

#### Trigger 2: Experiment Inventory Usage (Automatic)
```python
# From app/routes/main.py (line 1046)
# When inventory is added to experiment, trigger fires automatically
query = """
    INSERT INTO Experiment_Inventory (experiment_id, inventory_id, quantity_used)
    VALUES (%s, %s, %s)
"""
cursor.execute(query, (experiment_id, inventory_id, quantity_used))
db_conn.commit()
# Trigger trg_reduce_inventory_after_experiment automatically fires
```

#### Trigger 3: Maintenance Completed (Automatic)
```python
# From app/routes/main.py (line 1202)
# When maintenance is completed via procedure, trigger fires automatically
cursor.callproc('Complete_Maintenance', [maintenance_id, staff_id_int])
db_conn.commit()
# Trigger trg_update_inventory_after_maintenance automatically fires
```

#### Trigger 4: Low Stock Alert (Automatic)
```python
# Trigger fires automatically when inventory quantity is updated below min_stock_level
# No explicit code needed - trigger handles it automatically
```

**All code snippets available in:** `app/routes/main.py`

---

## 12. SQL Queries in .sql File Format

All SQL queries are organized in separate files in the `database/` directory:

1. **`schema.sql`** - Complete DDL commands (CREATE DATABASE, CREATE TABLE, constraints)
2. **`seed.sql`** - DML commands (INSERT statements for initial data)
3. **`functions.sql`** - User-defined functions (5 functions)
4. **`procedures.sql`** - Stored procedures (8 procedures)
5. **`triggers.sql`** - Database triggers (5 triggers)
6. **`queries.sql`** - Example queries (JOIN, Nested, Aggregate queries)

**Location:** `database/` folder

**To execute all SQL files:**
```bash
python scripts/setup_project.py
```

Or manually:
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/functions.sql
mysql -u root -p < database/procedures.sql
mysql -u root -p < database/triggers.sql
mysql -u root -p < database/seed.sql
```

---

## 13. GitHub Repository Link

**Repository URL:** https://github.com/Kanishk-Raghavendra/lab-management-system

**Branch:** `dev` (main development branch)

**Key Files:**
- Application code: `app/` directory
- Database scripts: `database/` directory
- Documentation: `docs/` directory
- Tests: `tests/` directory
- Setup script: `scripts/setup_project.py`

**To clone the repository:**
```bash
git clone https://github.com/Kanishk-Raghavendra/lab-management-system.git
cd lab-management-system
```

---

## Additional Information

### Setup Instructions
See `README.md` for complete setup instructions.

### Login Credentials
See `LOGIN_CREDENTIALS.md` for default login credentials.

### Testing
Run tests with:
```bash
pytest tests/ -v
```

### Application Demo
1. Start the application: `python run.py`
2. Access at: `http://localhost:5000`
3. Login with credentials from `LOGIN_CREDENTIALS.md`
4. Explore all features and CRUD operations

---

## Conclusion

The Lab Management System successfully implements all required database operations including CRUD operations, stored procedures, functions, triggers, complex queries (JOINs, nested queries, aggregate queries), and provides a complete web-based interface for managing laboratory operations. The system demonstrates proper database design, data integrity through constraints and triggers, and efficient data access through optimized queries.

---

**End of Report**

