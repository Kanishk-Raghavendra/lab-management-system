USE lab_management;

DELIMITER //

-- 1️⃣ Check Inventory Availability (No change)
CREATE FUNCTION Is_Inventory_Available(p_inventory_id INT, p_required_quantity INT)
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE available_quantity INT;
    SELECT quantity INTO available_quantity
    FROM Inventory
    WHERE inventory_id = p_inventory_id AND status = 'Available';
    
    IF available_quantity >= p_required_quantity THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
//

-- 2️⃣ Get Total Quantity of an Item Across All Labs (No change)
CREATE FUNCTION Get_Total_Item_Quantity(p_item_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total_quantity INT;
    
    SELECT SUM(quantity) INTO total_quantity
    FROM Inventory
    WHERE item_id = p_item_id;
    
    RETURN IFNULL(total_quantity, 0);
END;
//

-- 3️⃣ Check if Student Can Be Assigned to Lab (No change)
CREATE FUNCTION Can_Assign_Student(p_student_id INT, p_lab_id INT)
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE lab_count INT;
    
    -- Checks if student is already in ANY lab.
    SELECT COUNT(*) INTO lab_count
    FROM Student
    WHERE student_id = p_student_id AND lab_id IS NOT NULL;
    
    IF lab_count = 0 THEN
        RETURN TRUE; -- Can be assigned
    ELSE
        RETURN FALSE; -- Already assigned to a lab
    END IF;
END;
//


-- 4️⃣ !! NEW: (AGGREGATE QUERY) Get total number of items in a lab
CREATE FUNCTION Get_Lab_Total_Item_Count(p_lab_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total_items INT;
    
    SELECT SUM(quantity) INTO total_items -- Aggregate Function SUM()
    FROM Inventory
    WHERE lab_id = p_lab_id;
    
    RETURN IFNULL(total_items, 0);
END;
//

DELIMITER ;