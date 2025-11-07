USE lab_management;

DELIMITER //

-- 1️⃣ Trigger: Update Inventory when Order is Received (!! UPDATED !!)
CREATE TRIGGER trg_update_inventory_on_order_receive
AFTER UPDATE ON `Order`
FOR EACH ROW
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_item_id INT;
    DECLARE v_quantity_ordered INT;
    DECLARE cur_order_items CURSOR FOR 
        SELECT item_id, quantity_ordered 
        FROM Order_Item 
        WHERE order_id = NEW.order_id;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Only run if the order status is changing to 'Received'
    IF NEW.status = 'Received' AND OLD.status != 'Received' THEN
        OPEN cur_order_items;

        read_loop: LOOP
            FETCH cur_order_items INTO v_item_id, v_quantity_ordered;
            IF done THEN
                LEAVE read_loop;
            END IF;
            
            -- This is the "UPSERT" magic.
            -- It tries to insert a new row for the item in that lab.
            -- If a row with that (item_id, lab_id) pair already exists (due to our UNIQUE KEY),
            -- it executes the ON DUPLICATE KEY UPDATE part instead.
            INSERT INTO Inventory(item_id, lab_id, quantity, status, last_updated)
            VALUES (v_item_id, NEW.lab_id, v_quantity_ordered, 'Available', NOW())
            ON DUPLICATE KEY UPDATE
                quantity = quantity + v_quantity_ordered,
                last_updated = NOW(),
                status = 'Available'; -- Set to 'Available' in case it was in 'Maintenance'
                
        END LOOP;

        CLOSE cur_order_items;
    END IF;
END;
//

-- 2️⃣ Trigger: Reduce Inventory after Experiment usage (No change)
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

-- 3️⃣ Trigger: Update Inventory Status after Maintenance Completed (No change)
CREATE TRIGGER trg_update_inventory_after_maintenance
AFTER UPDATE ON Maintenance_Log
FOR EACH ROW
BEGIN
    -- If log status changes to 'Completed', set inventory to 'Available'
    IF NEW.status = 'Completed' AND OLD.status != 'Completed' THEN
        UPDATE Inventory
        SET status = 'Available',
            last_updated = NOW()
        WHERE inventory_id = NEW.inventory_id;
    END IF;
END;
//

-- 4️⃣ Trigger: Prevent Negative Stock (No change)
CREATE TRIGGER trg_prevent_negative_stock
BEFORE UPDATE ON Inventory
FOR EACH ROW
BEGIN
    IF NEW.quantity < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Inventory quantity cannot be negative';
    END IF;
END;
//

-- 5️⃣ Trigger: Low Stock Alert (No change, but requires Low_Stock_Alert table in schema)
CREATE TRIGGER trg_low_stock_alert
AFTER UPDATE ON Inventory
FOR EACH ROW
BEGIN
    DECLARE v_min_stock INT;
    SELECT min_stock_level INTO v_min_stock FROM Item WHERE item_id = NEW.item_id;

    -- When quantity drops below minimum, upsert alert. When it recovers, clear alert.
    IF NEW.quantity < v_min_stock THEN
        INSERT INTO Low_Stock_Alert(item_id, inventory_id, quantity)
        VALUES (NEW.item_id, NEW.inventory_id, NEW.quantity)
        ON DUPLICATE KEY UPDATE
            quantity = NEW.quantity,
            alert_date = NOW();
    ELSEIF NEW.quantity >= v_min_stock AND OLD.quantity < v_min_stock THEN
        DELETE FROM Low_Stock_Alert WHERE inventory_id = NEW.inventory_id;
    END IF;
END;
//

DELIMITER ;