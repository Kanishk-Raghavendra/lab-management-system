Lab Management System - Schema Explanation
------------------------------------------

Key Entities and Attributes:

1. Roles
   - role_id (PK)
   - role_name
   - description
   - Purpose: Defines staff roles like Admin, Supervisor, Assistant.

2. Supplier
   - supplier_id (PK)
   - name
   - contact_no
   - email
   - address
   - Purpose: Suppliers provide equipment and consumables.

3. Item
   - item_id (PK)
   - item_name
   - item_type (Equipment/Consumable)
   - description
   - unit_price
   - min_stock_level
   - Purpose: Represents both equipment and consumables.

4. Lab
   - lab_id (PK)
   - lab_name
   - lab_type (Chemistry/Physics)
   - location
   - Purpose: Represents labs where experiments are conducted.

5. Staff
   - staff_id (PK)
   - name
   - role_id (FK -> Roles)
   - contact_no
   - email
   - lab_id (FK -> Lab)
   - Purpose: Staff members who manage labs, assign experiments, and issue inventory.

6. Inventory
   - inventory_id (PK)
   - item_id (FK -> Item)
   - lab_id (FK -> Lab)
   - quantity
   - status (Available/In Use/Maintenance)
   - last_updated
   - Purpose: Tracks items stored in labs with current quantity and status.

7. Order
   - order_id (PK)
   - supplier_id (FK -> Supplier)
   - order_date
   - delivery_date
   - total_cost
   - status (Pending/Received/Cancelled)
   - Purpose: Records orders made to suppliers.

8. Order_Item (Junction Table)
   - order_id (FK -> Order)
   - item_id (FK -> Item)
   - quantity_ordered
   - cost_per_unit
   - PK: (order_id, item_id)
   - Purpose: M:N relationship between orders and items.

9. Experiment
   - experiment_id (PK)
   - experiment_name
   - lab_id (FK -> Lab)
   - staff_id (FK -> Staff)
   - description
   - experiment_date
   - Purpose: Represents experiments conducted in labs.

10. Student
    - student_id (PK)
    - name
    - lab_id (FK -> Lab)
    - assigned_staff_id (FK -> Staff)
    - Purpose: Students assigned to labs and staff supervisors.

11. Experiment_Inventory (Junction Table)
    - experiment_id (FK -> Experiment)
    - inventory_id (FK -> Inventory)
    - quantity_used
    - PK: (experiment_id, inventory_id)
    - Purpose: Tracks which inventory items are used in which experiments (M:N).

12. Maintenance_Log
    - maintenance_id (PK)
    - inventory_id (FK -> Inventory)
    - staff_id (FK -> Staff)
    - log_date
    - description
    - status (Pending/Completed)
    - Purpose: Tracks maintenance activities on inventory items.

------------------------------------------
Relationships and Cardinalities:

1. Staff -> Roles
   - Many staff can have the same role (1:N)
   
2. Staff -> Lab
   - One staff can be assigned to one lab (1:1 or 1:N if assistants included)
   
3. Supplier -> Item (via Order and Order_Item)
   - Many suppliers can supply many items (M:N)
   
4. Lab -> Inventory
   - One lab can hold many inventory items (1:N)
   
5. Item -> Inventory
   - One item can be in many inventory records (1:N)
   
6. Staff -> Experiment
   - One staff can assign many experiments (1:N)
   
7. Experiment -> Inventory (via Experiment_Inventory)
   - Many experiments can use many inventory items (M:N)
   
8. Student -> Lab
   - One student belongs to one lab at a time (1:N)
   
9. Student -> Staff
   - One student is supervised by one staff (1:N)
   
10. Inventory -> Maintenance_Log
    - One inventory item can have many maintenance logs (1:N)

------------------------------------------
Notes:
- Roles table allows dynamic addition of new staff roles.
- Inventory tracks both equipment and consumables in a single table.
- Experiments can only use items present in the inventory.
- Maintenance logs are linked to inventory items, not directly to experiments.
- Orders and Order_Item tables allow tracking which items were ordered from which supplier and quantity.
