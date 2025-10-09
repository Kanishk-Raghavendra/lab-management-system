USE lab_management;

-- -----------------------
-- Roles
-- -----------------------
INSERT INTO Roles(role_name, description) VALUES
('Admin','Manages overall lab operations'),
('Supervisor','Manages lab and assigns experiments'),
('Assistant','Assists supervisor and staff');

-- -----------------------
-- Labs
-- -----------------------
INSERT INTO Lab(lab_name, lab_type, location) VALUES
('Chem Lab 1','Chemistry','Building A'),
('Chem Lab 2','Chemistry','Building B');

-- -----------------------
-- Staff
-- -----------------------
INSERT INTO Staff(name, role_id, contact_no, email, lab_id) VALUES
('Alice',1,'9999999999','alice@lab.com',NULL), -- Admin
('Bob',2,'8888888888','bob@lab.com',1),       -- Supervisor
('Charlie',3,'7777777777','charlie@lab.com',1); -- Assistant

-- -----------------------
-- Suppliers
-- -----------------------
INSERT INTO Supplier(name, contact_no, email, address) VALUES
('Supplier A','1111111111','supA@email.com','Address 1'),
('Supplier B','2222222222','supB@email.com','Address 2');

-- -----------------------
-- Items
-- -----------------------
INSERT INTO Item(item_name, item_type, description, unit_price, min_stock_level) VALUES
('Microscope','Equipment','Optical microscope',5000,2),
('Test Tube','Consumable','Glass test tube',5,50),
('Bunsen Burner','Equipment','Gas burner',3000,1),
('Beaker','Consumable','Glass beaker 250ml',10,20);

-- -----------------------
-- Inventory
-- -----------------------
INSERT INTO Inventory(item_id, lab_id, quantity, status) VALUES
(1,1,5,'Available'),
(2,1,100,'Available'),
(3,1,3,'Available'),
(4,1,50,'Available');

-- -----------------------
-- Orders
-- -----------------------
INSERT INTO `Order`(supplier_id, order_date, delivery_date, total_cost, status) VALUES
(1,'2025-10-09','2025-10-12',10000,'Pending');

INSERT INTO Order_Item(order_id, item_id, quantity_ordered, cost_per_unit) VALUES
(1,1,2,5000),
(1,2,50,5);

-- -----------------------
-- Students
-- -----------------------
INSERT INTO Student(name, email, lab_id) VALUES
('Student One','student1@email.com',1),
('Student Two','student2@email.com',1),
('Student Three','student3@email.com',1),
('Student Four','student4@email.com',1);

-- -----------------------
-- Experiments
-- -----------------------
INSERT INTO Experiment(experiment_name, lab_id, staff_id, description, experiment_date) VALUES
('Acid-Base Titration',1,2,'Basic chemistry experiment','2025-10-09'),
('Heating Test',1,2,'Bunsen burner usage','2025-10-10');

-- -----------------------
-- Maintenance Logs
-- -----------------------
INSERT INTO Maintenance_Log(inventory_id, staff_id, log_date, description, status) VALUES
(1,2,'2025-10-09','Clean microscope lens','Pending'),
(3,2,'2025-10-09','Check Bunsen burner','Pending');
