USE lab_management;

-- Drop Tables (in reverse order of creation, children first)
DROP TABLE IF EXISTS Low_Stock_Alert;
DROP TABLE IF EXISTS Maintenance_Log;
DROP TABLE IF EXISTS Experiment_Inventory;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Experiment;
DROP TABLE IF EXISTS Order_Item;
DROP TABLE IF EXISTS `Order`;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS Lab;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Supplier;
DROP TABLE IF EXISTS Roles;

-- Drop Procedures
DROP PROCEDURE IF EXISTS Assign_Experiment;
DROP PROCEDURE IF EXISTS Add_Order;
DROP PROCEDURE IF EXISTS Log_Maintenance;
DROP PROCEDURE IF EXISTS Complete_Maintenance;
DROP PROCEDURE IF EXISTS Get_Staff_Experiment_Details;
DROP PROCEDURE IF EXISTS Get_Items_Nearing_Restock;

-- Drop Functions
DROP FUNCTION IF EXISTS Is_Inventory_Available;
DROP FUNCTION IF EXISTS Get_Total_Item_Quantity;
DROP FUNCTION IF EXISTS Can_Assign_Student;
DROP FUNCTION IF EXISTS Get_Lab_Capacity_Usage;

-- Drop Triggers
DROP TRIGGER IF EXISTS trg_update_inventory_on_order_receive;
DROP TRIGGER IF EXISTS trg_reduce_inventory_after_experiment;
DROP TRIGGER IF EXISTS trg_update_inventory_after_maintenance;
DROP TRIGGER IF EXISTS trg_prevent_negative_stock;
DROP TRIGGER IF EXISTS trg_low_stock_alert;

-- Drop Database
DROP DATABASE IF EXISTS lab_management;