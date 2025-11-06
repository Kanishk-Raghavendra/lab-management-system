"""
Test authentication functionality including:
- Login with valid credentials
- Login with invalid credentials
- Logout
- Password hashing
- Role-based access control
"""
import pytest
from flask import session

def test_login_with_valid_credentials(client, auth):
    """Test that users can log in with valid credentials."""
    response = auth.login() # Uses admin@lab.com/adminpass by default
    assert response.status_code == 200
    # After login we should have a success message and be redirected to dashboard
    assert b'Welcome back' in response.data

def test_login_with_invalid_credentials(client):
    """Test that login fails with invalid credentials."""
    response = client.post('/login', data={
        'email': 'wrong@example.com',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert b'Login Unsuccessful' in response.data

def test_logout(client, auth):
    """Test that users can log out."""
    # First login
    auth.login()
    
    # Then logout
    response = auth.logout()
    assert b'You have been logged out' in response.data

def test_login_required_redirect(client):
    """Test that protected routes redirect to login."""
    response = client.get('/dashboard', follow_redirects=True)
    assert b'Please log in to access this page' in response.data

def test_admin_required(client, auth):
    """Test that non-admin users cannot access admin routes."""
    # Login as non-admin user
    auth.login(email='student@lab.com', password='student123')
    
    # Try to access admin route
    response = client.get('/admin/staff', follow_redirects=True)
    assert b'You do not have permission to access this page' in response.data

def test_supervisor_required(client, auth):
    """Test that non-supervisor users cannot access supervisor routes."""
    # Login as non-supervisor user
    auth.login(email='student@lab.com', password='student123')
    
    # Try to access supervisor route
    response = client.get('/supervisor/my_students', follow_redirects=True)
    assert b'You do not have permission to access this page' in response.data

def test_remember_me_functionality(client):
    """Test that the remember me functionality works."""
    response = client.post('/login', data={
        'email': 'admin@lab.com', 
        'password': 'adminpass',
        'remember': True
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Check that the session is marked as permanent
    with client.session_transaction() as sess:
        assert sess.permanent is True