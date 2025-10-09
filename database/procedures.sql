-- ==============================================
-- Lab Management System - Procedures
-- ==============================================

USE lab_management;

DELIMITER //

-- 1️⃣ Assign Experiment to Students with Inventory Check
CREATE PROCEDURE Assign_Experiment(
    IN p_experiment_name VARCHAR(100),
    IN p_lab_id INT,
    IN p_staff_id INT,
    IN p_description VARCHAR(255)
)
BEGIN
    DECLARE new_experiment_id INT;
    
    -- Insert new experiment
    INSERT INTO Experiment(experiment_name, lab_id, staff_id, description, experiment_date)
    VALUES(p_experiment_name, p_lab_id, p_staff_id, p_description, CURDATE());
    
    SET new_experiment_id = LAST_INSERT_ID();
    
    -- Check inventory for all items assigned to this lab
    -- This is just an example: you can extend it to actually assign items
    -- Ensure quantity > 0 before assignment
    SELECT inventory_id, item_id, quantity
    FROM Inventory
    WHERE lab_id = p_lab_id AND quantity > 0;
    
    -- You can insert into Experiment_Inventory only if quantity sufficient
    -- This part should be handled in application or extended SQL logic
END;
//

-- 2️⃣ Add a New Order with Multiple Items
CREATE PROCEDURE Add_Order(
    IN p_supplier_id INT,
    IN p_order_date DATE,
    IN p_delivery_date DATE,
    IN p_total_cost DECIMAL(10,2)
)
BEGIN
    -- Insert new order
    INSERT INTO `Order`(supplier_id, order_date, delivery_date, total_cost, status)
    VALUES(p_supplier_id, p_order_date, p_delivery_date, p_total_cost, 'Pending');
END;
//

-- 3️⃣ Log Maintenance for an Inventory Item
CREATE PROCEDURE Log_Maintenance(
    IN p_inventory_id INT,
    IN p_staff_id INT,
    IN p_description VARCHAR(255)
)
BEGIN
    -- Insert maintenance log
    INSERT INTO Maintenance_Log(inventory_id, staff_id, log_date, description, status)
    VALUES(p_inventory_id, p_staff_id, CURDATE(), p_description, 'Pending');
    
    -- Update inventory status to 'Maintenance'
    UPDATE Inventory
    SET status = 'Maintenance', last_updated = NOW()
    WHERE inventory_id = p_inventory_id;
END;
//

DELIMITER ;
