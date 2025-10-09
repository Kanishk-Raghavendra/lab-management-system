USE lab_management;

-- -----------------------
-- Check inventory
-- -----------------------
SELECT * FROM Inventory;

-- -----------------------
-- Check if inventory is available for 3 microscopes
-- -----------------------
SELECT Is_Inventory_Available(1,3) AS Microscope_Available;

-- -----------------------
-- Check total quantity of Test Tubes
-- -----------------------
SELECT Get_Total_Item_Quantity(2) AS Total_TestTubes;

-- -----------------------
-- Can Student One be assigned to Lab 1?
-- -----------------------
SELECT Can_Assign_Student(1,1) AS Can_Assign;

-- -----------------------
-- List all experiments for Lab 1
-- -----------------------
SELECT * FROM Experiment WHERE lab_id = 1;

-- -----------------------
-- Assign an experiment via procedure
-- -----------------------
CALL Assign_Experiment('Volumetric Analysis',1,2,'Advanced titration experiment');

-- -----------------------
-- Check experiments after procedure call
-- -----------------------
SELECT * FROM Experiment WHERE lab_id = 1;

-- -----------------------
-- Log maintenance for an inventory item
-- -----------------------
CALL Log_Maintenance(1,2,'Polish microscope lens');

-- -----------------------
-- Check maintenance logs
-- -----------------------
SELECT * FROM Maintenance_Log;

-- -----------------------
-- Update order to Received (trigger should add to inventory)
-- -----------------------
UPDATE `Order` SET status='Received' WHERE order_id=1;

-- Verify inventory update after order received
SELECT * FROM Inventory;

-- -----------------------
-- Inventory reduction after experiment usage
-- -----------------------
INSERT INTO Experiment_Inventory(experiment_id, inventory_id, quantity_used)
VALUES(1,1,1);

-- Verify inventory quantity reduced
SELECT * FROM Inventory;
