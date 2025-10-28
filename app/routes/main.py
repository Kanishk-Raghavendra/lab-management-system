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
    """Main dashboard, protected by login."""
    # We must use 'main_routes.dashboard' in url_for
    return render_template('dashboard.html', title='Dashboard')

@main_routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if current_user.is_authenticated:
        return redirect(url_for('main_routes.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            db_conn = current_app.db_pool.get_connection()
            cursor = db_conn.cursor(dictionary=True)
            
            query = """
                SELECT Staff.*, Roles.role_name 
                FROM Staff 
                JOIN Roles ON Staff.role_id = Roles.role_id 
                WHERE Staff.email = %s
            """
            cursor.execute(query, (email,))
            user_data = cursor.fetchone()
            
            cursor.close()
            db_conn.close()
            
            # !! REMEMBER: This checks plaintext.
            # Change to bcrypt.check_password_hash for production
            if user_data and user_data['password_hash'] == password:
                
                user = User(
                    staff_id=user_data['staff_id'],
                    email=user_data['email'],
                    name=user_data['name'],
                    role_name=user_data['role_name'],
                    lab_id=user_data['lab_id']
                )
                
                login_user(user, remember=request.form.get('remember'))
                flash(f'Welcome back, {user.name}!', 'success')
                
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main_routes.dashboard'))
            else:
                flash('Login Unsuccessful. Please check email and password.', 'danger')
                
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')

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