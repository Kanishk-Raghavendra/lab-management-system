USE lab_management;

-- -----------------------
-- 1. Check initial inventory
-- -----------------------
SELECT * FROM Inventory;
-- Expected Output: 4 rows (Microscope: 5, Test Tube: 100, Bunsen: 3, Beaker: 50)

-- -----------------------
-- 2. Check if 3 microscopes are available (Inventory ID 1)
-- -----------------------
SELECT Is_Inventory_Available(1,3) AS Microscope_Available;
-- Expected Output: 1 (TRUE), because 5 >= 3

-- -----------------------
-- 3. Get total quantity of Test Tubes (Item ID 2)
-- -----------------------
SELECT Get_Total_Item_Quantity(2) AS Total_TestTubes;
-- Expected Output: 100

-- -----------------------
-- 4. Check if Student 1 can be assigned (they are already in lab 1)
-- -----------------------
SELECT Can_Assign_Student(1,1) AS Can_Assign;
-- Expected Output: 0 (FALSE), because student 1 is already assigned to a lab.

-- -----------------------
-- 5. List all experiments for Lab 1
-- -----------------------
SELECT * FROM Experiment WHERE lab_id = 1;
-- Expected Output: 2 rows ('Acid-Base Titration', 'Heating Test')

-- -----------------------
-- 6. Assign a new experiment via procedure
-- -----------------------
CALL Assign_Experiment('Volumetric Analysis',1,2,'Advanced titration experiment');
-- Expected Output: Query OK, 1 row affected.

-- -----------------------
-- 7. Log maintenance for inventory item 1 (Microscope)
-- -----------------------
CALL Log_Maintenance(1,2,'Polish microscope lens');
-- Expected Output: Query OK, 1 row affected.
-- Side Effect: Inventory ID 1 status is set to 'Maintenance'

-- -----------------------
-- 8. Check maintenance logs
-- -----------------------
SELECT * FROM Maintenance_Log;
-- Expected Output: 3 rows (the 2 from seed + 'Polish microscope lens')

-- -----------------------
-- 9. Check status of item in maintenance
-- -----------------------
SELECT * FROM Inventory WHERE inventory_id = 1;
-- Expected Output: 1 row, showing quantity 5, status 'Maintenance'

-- -----------------------
-- 10. Complete a maintenance task (Log ID 1, completed by Staff 2)
-- -----------------------
CALL Complete_Maintenance(1, 2);
-- Expected Output: Query OK, 1 row affected.
-- Side Effect (Trigger): Inventory ID 1 status is set back to 'Available'

-- -----------------------
-- 11. Verify item is 'Available' again
-- -----------------------
SELECT * FROM Inventory WHERE inventory_id = 1;
-- Expected Output: 1 row, showing quantity 5, status 'Available'

-- -----------------------
-- 12. Update order to 'Received' (This will fire a trigger)
-- -----------------------
UPDATE `Order` SET status='Received' WHERE order_id=1;
-- Expected Output: Query OK, 1 row affected.
-- Side Effect (Trigger): Adds 2 Microscopes and 50 Test Tubes to Lab 1

-- -----------------------
-- 13. Verify inventory update after order
-- -----------------------
SELECT item_id, quantity FROM Inventory WHERE lab_id = 1;
-- Expected Output:
-- item_id 1 (Microscope): quantity 7 (was 5, +2 from order)
-- item_id 2 (Test Tube): quantity 150 (was 100, +50 from order)
-- item_id 3 (Bunsen Burner): quantity 3
-- item_id 4 (Beaker): quantity 50

-- -----------------------
-- 14. Use inventory in an experiment (This will fire a trigger)
-- -----------------------
INSERT INTO Experiment_Inventory(experiment_id, inventory_id, quantity_used)
VALUES(1,1,1); -- Use 1 of Inventory ID 1 (Microscope) for Experiment 1
-- Expected Output: Query OK, 1 row affected.
-- Side Effect (Trigger): Reduces Microscope quantity by 1

-- -----------------------
-- 15. Verify inventory quantity reduced
-- -----------------------
SELECT * FROM Inventory WHERE inventory_id = 1;
-- Expected Output: 1 row, showing quantity 6 (was 7, -1 from experiment)

-- -----------------------
-- 16. TEST NEW PROCEDURE (JOIN): Get details for Staff ID 2 (Bob)
-- -----------------------
CALL Get_Staff_Experiment_Details(2);
-- Expected Output: 3 rows, one for each experiment assigned to Bob
-- staff_name | role_name  | assigned_lab | experiment_name         | ...
-- 'Bob'      | 'Supervisor' | 'Chem Lab 1' | 'Acid-Base Titration' | ...
-- 'Bob'      | 'Supervisor' | 'Chem Lab 1' | 'Heating Test'        | ...
-- 'Bob'      | 'Supervisor' | 'Chem Lab 1' | 'Volumetric Analysis' | ...

-- -----------------------
-- 17. TEST NEW FUNCTION (AGGREGATE): Get total item count for Lab 1
-- -----------------------
SELECT Get_Lab_Total_Item_Count(1) AS Lab1_Total_Items;
-- Expected Output: 209 (6 + 150 + 3 + 50)

-- -----------------------
-- 18. TEST LOW STOCK (NESTED QUERY): First, make an item low-stock
-- -----------------------
-- Beaker min stock is 20, current quantity is 50. Let's set it to 15.
UPDATE Inventory SET quantity = 15 WHERE item_id = 4;
-- Expected Output: Query OK, 1 row affected.
-- Side Effect (Trigger): 'trg_low_stock_alert' fires, inserts into Low_Stock_Alert table.

-- -----------------------
-- 19. Check the Low_Stock_Alert table
-- -----------------------
SELECT * FROM Low_Stock_Alert;
-- Expected Output: 1 row, for item_id 4 (Beaker)

-- -----------------------
-- 20. TEST NEW PROCEDURE (NESTED QUERY): Get items needing restock
-- -----------------------
CALL Get_Items_Nearing_Restock();
-- Expected Output: 1 row
-- item_name | item_type  | quantity | min_stock_level | lab_name
-- 'Beaker'  | 'Consumable' | 15       | 20              | 'Chem Lab 1'

-- -----------------------
-- 21. TEST STUDENT LOGIN (Check for new password column)
-- -----------------------
SELECT student_id, name, email, password_hash FROM Student WHERE student_id = 1;
-- Expected Output: 1 row for 'Student One' with email and 'pass_student1_hashed'

-- -----------------------
-- 22. TEST NEW FUNCTION (AGGREGATE): Get item count for Supplier A (ID 1)
-- -----------------------
SELECT Get_Supplier_Item_Count(1) AS Supplier_A_Item_Count;
-- Expected Output: 2 (from seed.sql: Microscope, Test Tube)

-- -----------------------
-- 23. TEST NEW PROCEDURE (JOIN): Get items for Supplier B (ID 2)
-- -----------------------
CALL Get_Supplier_Items(2);
-- Expected Output: 2 rows
-- supplier_name | item_name     | item_type
-- 'Supplier B'  | 'Bunsen Burner' | 'Equipment'
-- 'Supplier B'  | 'Beaker'      | 'Consumable'

-- -----------------------
-- 24. TEST NEW PROCEDURE: Assign a new item (Beaker, ID 4) to Supplier A (ID 1)
-- -----------------------
CALL Assign_Item_To_Supplier(1, 4);
-- Expected Output: Query OK, 1 row affected.

-- -----------------------
-- 25. VERIFY ASSIGNMENT: Check Supplier A's item count again
-- -----------------------
SELECT Get_Supplier_Item_Count(1) AS Supplier_A_Item_Count;
-- Expected Output: 3 (Microscope, Test Tube, AND Beaker)