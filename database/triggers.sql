-- ==============================================
-- Lab Management System - Triggers
-- Works with schema.sql
-- ==============================================

USE lab_management;

DELIMITER //

-- 1️⃣ Trigger: Update Inventory when Order is Received
CREATE TRIGGER trg_update_inventory_on_order_receive
AFTER UPDATE ON `Order`
FOR EACH ROW
BEGIN
    IF NEW.status = 'Received' THEN
        INSERT INTO Inventory(item_id, lab_id, quantity, status, last_updated)
        SELECT item_id, NULL, quantity_ordered, 'Available', NOW()
        FROM Order_Item
        WHERE order_id = NEW.order_id;
    END IF;
END;
//

-- 2️⃣ Trigger: Reduce Inventory after Experiment usage
CREATE TRIGGER trg_reduce_inventory_after_experiment
AFTER INSERT ON Experiment_Inventory
FOR EACH ROW
BEGIN
    UPDATE Inventory
    SET quantity = quantity - NEW.quantity_used,
        last_updated = NOW()
    WHERE inventory_id = NEW.inventory_id;
END;
//

-- 3️⃣ Trigger: Update Inventory Status after Maintenance Completed
CREATE TRIGGER trg_update_inventory_after_maintenance
AFTER UPDATE ON Maintenance_Log
FOR EACH ROW
BEGIN
    IF NEW.status = 'Completed' THEN
        UPDATE Inventory
        SET status = 'Available',
            last_updated = NOW()
        WHERE inventory_id = NEW.inventory_id;
    END IF;
END;
//

-- 4️⃣ Optional Trigger: Prevent Negative Stock
CREATE TRIGGER trg_prevent_negative_stock
BEFORE UPDATE ON Inventory
FOR EACH ROW
BEGIN
    IF NEW.quantity < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Inventory quantity cannot be negative';
    END IF;
END;
//

-- 5️⃣ Optional Trigger: Low Stock Alert (just updates a log table)
CREATE TABLE IF NOT EXISTS Low_Stock_Alert (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    inventory_id INT NOT NULL,
    alert_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    quantity INT,
    FOREIGN KEY (item_id) REFERENCES Item(item_id),
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id)
);

CREATE TRIGGER trg_low_stock_alert
AFTER UPDATE ON Inventory
FOR EACH ROW
BEGIN
    IF NEW.quantity < (SELECT min_stock_level FROM Item WHERE item_id = NEW.item_id) THEN
        INSERT INTO Low_Stock_Alert(item_id, inventory_id, quantity)
        VALUES (NEW.item_id, NEW.inventory_id, NEW.quantity);
    END IF;
END;
//

DELIMITER ;
