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
-- Staff (!! UPDATED: Added password_hash !!)
-- -----------------------
-- Password hashes are bcrypt-generated. Original passwords for reference:
-- alice@lab.com: alicepass
-- bob@lab.com: bobpass
-- charlie@lab.com: charliepass
INSERT INTO Staff(name, role_id, contact_no, email, lab_id, password_hash) VALUES
('Alice',1,'9999999999','alice@lab.com',NULL,'$2b$12$dWQDxlsborMlmwgfRvjd0OOIkHdzZLdcq82gHTdNTj7cgESLS0qmG'), -- Admin
('Bob',2,'8888888888','bob@lab.com',1,'$2b$12$dV0ev7jg7ptSdCA5N0G.0.lIzFb.cwTT/iqje1/oVuCgx6UXy.VUO'),       -- Supervisor
('Charlie',3,'7777777777','charlie@lab.com',1,'$2b$12$GiTPmgdw0A6JILYUKbOkCeOYDsXjLDyb7eLQ6dzXFKjtx.RvG1J.W'); -- Assistant

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
(1,1,5,'Available'),  -- Microscope in Lab 1
(2,1,100,'Available'), -- Test Tube in Lab 1
(3,1,3,'Available'),  -- Bunsen Burner in Lab 1
(4,1,50,'Available');  -- Beaker in Lab 1

-- -----------------------
-- Orders (!! UPDATED: Added lab_id=1 !!)
-- -----------------------
INSERT INTO `Order`(supplier_id, lab_id, order_date, delivery_date, total_cost, status) VALUES
(1, 1, '2025-10-09','2025-10-12',10000,'Pending');

INSERT INTO Order_Item(order_id, item_id, quantity_ordered, cost_per_unit) VALUES
(1,1,2,5000), -- 2 Microscopes
(1,2,50,5);   -- 50 Test Tubes

-- -----------------------
-- Students (!! UPDATED: Added email column and values !!)
-- -----------------------
-- Password hashes are bcrypt-generated. Original passwords for reference:
-- student1@email.com: student1pass
-- student2@email.com: student2pass
-- student3@email.com: student3pass
-- student4@email.com: student4pass
INSERT INTO Student(name, email, password_hash, lab_id, assigned_staff_id) VALUES
('Student One','student1@email.com', '$2b$12$R/WAW6vlIcAw9hRcRZhZK.NjPmMi1nZcPZpTwU/WB.ralHSsF3YpK', 1, 2),
('Student Two','student2@email.com', '$2b$12$DvSwx2DIR888XHxoiOEqm.JAyOP0HLwHqJakyiSuOlf0msXHQsmYq', 1, 2),
('Student Three','student3@email.com', '$2b$12$D6KqCSkn87VP5Vev58.hEu8uboaT4D0XziWDRhLqzuRHfRQZs0JkW', 1, 3),
('Student Four','student4@email.com', '$2b$12$0tfeGvMMV3hkQ0NA/0/rhe/y46lGdAUs8cZpuX7Z/6vt6HvrPbZoS', 1, 3);

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

-- -----------------------
-- Supplier Items
-- -----------------------
INSERT INTO Supplier_Item(supplier_id, item_id) VALUES
(1, 1), -- Supplier A supplies Microscopes
(1, 2), -- Supplier A supplies Test Tubes
(2, 3), -- Supplier B supplies Bunsen Burners
(2, 4); -- Supplier B supplies Beakers