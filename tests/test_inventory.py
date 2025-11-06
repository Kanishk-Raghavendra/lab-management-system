"""
Test inventory management functionality including:
- Adding inventory items
- Updating inventory
- Deleting inventory
- Low stock alerts
"""
import pytest
from flask import url_for

def test_inventory_list_requires_login(client):
    """Test that inventory list requires authentication."""
    response = client.get('/inventory', follow_redirects=True)
    assert b'Please log in to access this page' in response.data

def test_inventory_list_as_admin(client, auth):
    """Test that admin can view inventory list."""
    auth.login()  # Login as admin
    response = client.get('/inventory')
    assert response.status_code == 200
    assert b'Inventory Management' in response.data

def test_add_inventory_item(client, auth):
    """Test adding a new inventory item."""
    auth.login()  # Login as admin
    
    # Add a new item
    response = client.post('/inventory/new', data={
        'item_id': '1',
        'lab_id': '1',
        'quantity': '10',
        'status': 'Available'
    }, follow_redirects=True)
    
    assert b'Inventory item added successfully' in response.data

def test_edit_inventory_item(client, auth):
    """Test editing an existing inventory item."""
    auth.login()  # Login as admin
    
    # First add an item
    client.post('/inventory/new', data={
        'item_id': '1',
        'lab_id': '1',
        'quantity': '10',
        'status': 'Available'
    })
    
    # Then edit it
    response = client.post('/inventory/1/edit', data={
        'quantity': '20',
        'status': 'Available'
    }, follow_redirects=True)
    
    assert b'Inventory updated successfully' in response.data

def test_delete_inventory_item(client, auth):
    """Test deleting an inventory item."""
    auth.login()  # Login as admin
    
    # First add an item
    client.post('/inventory/new', data={
        'item_id': '1',
        'lab_id': '1',
        'quantity': '10',
        'status': 'Available'
    })
    
    # Then delete it
    response = client.post('/inventory/1/delete', follow_redirects=True)
    assert b'Inventory item deleted successfully' in response.data

def test_low_stock_alert(client, auth, db):
    """Test that low stock alerts are created."""
    auth.login()  # Login as admin
    
    # Add an item with quantity below min_stock_level
    response = client.post('/inventory/new', data={
        'item_id': '1',  # Microscope with min_stock_level = 2
        'lab_id': '1',
        'quantity': '1',
        'status': 'Available'
    }, follow_redirects=True)
    
    # Check low stock alert list
    response = client.get('/low_stock')
    assert b'Low Stock Alerts' in response.data
    assert b'Microscope' in response.data

def test_inventory_search_filter(client, auth):
    """Test inventory search and filter functionality."""
    auth.login()  # Login as admin
    
    # Add some test items
    client.post('/inventory/new', data={
        'item_id': '1',
        'lab_id': '1',
        'quantity': '10',
        'status': 'Available'
    })
    
    # Test search
    response = client.get('/inventory?search=Microscope')
    assert b'Microscope' in response.data
    
    # Test filter by lab
    response = client.get('/inventory?lab=1')
    assert b'Chem Lab 1' in response.data
    
    # Test filter by status
    response = client.get('/inventory?status=Available')
    assert b'Available' in response.data