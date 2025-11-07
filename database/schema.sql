/* ===========================================
Lab Management System - Complete Schema
==============================================
*/

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS lab_management;
USE lab_management;

-- 2. Roles Table
CREATE TABLE IF NOT EXISTS Roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE, /* Admin, Supervisor, Assistant */
    description VARCHAR(255)
);

-- 3. Supplier Table
CREATE TABLE IF NOT EXISTS Supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_no VARCHAR(15),
    email VARCHAR(100),
    address VARCHAR(255)
);

-- 4. Item Table (Equipment + Consumables)
CREATE TABLE IF NOT EXISTS Item (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    item_type ENUM('Equipment','Consumable') NOT NULL,
    description VARCHAR(255),
    unit_price DECIMAL(10,2),
    min_stock_level INT DEFAULT 0
);

-- 5. Lab Table
CREATE TABLE IF NOT EXISTS Lab (
    lab_id INT AUTO_INCREMENT PRIMARY KEY,
    lab_name VARCHAR(100) NOT NULL,
    lab_type ENUM('Chemistry','Physics') NOT NULL,
    location VARCHAR(255)
);

-- 6. Staff Table
CREATE TABLE IF NOT EXISTS Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role_id INT NOT NULL,
    contact_no VARCHAR(15),
    email VARCHAR(100) UNIQUE NOT NULL, /* Added UNIQUE NOT NULL, needed for login */
    lab_id INT,
    password_hash VARCHAR(255) NOT NULL, /* !! ADDED: For login */
    FOREIGN KEY (role_id) REFERENCES Roles(role_id),
    FOREIGN KEY (lab_id) REFERENCES Lab(lab_id)
);

-- 7. Inventory Table
CREATE TABLE IF NOT EXISTS Inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    lab_id INT NOT NULL, /* !! UPDATED: Made this NOT NULL */
    quantity INT DEFAULT 0,
    status ENUM('Available','In Use','Maintenance') DEFAULT 'Available',
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES Item(item_id),
    FOREIGN KEY (lab_id) REFERENCES Lab(lab_id),
    UNIQUE KEY uk_item_lab (item_id, lab_id) /* ADDED: Prevents duplicate item entries per lab */
);

-- 8. Order Table
CREATE TABLE IF NOT EXISTS `Order` (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    lab_id INT NOT NULL, /* !! ADDED: Specifies which lab the order is for */
    order_date DATE NOT NULL,
    delivery_date DATE,
    total_cost DECIMAL(10,2),
    status ENUM('Pending','Received','Cancelled') DEFAULT 'Pending',
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id),
    FOREIGN KEY (lab_id) REFERENCES Lab(lab_id) /* !! ADDED: Foreign key for lab_id */
);

-- 9. Order_Item Junction Table
CREATE TABLE IF NOT EXISTS Order_Item (
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity_ordered INT NOT NULL,
    cost_per_unit DECIMAL(10,2),
    PRIMARY KEY(order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id),
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
);

-- 10. Experiment Table
CREATE TABLE IF NOT EXISTS Experiment (
    experiment_id INT AUTO_INCREMENT PRIMARY KEY,
    experiment_name VARCHAR(100) NOT NULL,
    lab_id INT,
    staff_id INT,
    description VARCHAR(255),
    experiment_date DATE,
    FOREIGN KEY (lab_id) REFERENCES Lab(lab_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

-- 11. Student Table
CREATE TABLE IF NOT EXISTS Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL, /* !! ADDED: For student login */
    lab_id INT,
    assigned_staff_id INT,
    FOREIGN KEY (lab_id) REFERENCES Lab(lab_id),
    FOREIGN KEY (assigned_staff_id) REFERENCES Staff(staff_id)
);

-- 12. Experiment_Inventory Junction Table
CREATE TABLE IF NOT EXISTS Experiment_Inventory (
    experiment_id INT NOT NULL,
    inventory_id INT NOT NULL,
    quantity_used INT NOT NULL,
    PRIMARY KEY(experiment_id, inventory_id),
    FOREIGN KEY (experiment_id) REFERENCES Experiment(experiment_id),
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id)
);

-- 13. Maintenance_Log Table
CREATE TABLE IF NOT EXISTS Maintenance_Log (
    maintenance_id INT AUTO_INCREMENT PRIMARY KEY,
    inventory_id INT NOT NULL,
    staff_id INT NOT NULL,
    log_date DATE NOT NULL,
    description VARCHAR(255),
    status ENUM('Pending','Completed') DEFAULT 'Pending',
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

-- 14. Low_Stock_Alert Table (From triggers.sql)
CREATE TABLE IF NOT EXISTS Low_Stock_Alert (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    inventory_id INT NOT NULL,
    alert_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    quantity INT,
    FOREIGN KEY (item_id) REFERENCES Item(item_id),
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id),
    UNIQUE KEY uk_low_stock_inventory (inventory_id)
);

-- 15. Supplier_Item (M:N)
CREATE TABLE IF NOT EXISTS Supplier_Item (
    supplier_id INT NOT NULL,
    item_id INT NOT NULL,
    PRIMARY KEY(supplier_id, item_id),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES Item(item_id) ON DELETE CASCADE
);