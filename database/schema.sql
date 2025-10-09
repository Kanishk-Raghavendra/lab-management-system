-- ==============================================
-- Lab Management System - Complete Schema
-- Includes Roles, Staff, Items, Inventory, Orders, Experiments, Maintenance
-- ==============================================

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS lab_management;
USE lab_management;

-- 2. Roles Table
CREATE TABLE Roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
);

-- 3. Supplier Table
CREATE TABLE Supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_no VARCHAR(15),
    email VARCHAR(100),
    address VARCHAR(255)
);

-- 4. Item Table (Equipment + Consumables)
CREATE TABLE Item (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    item_type ENUM('Equipment','Consumable') NOT NULL,
    description VARCHAR(255),
    unit_price DECIMAL(10,2),
    min_stock_level INT DEFAULT 0
);

-- 5. Lab Table
CREATE TABLE Lab (
    lab_id INT AUTO_INCREMENT PRIMARY KEY,
    lab_name VARCHAR(100) NOT NULL,
    lab_type ENUM('Chemistry','Physics') NOT NULL,
    location VARCHAR(255)
);

-- 6. Staff Table
CREATE TABLE Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role_id INT NOT NULL,
    contact_no VARCHAR(15),
    email VARCHAR(100),
    lab_id INT,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id),
    FOREIGN KEY (lab_id) REFERENCES Lab(lab_id)
);

-- 7. Inventory Table
CREATE TABLE Inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    lab_id INT,
    quantity INT DEFAULT 0,
    status ENUM('Available','In Use','Maintenance') DEFAULT 'Available',
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES Item(item_id),
    FOREIGN KEY (lab_id) REFERENCES Lab(lab_id)
);

-- 8. Order Table
CREATE TABLE `Order` (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    order_date DATE NOT NULL,
    delivery_date DATE,
    total_cost DECIMAL(10,2),
    status ENUM('Pending','Received','Cancelled') DEFAULT 'Pending',
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
);

-- 9. Order_Item Junction Table (M:N relationship)
CREATE TABLE Order_Item (
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity_ordered INT NOT NULL,
    cost_per_unit DECIMAL(10,2),
    PRIMARY KEY(order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id),
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
);

-- 10. Experiment Table
CREATE TABLE Experiment (
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
CREATE TABLE Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lab_id INT,
    assigned_staff_id INT,
    FOREIGN KEY (lab_id) REFERENCES Lab(lab_id),
    FOREIGN KEY (assigned_staff_id) REFERENCES Staff(staff_id)
);

-- 11. Experiment_Inventory Junction Table (M:N relationship)
CREATE TABLE Experiment_Inventory (
    experiment_id INT NOT NULL,
    inventory_id INT NOT NULL,
    quantity_used INT NOT NULL,
    PRIMARY KEY(experiment_id, inventory_id),
    FOREIGN KEY (experiment_id) REFERENCES Experiment(experiment_id),
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id)
);

-- 12. Maintenance_Log Table (linked to Inventory)
CREATE TABLE Maintenance_Log (
    maintenance_id INT AUTO_INCREMENT PRIMARY KEY,
    inventory_id INT NOT NULL,
    staff_id INT NOT NULL,
    log_date DATE NOT NULL,
    description VARCHAR(255),
    status ENUM('Pending','Completed') DEFAULT 'Pending',
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

-- ==============================================
-- SCHEMA CREATION COMPLETE
-- ==============================================
