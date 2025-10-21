import streamlit as st
from pathlib import Path

def apply_nmb_branding():
    """Apply NMB branding: logo, hide Streamlit footer, add custom footer"""
    
    # Custom CSS to hide Streamlit footer and add custom styling
    st.markdown("""
        <style>
        /* Hide Streamlit footer */
        footer {visibility: hidden;}
        
        /* Hide Streamlit menu */
        #MainMenu {visibility: hidden;}
        
        /* Logo styling */
        .nmb-logo {
            max-width: 180px;
            margin-bottom: 1rem;
        }
        
        /* Custom footer */
        .nmb-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #003366 0%, #004080 100%);
            color: white;
            text-align: center;
            padding: 0.8rem;
            font-size: 0.9rem;
            z-index: 999;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }
        
        .nmb-footer a {
            color: #FFD700;
            text-decoration: none;
        }
        
        /* Adjust main content to not be hidden by fixed footer */
        .main .block-container {
            padding-bottom: 4rem;
        }
        </style>
    """, unsafe_allow_html=True)

def show_nmb_logo():
    """Display NMB logo at the top of the page"""
    # Find the logo file
    logo_path = Path("attached_assets/logo_1_1761020412913.png")
    
    if logo_path.exists():
        st.image(str(logo_path), width=180)
    else:
        st.markdown("### NMB Bank")

def show_nmb_footer():
    """Display custom NMB footer"""
    st.markdown("""
        <div class="nmb-footer">
            Made with ❤️ by NMB Business Intelligence
        </div>
    """, unsafe_allow_html=True)
