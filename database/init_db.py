"""
Database initialization script
Run this to set up the database schema and create default admin user
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import init_database, test_database_connection
from utils.auth import hash_password
import streamlit as st

def main():
    """Initialize database"""
    st.set_page_config(page_title="Database Setup", page_icon="🔧", layout="wide")
    
    st.title("🔧 Database Initialization")
    
    st.info("""
    This tool initializes the PostgreSQL database for the NMB BI Portal.
    
    **What it does:**
    - Creates all necessary tables (users, roles, bookmarks, favorites, notifications, audit_log)
    - Sets up indexes for performance
    - Inserts default roles (Executive, Manager, Analyst, Read-Only, External)
    - Creates default admin user (username: admin, password: Admin@123456)
    
    **⚠️ Warning:** This will execute the schema.sql file. Only run once or after database reset.
    """)
    
    st.markdown("---")
    
    # Test connection first
    st.markdown("### Step 1: Test Database Connection")
    
    if st.button("Test Connection", key="test_conn"):
        with st.spinner("Testing database connection..."):
            success, message = test_database_connection()
            
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
                st.stop()
    
    st.markdown("---")
    
    # Initialize database
    st.markdown("### Step 2: Initialize Database Schema")
    
    st.warning("⚠️ This will create/update all database tables. Proceed with caution in production.")
    
    if st.button("Initialize Database", key="init_db"):
        with st.spinner("Initializing database..."):
            success, message = init_database()
            
            if success:
                st.success(f"✅ {message}")
                
                st.balloons()
                
                st.markdown("---")
                st.markdown("### ✅ Database Initialized Successfully!")
                
                st.info("""
                **Default Admin Account:**
                - **Username:** admin
                - **Password:** Admin@123456
                - **Role:** Executive (Level 1)
                - **Email:** admin@nmbz.co.zw
                
                **⚠️ IMPORTANT:** Change the admin password after first login!
                
                **Next Steps:**
                1. Navigate to the Login page
                2. Log in with the admin credentials
                3. Change your password in Profile Settings
                4. Create additional user accounts as needed
                """)
                
            else:
                st.error(f"❌ {message}")
                st.error("Database initialization failed. Check error message above.")
    
    st.markdown("---")
    
    # View database info
    st.markdown("### Database Information")
    
    db_url = os.environ.get('DATABASE_URL', 'Not set')
    if db_url:
        # Mask password for security
        if '@' in db_url:
            parts = db_url.split('@')
            masked_url = f"{parts[0].split(':')[0]}://***:***@{parts[1]}"
        else:
            masked_url = "***"
        
        st.code(f"Database URL: {masked_url}")
    else:
        st.error("DATABASE_URL environment variable not set!")
    
    st.code(f"Host: {os.environ.get('PGHOST', 'Not set')}")
    st.code(f"Port: {os.environ.get('PGPORT', 'Not set')}")
    st.code(f"Database: {os.environ.get('PGDATABASE', 'Not set')}")
    st.code(f"User: {os.environ.get('PGUSER', 'Not set')}")

if __name__ == "__main__":
    main()
