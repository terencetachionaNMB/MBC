"""
Login page for NMB BI Portal
Handles user authentication
"""

import streamlit as st
from utils.branding import apply_nmb_branding, show_nmb_logo, show_nmb_footer
from utils.auth import authenticate_user, login_user, init_session, is_authenticated, logout_user
from utils.database import test_database_connection

st.set_page_config(page_title="Login - NMB BI Portal", page_icon="🔐", layout="centered")
apply_nmb_branding()

# Initialize session
init_session()

# If already logged in, show logout option
if is_authenticated():
    show_nmb_logo()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #003366 0%, #004080 100%); 
                padding: 2rem; border-radius: 10px; text-align: center; margin: 2rem 0;">
        <h1 style="color: #FFD700; margin: 0; font-size: 2.5rem;">✅ Already Logged In</h1>
        <p style="color: white; margin: 1rem 0 0 0; font-size: 1.2rem;">
            Welcome back, <strong>{}</strong>!
        </p>
    </div>
    """.format(st.session_state.get('username', 'User')), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info(f"""
        **You are logged in as:**
        - Username: {st.session_state.get('username')}
        - Email: {st.session_state.get('user_email')}
        - Role: {st.session_state.get('role_level')}
        """)
        
        if st.button("🚪 Logout", key="logout_main", use_container_width=True):
            logout_user()
            st.success("Logged out successfully!")
            st.rerun()
        
        st.markdown("---")
        
        if st.button("📊 Go to Dashboards", key="go_dashboards", use_container_width=True):
            st.switch_page("app.py")
    
    show_nmb_footer()
    st.stop()

# Show login form
show_nmb_logo()

st.markdown("""
<div style="background: linear-gradient(135deg, #003366 0%, #004080 100%); 
            padding: 2rem; border-radius: 10px; text-align: center; margin: 2rem 0;">
    <h1 style="color: #FFD700; margin: 0; font-size: 2.8rem;">🔐 Login</h1>
    <p style="color: white; margin: 1rem 0 0 0; font-size: 1.2rem;">
        NMB Bank Business Intelligence Portal
    </p>
</div>
""", unsafe_allow_html=True)

# Test database connection status
connection_status = st.empty()

with st.spinner("Checking database connection..."):
    db_success, db_message = test_database_connection()
    
    if not db_success:
        connection_status.error(f"⚠️ Database Connection Issue: {db_message}")
        st.info("""
        **Database not initialized or connection failed.**
        
        Please initialize the database first:
        1. Navigate to the Database Setup page
        2. Click "Initialize Database"
        3. Return here to log in
        """)
        show_nmb_footer()
        st.stop()
    else:
        connection_status.success("✅ Database connected")

st.markdown("---")

# Login form
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    with st.form("login_form"):
        st.markdown("### Enter your credentials")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        submit = st.form_submit_button("🔑 Login", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                with st.spinner("Authenticating..."):
                    success, message, user_data = authenticate_user(username, password)
                    
                    if success:
                        # Log in user
                        login_user(user_data)
                        
                        st.success(f"✅ {message}")
                        st.success(f"Welcome, {user_data.get('first_name') or username}!")
                        
                        st.balloons()
                        
                        # Redirect to home page
                        st.info("Redirecting to dashboards...")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
    
    st.markdown("---")
    
    # Additional options
    st.markdown("### Need help?")
    
    with st.expander("🔑 Default Admin Credentials"):
        st.info("""
        **Default Admin Account (if database just initialized):**
        - Username: `admin`
        - Password: `Admin@123456`
        
        ⚠️ **Change password after first login!**
        """)
    
    with st.expander("❓ Forgot Password"):
        st.info("""
        Password reset feature coming soon.
        
        For now, contact the BI team at:
        - Email: bi@nmbz.co.zw
        - Phone: [Internal Extension]
        """)
    
    with st.expander("👥 Request Access"):
        st.info("""
        To request access to the BI Portal:
        
        1. Contact your department head for approval
        2. Email bi@nmbz.co.zw with:
           - Your full name
           - Department
           - NMB email address
           - Required access level
        3. Account will be created within 1 business day
        """)

show_nmb_footer()
