from flask import (render_template, redirect, url_for, flash, 
                   request, current_app, abort)
from flask_login import login_user, logout_user, login_required, current_user
import mysql.connector

from app import bcrypt
from app.models.user import User
from app.decorators import admin_required, supervisor_required
from . import main_routes_blueprint

# We use the blueprint to define routes, not 'main'
@main_routes_blueprint.route('/')
@main_routes_blueprint.route('/dashboard')
@login_required
def dashboard():
    """
    Main dashboard.
    Redirects Students to their own dashboard.
    Shows Staff the main dashboard.
    """
    if current_user.is_student():
        return render_template('student_dashboard.html', title='Dashboard')
    
    # For Staff (Admin, Supervisor, Assistant)
    return render_template('dashboard.html', title='Dashboard')

@main_routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login for BOTH Staff and Students."""
    if current_user.is_authenticated:
        return redirect(url_for('main_routes.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        db_conn = None
        cursor = None
        try:
            db_conn = current_app.db_pool.get_connection()
            cursor = db_conn.cursor(dictionary=True)
            
            user = None
            user_data = None
            
            # 1. Check Staff table first
            query_staff = """
                SELECT Staff.*, Roles.role_name 
                FROM Staff 
                JOIN Roles ON Staff.role_id = Roles.role_id 
                WHERE Staff.email = %s
            """
            cursor.execute(query_staff, (email,))
            user_data = cursor.fetchone()
            
            if user_data and user_data['password_hash'] == password:
                user = User(
                    user_id=f"staff_{user_data['staff_id']}",
                    user_type='Staff',
                    email=user_data['email'],
                    name=user_data['name'],
                    role_name=user_data['role_name'],
                    lab_id=user_data['lab_id']
                )
            
            # 2. If not found in Staff, check Student table
            if not user:
                query_student = "SELECT * FROM Student WHERE email = %s"
                cursor.execute(query_student, (email,))
                user_data = cursor.fetchone()
                
                if user_data and user_data['password_hash'] == password:
                    user = User(
                        user_id=f"student_{user_data['student_id']}",
                        user_type='Student',
                        email=user_data['email'],
                        name=user_data['name'],
                        lab_id=user_data['lab_id']
                    )
            
            # 3. If user was found and password matched
            if user:
                login_user(user, remember=request.form.get('remember'))
                flash(f'Welcome back, {user.name}!', 'success')
                
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main_routes.dashboard'))
            else:
                flash('Login Unsuccessful. Please check email and password.', 'danger')
                
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            if cursor: cursor.close()
            if db_conn: db_conn.close()

    return render_template('login.html', title='Login')


@main_routes_blueprint.route('/logout')
def logout():
    """Logs the user out."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main_routes.login'))

# --- Example Protected Routes ---

@main_routes_blueprint.route('/admin_only')
@login_required
@admin_required
def admin_page():
    return "<h1>Admin Page</h1><p>Only admins can see this.</p>"

@main_routes_blueprint.route('/supervisor_stuff')
@login_required
@supervisor_required
def supervisor_page():
    return "<h1>Supervisor Page</h1><p>Supervisors and Admins can see this.</p>"

# --- Inventory CRUD Routes ---

@main_routes_blueprint.route('/inventory')
@login_required
def inventory_list():
    """
    (R)EAD: Displays a list of all inventory items from all labs.
    This query uses JOINs.
    """
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)
        
        # JOIN query to get item names and lab names
        query = """
            SELECT 
                inv.inventory_id,
                i.item_name,
                l.lab_name,
                inv.quantity,
                inv.status
            FROM Inventory inv
            JOIN Item i ON inv.item_id = i.item_id
            JOIN Lab l ON inv.lab_id = l.lab_id
            ORDER BY l.lab_name, i.item_name
        """
        cursor.execute(query)
        inventory_items = cursor.fetchall()
        
        cursor.close()
        db_conn.close()
        
        return render_template('inventory_list.html', 
                               title='Inventory', 
                               inventory_items=inventory_items)
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.dashboard'))


@main_routes_blueprint.route('/inventory/edit/<int:inventory_id>', methods=['GET', 'POST'])
@login_required
@supervisor_required
def edit_inventory(inventory_id):
    """
    (U)PDATE: Shows a form to edit an inventory item (GET)
    and processes the form submission (POST).
    """
    db_conn = None  # Initialize to None
    cursor = None   # Initialize to None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)

        if request.method == 'POST':
            # --- UPDATE LOGIC ---
            new_quantity = request.form.get('quantity')
            new_status = request.form.get('status')
            
            update_query = """
                UPDATE Inventory 
                SET quantity = %s, status = %s, last_updated = NOW()
                WHERE inventory_id = %s
            """
            cursor.execute(update_query, (new_quantity, new_status, inventory_id))
            db_conn.commit()
            
            flash('Inventory item updated successfully!', 'success')
            return redirect(url_for('main_routes.inventory_list'))

        # --- GET LOGIC (if not POST) ---
        get_query = """
            SELECT inv.inventory_id, i.item_name, inv.quantity, inv.status
            FROM Inventory inv
            JOIN Item i ON inv.item_id = i.item_id
            WHERE inv.inventory_id = %s
        """
        cursor.execute(get_query, (inventory_id,))
        
        # This line defines the 'item' variable
        item = cursor.fetchone() 
        
        if not item:
            abort(404) # Not found
            
        # This line uses 'item' after it's defined
        return render_template('inventory_edit.html', title='Edit Inventory', item=item)
        
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.inventory_list'))
    finally:
        # This block ensures the connection is always closed
        if cursor:
            cursor.close()
        if db_conn:
            db_conn.close()

@main_routes_blueprint.route('/inventory/delete/<int:inventory_id>', methods=['POST'])
@login_required
@supervisor_required # Only Supervisors or Admins can delete
def delete_inventory(inventory_id):
    """
    (D)ELETE: Deletes an inventory item from a lab.
    """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor()
        
        # Try to delete. DB will throw error 1451 if FK is violated.
        cursor.execute("DELETE FROM Inventory WHERE inventory_id = %s", (inventory_id,))
        db_conn.commit()
        
        flash('Inventory item removed successfully.', 'success')
    except mysql.connector.Error as err:
        if err.errno == 1451: # Foreign Key constraint fail
            flash('Cannot remove this item. It is in use in an experiment or maintenance log.', 'danger')
        else:
            flash(f'An error occurred: {err}', 'danger')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()
        
    return redirect(url_for('main_routes.inventory_list'))            

# --- Item CRUD Routes (Admin Only) ---

@main_routes_blueprint.route('/item')
@login_required
@admin_required
def item_list():
    """ (R)EAD: List all master items. """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Item ORDER BY item_name")
        items = cursor.fetchall()
        return render_template('item_list.html', title="Manage Items", items=items)
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.dashboard'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/item/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_item():
    """ (C)REATE: Add a new master item. """
    db_conn = None
    cursor = None
    try:
        if request.method == 'POST':
            name = request.form.get('item_name')
            item_type = request.form.get('item_type')
            desc = request.form.get('description')
            price = request.form.get('unit_price')
            min_stock = request.form.get('min_stock_level')
            
            query = """
                INSERT INTO Item (item_name, item_type, description, unit_price, min_stock_level)
                VALUES (%s, %s, %s, %s, %s)
            """
            db_conn = current_app.db_pool.get_connection()
            cursor = db_conn.cursor()
            cursor.execute(query, (name, item_type, desc, price, min_stock))
            db_conn.commit()
            
            flash(f'Item "{name}" created successfully!', 'success')
            return redirect(url_for('main_routes.item_list'))
            
        # GET request shows the form
        return render_template('item_form.html', title="New Item", form_action=url_for('main_routes.new_item'), item=None)
        
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        # Rollback in case of error
        if db_conn: db_conn.rollback()
        return redirect(url_for('main_routes.item_list'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_item(item_id):
    """ (U)PDATE: Edit a master item. """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            name = request.form.get('item_name')
            item_type = request.form.get('item_type')
            desc = request.form.get('description')
            price = request.form.get('unit_price')
            min_stock = request.form.get('min_stock_level')
            
            query = """
                UPDATE Item SET 
                item_name = %s, item_type = %s, description = %s, 
                unit_price = %s, min_stock_level = %s
                WHERE item_id = %s
            """
            cursor.execute(query, (name, item_type, desc, price, min_stock, item_id))
            db_conn.commit()
            
            flash(f'Item "{name}" updated successfully!', 'success')
            return redirect(url_for('main_routes.item_list'))

        # GET request: fetch item to pre-fill form
        cursor.execute("SELECT * FROM Item WHERE item_id = %s", (item_id,))
        item = cursor.fetchone()
        if not item:
            abort(404)
        
        return render_template('item_form.html', title="Edit Item", form_action=url_for('main_routes.edit_item', item_id=item_id), item=item)
        
    except Exception as e:
        if db_conn: db_conn.rollback()
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.item_list'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/item/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_item(item_id):
    """ (D)ELETE: Delete a master item. """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor()
        
        cursor.execute("DELETE FROM Item WHERE item_id = %s", (item_id,))
        db_conn.commit()
        
        flash('Item deleted successfully!', 'success')
    except mysql.connector.Error as err:
        if err.errno == 1451: # Foreign Key constraint fail
            flash('Cannot delete this item. It is currently in use in an inventory or order.', 'danger')
        else:
            flash(f'An error occurred: {err}', 'danger')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()
        
    return redirect(url_for('main_routes.item_list'))

# --- Order Management Routes (Supervisor+) ---

@main_routes_blueprint.route('/orders')
@login_required
@supervisor_required
def order_list():
    """ (R)EAD: List all orders. """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)
        
        query = """
            SELECT o.order_id, s.name as supplier_name, l.lab_name, 
                   o.order_date, o.delivery_date, o.total_cost, o.status
            FROM `Order` o
            JOIN Supplier s ON o.supplier_id = s.supplier_id
            JOIN Lab l ON o.lab_id = l.lab_id
            ORDER BY o.order_date DESC
        """
        cursor.execute(query)
        orders = cursor.fetchall()
        return render_template('order_list.html', title="Manage Orders", orders=orders)
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.dashboard'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/order/new', methods=['GET', 'POST'])
@login_required
@supervisor_required
def new_order():
    """ (C)REATE: Create a new order (calls a Stored Procedure). """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)

        if request.method == 'POST':
            supplier_id = request.form.get('supplier_id')
            lab_id = request.form.get('lab_id')
            order_date = request.form.get('order_date')
            delivery_date_raw = request.form.get('delivery_date')
            total_cost = request.form.get('total_cost')

            delivery_date = delivery_date_raw if delivery_date_raw else None
            
            # Call the Stored Procedure 'Add_Order'
            cursor.callproc('Add_Order', [supplier_id, lab_id, order_date, delivery_date, total_cost])
            db_conn.commit()
            
            # Get the ID of the order we just created
            cursor.execute("SELECT LAST_INSERT_ID() AS new_id")
            new_order_id = cursor.fetchone()['new_id']
            
            flash('New order created successfully! Now add items to it.', 'success')
            return redirect(url_for('main_routes.view_order', order_id=new_order_id))

        # GET request: Fetch suppliers and labs for the dropdowns
        cursor.execute("SELECT supplier_id, name FROM Supplier ORDER BY name")
        suppliers = cursor.fetchall()
        
        # Only show labs the user is associated with (if not admin)
        if current_user.is_admin():
            cursor.execute("SELECT lab_id, lab_name FROM Lab ORDER BY lab_name")
        else:
            # Supervisor is tied to one lab
            query = "SELECT lab_id, lab_name FROM Lab WHERE lab_id = %s"
            cursor.execute(query, (current_user.lab_id,))
            
        labs = cursor.fetchall()
        
        return render_template('order_form.html', title="New Order", suppliers=suppliers, labs=labs)
        
    except Exception as e:
        if db_conn: db_conn.rollback()
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.order_list'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/order/<int:order_id>')
@login_required
@supervisor_required
def view_order(order_id):
    """ (R)EAD: View a single order, its items, and add new items. """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)

        # Get Order Details
        query = """
            SELECT o.*, s.name as supplier_name, l.lab_name
            FROM `Order` o
            JOIN Supplier s ON o.supplier_id = s.supplier_id
            JOIN Lab l ON o.lab_id = l.lab_id
            WHERE o.order_id = %s
        """
        cursor.execute(query, (order_id,))
        order = cursor.fetchone()
        
        if not order:
            abort(404)

        # Get Items on the Order
        query_items = """
            SELECT oi.item_id, i.item_name, oi.quantity_ordered, oi.cost_per_unit
            FROM Order_Item oi
            JOIN Item i ON oi.item_id = i.item_id
            WHERE oi.order_id = %s
        """
        cursor.execute(query_items, (order_id,))
        order_items = cursor.fetchall()
        
        # Get all master items to populate the "Add Item" dropdown
        cursor.execute("SELECT item_id, item_name, unit_price FROM Item ORDER BY item_name")
        all_items = cursor.fetchall()
        
        return render_template('order_view.html', title="View Order", 
                               order=order, order_items=order_items, all_items=all_items)
        
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.order_list'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/order/<int:order_id>/add_item', methods=['POST'])
@login_required
@supervisor_required
def add_item_to_order(order_id):
    """ (U)PDATE: Adds a line item to an existing order. """
    db_conn = None
    cursor = None
    try:
        item_id = request.form.get('item_id')
        quantity = request.form.get('quantity')
        cost = request.form.get('cost_per_unit')
        
        query = """
            INSERT INTO Order_Item (order_id, item_id, quantity_ordered, cost_per_unit)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                quantity_ordered = quantity_ordered + VALUES(quantity_ordered),
                cost_per_unit = VALUES(cost_per_unit)
        """
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor()
        cursor.execute(query, (order_id, item_id, quantity, cost))
        db_conn.commit()
        
        flash('Item added to order.', 'success')
    except Exception as e:
        if db_conn: db_conn.rollback()
        flash(f'An error occurred: {e}', 'danger')
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()
        
    return redirect(url_for('main_routes.view_order', order_id=order_id))

@main_routes_blueprint.route('/order/<int:order_id>/receive', methods=['POST'])
@login_required
@supervisor_required
def receive_order(order_id):
    """ 
    (U)PDATE: Mark an order as 'Received'.
    This will fire 'trg_update_inventory_on_order_receive' in MySQL.
    """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor()
        
        query = "UPDATE `Order` SET status = 'Received', delivery_date = CURDATE() WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        db_conn.commit()
        
        flash('Order marked as "Received". Inventory has been updated.', 'success')
    except Exception as e:
        if db_conn: db_conn.rollback()
        flash(f'An error occurred: {e}', 'danger')
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()
        
    return redirect(url_for('main_routes.view_order', order_id=order_id))

# --- Experiment Management Routes (Supervisor+) ---

@main_routes_blueprint.route('/experiments')
@login_required
@supervisor_required
def experiment_list():
    """ (R)EAD: List all experiments. """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)
        
        query = """
            SELECT e.experiment_id, e.experiment_name, l.lab_name, s.name as staff_name, e.experiment_date
            FROM Experiment e
            JOIN Lab l ON e.lab_id = l.lab_id
            JOIN Staff s ON e.staff_id = s.staff_id
            ORDER BY e.experiment_date DESC
        """
        cursor.execute(query)
        experiments = cursor.fetchall()
        return render_template('experiment_list.html', title="Experiments", experiments=experiments)
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.dashboard'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/experiment/new', methods=['GET', 'POST'])
@login_required
@supervisor_required
def new_experiment():
    """ (C)REATE: Create a new experiment (calls Stored Procedure). """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)

        if request.method == 'POST':
            name = request.form.get('experiment_name')
            lab_id = request.form.get('lab_id')
            description = request.form.get('description')
            staff_id = current_user.id # Assign to logged-in supervisor
            
            # Call the Stored Procedure 'Assign_Experiment'
            cursor.callproc('Assign_Experiment', [name, lab_id, staff_id, description])
            db_conn.commit()
            
            cursor.execute("SELECT LAST_INSERT_ID() AS new_id")
            new_exp_id = cursor.fetchone()['new_id']
            
            flash('New experiment created successfully! Now add inventory items used.', 'success')
            return redirect(url_for('main_routes.view_experiment', experiment_id=new_exp_id))

        # GET request: Fetch labs (and staff, though we use current_user)
        if current_user.is_admin():
            cursor.execute("SELECT lab_id, lab_name FROM Lab ORDER BY lab_name")
        else:
            query = "SELECT lab_id, lab_name FROM Lab WHERE lab_id = %s"
            cursor.execute(query, (current_user.lab_id,))
        labs = cursor.fetchall()
        
        return render_template('experiment_form.html', title="New Experiment", labs=labs)
        
    except Exception as e:
        if db_conn: db_conn.rollback()
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.experiment_list'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/experiment/<int:experiment_id>')
@login_required
@supervisor_required
def view_experiment(experiment_id):
    """ (R)EAD: View a single experiment and its used inventory. """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)

        # Get Experiment Details
        query = """
            SELECT e.*, l.lab_name, s.name as staff_name
            FROM Experiment e
            JOIN Lab l ON e.lab_id = l.lab_id
            JOIN Staff s ON e.staff_id = s.staff_id
            WHERE e.experiment_id = %s
        """
        cursor.execute(query, (experiment_id,))
        experiment = cursor.fetchone()
        if not experiment:
            abort(404)

        # Get Inventory Used in this Experiment
        query_items = """
            SELECT ei.quantity_used, i.item_name, inv.inventory_id
            FROM Experiment_Inventory ei
            JOIN Inventory inv ON ei.inventory_id = inv.inventory_id
            JOIN Item i ON inv.item_id = i.item_id
            WHERE ei.experiment_id = %s
        """
        cursor.execute(query_items, (experiment_id,))
        used_items = cursor.fetchall()
        
        # Get AVAILABLE inventory from that lab to add
        query_avail = """
            SELECT inv.inventory_id, i.item_name, inv.quantity
            FROM Inventory inv
            JOIN Item i ON inv.item_id = i.item_id
            WHERE inv.lab_id = %s AND inv.status = 'Available' AND inv.quantity > 0
            ORDER BY i.item_name
        """
        cursor.execute(query_avail, (experiment['lab_id'],))
        available_inventory = cursor.fetchall()
        
        return render_template('experiment_view.html', title="View Experiment", 
                               experiment=experiment, used_items=used_items, 
                               available_inventory=available_inventory)
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.experiment_list'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/experiment/<int:experiment_id>/add_inventory', methods=['POST'])
@login_required
@supervisor_required
def add_inventory_to_experiment(experiment_id):
    """ 
    (U)PDATE: Adds an inventory item to an experiment.
    This will fire 'trg_reduce_inventory_after_experiment' in MySQL.
    """
    db_conn = None
    cursor = None
    try:
        inventory_id = request.form.get('inventory_id')
        quantity_used = request.form.get('quantity_used')
        
        # Check if available (using our SQL Function)
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor()
        cursor.execute("SELECT Is_Inventory_Available(%s, %s)", (inventory_id, quantity_used))
        is_available = cursor.fetchone()[0]

        if is_available:
            query = """
                INSERT INTO Experiment_Inventory (experiment_id, inventory_id, quantity_used)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (experiment_id, inventory_id, quantity_used))
            db_conn.commit()
            flash('Inventory item added to experiment. Stock has been reduced.', 'success')
        else:
            flash('Not enough stock available for this action.', 'danger')
            
    except Exception as e:
        if db_conn: db_conn.rollback()
        flash(f'An error occurred: {e}', 'danger')
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()
        
    return redirect(url_for('main_routes.view_experiment', experiment_id=experiment_id))

# --- Maintenance Log Routes (Supervisor+) ---

@main_routes_blueprint.route('/maintenance')
@login_required
@supervisor_required
def maintenance_list():
    """ (R)EAD: List all maintenance logs. """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)
        
        query = """
            SELECT m.maintenance_id, i.item_name, inv.inventory_id, l.lab_name, 
                   s.name as logged_by_name, m.log_date, m.description, m.status
            FROM Maintenance_Log m
            JOIN Staff s ON m.staff_id = s.staff_id
            JOIN Inventory inv ON m.inventory_id = inv.inventory_id
            JOIN Item i ON inv.item_id = i.item_id
            JOIN Lab l ON inv.lab_id = l.lab_id
            ORDER BY m.log_date DESC
        """
        cursor.execute(query)
        logs = cursor.fetchall()
        return render_template('maintenance_list.html', title="Maintenance Logs", logs=logs)
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.dashboard'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/maintenance/new', methods=['GET', 'POST'])
@login_required
@supervisor_required
def new_maintenance_log():
    """ 
    (C)REATE: Create a new maintenance log (calls Stored Procedure).
    This will also trigger an inventory status update.
    """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)

        if request.method == 'POST':
            inventory_id = request.form.get('inventory_id')
            description = request.form.get('description')
            staff_id = current_user.id
            
            # Call the Stored Procedure 'Log_Maintenance'
            cursor.callproc('Log_Maintenance', [inventory_id, staff_id, description])
            db_conn.commit()
            
            flash('Maintenance log created. Inventory status set to "Maintenance".', 'success')
            return redirect(url_for('main_routes.maintenance_list'))

        # GET request: Fetch 'Available' inventory items to log maintenance for
        if current_user.is_admin():
             query = """
                SELECT inv.inventory_id, i.item_name, l.lab_name
                FROM Inventory inv
                JOIN Item i ON inv.item_id = i.item_id
                JOIN Lab l ON inv.lab_id = l.lab_id
                WHERE inv.status = 'Available'
                ORDER BY l.lab_name, i.item_name
             """
             cursor.execute(query)
        else:
            # Supervisor can only log for their own lab
            query = """
                SELECT inv.inventory_id, i.item_name, l.lab_name
                FROM Inventory inv
                JOIN Item i ON inv.item_id = i.item_id
                JOIN Lab l ON inv.lab_id = l.lab_id
                WHERE inv.status = 'Available' AND inv.lab_id = %s
                ORDER BY i.item_name
            """
            cursor.execute(query, (current_user.lab_id,))
        
        inventory_items = cursor.fetchall()
        
        return render_template('maintenance_form.html', title="New Maintenance Log", inventory_items=inventory_items)
        
    except Exception as e:
        if db_conn: db_conn.rollback()
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.maintenance_list'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/maintenance/complete/<int:maintenance_id>', methods=['POST'])
@login_required
@supervisor_required
def complete_maintenance_log(maintenance_id):
    """ 
    (U)PDATE: Mark a maintenance log as 'Completed' (calls Stored Procedure).
    This will trigger an inventory status update.
    """
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor()
        
        # Call the Stored Procedure 'Complete_Maintenance'
        cursor.callproc('Complete_Maintenance', [maintenance_id, current_user.id])
        db_conn.commit()
        
        flash('Maintenance completed. Inventory status set to "Available".', 'success')
    except Exception as e:
        if db_conn: db_conn.rollback()
        flash(f'An error occurred: {e}', 'danger')
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()
        
    return redirect(url_for('main_routes.maintenance_list'))

# --- Student-Facing Routes ---

@main_routes_blueprint.route('/student/my_lab')
@login_required
def student_my_lab():
    """ (R)EAD: Shows student their lab and supervisor info. """
    if not current_user.is_student():
        abort(403) # Forbidden
        
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)
        
        query = """
            SELECT s.name as student_name, l.lab_name, l.location, st.name as supervisor_name, st.email as supervisor_email
            FROM Student s
            LEFT JOIN Lab l ON s.lab_id = l.lab_id
            LEFT JOIN Staff st ON s.assigned_staff_id = st.staff_id
            WHERE s.student_id = %s
        """
        # We must split the composite ID 'student_XX'
        student_id_int = int(current_user.id.split('_')[1])
        cursor.execute(query, (student_id_int,))
        lab_info = cursor.fetchone()
        
        return render_template('student_my_lab.html', title="My Lab", lab_info=lab_info)
        
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.dashboard'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()

@main_routes_blueprint.route('/student/my_experiments')
@login_required
def student_my_experiments():
    """ (R)EAD: Shows experiments for the student's lab. """
    if not current_user.is_student():
        abort(403)
        
    db_conn = None
    cursor = None
    try:
        db_conn = current_app.db_pool.get_connection()
        cursor = db_conn.cursor(dictionary=True)
        
        query = """
            SELECT e.experiment_name, e.description, e.experiment_date, s.name as supervisor_name
            FROM Experiment e
            JOIN Staff s ON e.staff_id = s.staff_id
            WHERE e.lab_id = %s
            ORDER BY e.experiment_date DESC
        """
        cursor.execute(query, (current_user.lab_id,))
        experiments = cursor.fetchall()
        
        return render_template('student_my_experiments.html', title="Lab Experiments", experiments=experiments)
        
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('main_routes.dashboard'))
    finally:
        if cursor: cursor.close()
        if db_conn: db_conn.close()