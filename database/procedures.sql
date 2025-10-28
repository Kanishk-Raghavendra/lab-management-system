USE lab_management;

DELIMITER //

-- 1️⃣ Assign Experiment (No change)
CREATE PROCEDURE Assign_Experiment(
    IN p_experiment_name VARCHAR(100),
    IN p_lab_id INT,
    IN p_staff_id INT,
    IN p_description VARCHAR(255)
)
BEGIN
    INSERT INTO Experiment(experiment_name, lab_id, staff_id, description, experiment_date)
    VALUES(p_experiment_name, p_lab_id, p_staff_id, p_description, CURDATE());
END;
//

-- 2️⃣ Add a New Order (!! UPDATED: Added p_lab_id !!)
CREATE PROCEDURE Add_Order(
    IN p_supplier_id INT,
    IN p_lab_id INT, /* !! ADDED !! */
    IN p_order_date DATE,
    IN p_delivery_date DATE,
    IN p_total_cost DECIMAL(10,2)
)
BEGIN
    INSERT INTO `Order`(supplier_id, lab_id, order_date, delivery_date, total_cost, status)
    VALUES(p_supplier_id, p_lab_id, p_order_date, p_delivery_date, p_total_cost, 'Pending');
END;
//

-- 3️⃣ Log Maintenance for an Inventory Item (No change)
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

-- 4️⃣ !! NEW: Complete a Maintenance Task
CREATE PROCEDURE Complete_Maintenance(
    IN p_maintenance_id INT,
    IN p_staff_id INT
)
BEGIN
    -- This UPDATE will fire 'trg_update_inventory_after_maintenance'
    UPDATE Maintenance_Log
    SET status = 'Completed',
        staff_id = p_staff_id -- Log who completed it
    WHERE maintenance_id = p_maintenance_id;
END;
//

-- 5️⃣ !! NEW: (JOIN QUERY) Get Staff, their Role, and Experiments
CREATE PROCEDURE Get_Staff_Experiment_Details(
    IN p_staff_id INT
)
BEGIN
    SELECT 
        s.name AS staff_name,
        r.role_name AS role,
        l.lab_name AS assigned_lab,
        e.experiment_name,
        e.experiment_date
    FROM Staff s
    JOIN Roles r ON s.role_id = r.role_id
    LEFT JOIN Lab l ON s.lab_id = l.lab_id
    LEFT JOIN Experiment e ON s.staff_id = e.staff_id
    WHERE s.staff_id = p_staff_id;
END;
//

-- 6️⃣ !! NEW: (NESTED QUERY) Get items that are below min_stock_level
CREATE PROCEDURE Get_Items_Nearing_Restock()
BEGIN
    SELECT 
        i.item_name,
        i.item_type,
        inv.quantity,
        i.min_stock_level,
        l.lab_name
    FROM Item i
    JOIN Inventory inv ON i.item_id = inv.item_id
    JOIN Lab l ON inv.lab_id = l.lab_id
    WHERE inv.item_id IN (
        -- Nested Subquery
        SELECT item_id 
        FROM Inventory 
        WHERE quantity < (SELECT min_stock_level FROM Item WHERE item_id = Inventory.item_id)
    );
END;
//

DELIMITER ;