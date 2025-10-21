"""
Authentication utilities for NMB BI Portal
Handles user authentication, password hashing, and session management
"""

import streamlit as st
import bcrypt
import re
from datetime import datetime, timedelta
from utils.database import (
    get_user_by_username,
    get_user_by_email,
    create_user,
    update_user_login,
    log_user_action
)

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns: (is_valid, error_message)
    """
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username: str) -> tuple[bool, str]:
    """
    Validate username format
    Returns: (is_valid, error_message)
    """
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 50:
        return False, "Username must be less than 50 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, ""

def authenticate_user(username: str, password: str) -> tuple[bool, str, dict]:
    """
    Authenticate user with username and password
    Returns: (success, message, user_data)
    """
    try:
        # Get user from database
        user = get_user_by_username(username)
        
        if not user:
            return False, "Invalid username or password", None
        
        # Check if user is active
        if not user.is_active:
            return False, "Account is inactive. Contact administrator.", None
        
        # Verify password
        if not verify_password(password, user.password_hash):
            return False, "Invalid username or password", None
        
        # Update login timestamp
        update_user_login(user.user_id)
        
        # Log successful login
        log_user_action(user.user_id, user.username, 'login')
        
        # Return user data
        user_data = {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role_level': user.role_level,
            'department': user.department
        }
        
        return True, "Login successful", user_data
        
    except Exception as e:
        return False, f"Authentication error: {str(e)}", None

def register_user(username: str, email: str, password: str, first_name: str = None, 
                 last_name: str = None, role_level: int = 4, department: str = None) -> tuple[bool, str]:
    """
    Register new user
    Returns: (success, message)
    """
    try:
        # Validate username
        valid, msg = validate_username(username)
        if not valid:
            return False, msg
        
        # Validate email
        if not validate_email(email):
            return False, "Invalid email format"
        
        # Validate password
        valid, msg = validate_password_strength(password)
        if not valid:
            return False, msg
        
        # Check if username already exists
        if get_user_by_username(username):
            return False, "Username already exists"
        
        # Check if email already exists
        if get_user_by_email(email):
            return False, "Email already registered"
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user
        user = create_user(
            username=username,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role_level=role_level,
            department=department
        )
        
        # Log registration
        log_user_action(user.user_id, user.username, 'register')
        
        return True, "Registration successful"
        
    except Exception as e:
        return False, f"Registration error: {str(e)}"

def init_session():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if 'role_level' not in st.session_state:
        st.session_state.role_level = None
    
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    
    if 'first_name' not in st.session_state:
        st.session_state.first_name = None
    
    if 'last_name' not in st.session_state:
        st.session_state.last_name = None

def login_user(user_data: dict):
    """Set session state for logged-in user"""
    st.session_state.authenticated = True
    st.session_state.user_id = user_data['user_id']
    st.session_state.username = user_data['username']
    st.session_state.user_email = user_data['email']
    st.session_state.first_name = user_data.get('first_name')
    st.session_state.last_name = user_data.get('last_name')
    st.session_state.role_level = user_data['role_level']
    st.session_state.department = user_data.get('department')

def logout_user():
    """Clear session state and log out user"""
    if st.session_state.get('user_id') and st.session_state.get('username'):
        log_user_action(st.session_state.user_id, st.session_state.username, 'logout')
    
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.user_email = None
    st.session_state.first_name = None
    st.session_state.last_name = None
    st.session_state.role_level = None
    st.session_state.department = None

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user() -> dict:
    """Get current user data from session"""
    if not is_authenticated():
        return None
    
    return {
        'user_id': st.session_state.get('user_id'),
        'username': st.session_state.get('username'),
        'email': st.session_state.get('user_email'),
        'first_name': st.session_state.get('first_name'),
        'last_name': st.session_state.get('last_name'),
        'role_level': st.session_state.get('role_level'),
        'department': st.session_state.get('department')
    }

def get_role_name(role_level: int) -> str:
    """Get role name from role level"""
    role_names = {
        1: "Executive",
        2: "Manager",
        3: "Analyst",
        4: "Read-Only",
        5: "External Stakeholder"
    }
    return role_names.get(role_level, "Unknown")

def check_permission(required_level: int) -> bool:
    """
    Check if current user has required permission level
    Lower role_level = higher privileges (1=Executive, 5=External)
    """
    if not is_authenticated():
        return False
    
    user_level = st.session_state.get('role_level', 99)
    return user_level <= required_level

def require_auth(required_level: int = 5):
    """
    Decorator/function to require authentication and minimum role level
    Usage in dashboard: require_auth(3) to require Analyst level or higher
    """
    if not is_authenticated():
        st.warning("🔒 Please log in to access this dashboard")
        st.stop()
    
    if not check_permission(required_level):
        st.error(f"⛔ Insufficient permissions. This dashboard requires {get_role_name(required_level)} level access or higher.")
        st.info(f"Your access level: {get_role_name(st.session_state.get('role_level'))}")
        st.stop()

def can_export() -> bool:
    """Check if current user can export data"""
    if not is_authenticated():
        return False
    
    role_level = st.session_state.get('role_level', 99)
    # Executives (1) and Managers (2) can export
    return role_level <= 2

def can_view_dashboard(dashboard_name: str) -> bool:
    """Check if user can view specific dashboard based on role"""
    if not is_authenticated():
        return False
    
    role_level = st.session_state.get('role_level', 99)
    
    # Define dashboard access levels
    dashboard_access = {
        'Executive Summary': 5,  # All roles
        'Active Email Accounts': 3,  # Analyst and above
        'Account Activity': 3,  # Analyst and above
        'Customer Metrics': 2,  # Manager and above
        'Quarterly Performance': 5,  # All roles
        'Campaign Analysis': 3,  # Analyst and above
        'Customer Engagement Analytics': 2,  # Manager and above
        'Sentiment Analysis': 2,  # Manager and above
        'Social Media Analytics': 3,  # Analyst and above
    }
    
    required_level = dashboard_access.get(dashboard_name, 1)  # Default to Executive only
    return role_level <= required_level

def get_accessible_dashboards() -> list:
    """Get list of dashboards accessible to current user"""
    if not is_authenticated():
        return []
    
    all_dashboards = [
        'Executive Summary',
        'Active Email Accounts',
        'Account Activity',
        'Customer Metrics',
        'Quarterly Performance',
        'Campaign Analysis',
        'Customer Engagement Analytics',
        'Sentiment Analysis',
        'Social Media Analytics'
    ]
    
    return [d for d in all_dashboards if can_view_dashboard(d)]

def display_user_info():
    """Display current user info in sidebar"""
    if is_authenticated():
        user = get_current_user()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 User Info")
        
        full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        if full_name:
            st.sidebar.write(f"**{full_name}**")
        else:
            st.sidebar.write(f"**{user['username']}**")
        
        st.sidebar.write(f"Role: {get_role_name(user['role_level'])}")
        
        if user.get('department'):
            st.sidebar.write(f"Department: {user['department']}")
        
        if st.sidebar.button("🚪 Logout", key="logout_btn"):
            logout_user()
            st.rerun()
