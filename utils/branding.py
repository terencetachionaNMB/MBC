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

def show_acknowledgment():
    """Display acknowledgment section for project lead"""
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            border: 3px solid #003366;
        ">
            <h3 style="
                color: #003366;
                text-align: center;
                margin: 0 0 1rem 0;
                font-size: 1.8rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 2px;
            ">🏆 Project Acknowledgment</h3>
            <div style="
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                border-left: 6px solid #003366;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            ">
                <p style="
                    color: #003366;
                    font-size: 1.2rem;
                    text-align: center;
                    margin: 0 0 0.5rem 0;
                    font-weight: 600;
                ">This Business Intelligence Portal represents a significant achievement in delivering data-driven business value.</p>
                <p style="
                    color: #333;
                    font-size: 1.1rem;
                    text-align: center;
                    margin: 1rem 0;
                    line-height: 1.6;
                ">
                    <strong style="color: #003366; font-size: 1.3rem;">Special Recognition:</strong><br>
                    <span style="color: #FFA500; font-size: 1.4rem; font-weight: 700;">Terence Tachiona</span>
                </p>
                <p style="
                    color: #555;
                    font-size: 1rem;
                    text-align: center;
                    margin: 1rem 0 0 0;
                    font-style: italic;
                ">
                    For his exceptional solo effort and unwavering dedication in conceptualizing, developing, and implementing 
                    a comprehensive BI solution that transforms raw banking data into actionable strategic insights, 
                    driving measurable business value for NMB Bank's Marketing and Brand Communications department.
                </p>
                <div style="
                    text-align: center;
                    margin-top: 1.5rem;
                    padding-top: 1rem;
                    border-top: 2px solid #FFD700;
                ">
                    <p style="
                        color: #003366;
                        font-size: 0.95rem;
                        font-weight: 600;
                        margin: 0;
                    ">
                        ⭐ Excellence in Innovation • Leadership in Analytics • Commitment to Business Impact ⭐
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_professional_banner(title, subtitle, icon="📊"):
    """Create a professional banner for pages"""
    return f"""
        <div style="
            background: linear-gradient(135deg, #003366 0%, #004080 100%);
            padding: 2.5rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
            border: 3px solid #FFD700;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: -50px;
                right: -50px;
                width: 200px;
                height: 200px;
                background: rgba(255, 215, 0, 0.1);
                border-radius: 50%;
            "></div>
            <div style="
                position: absolute;
                bottom: -30px;
                left: -30px;
                width: 150px;
                height: 150px;
                background: rgba(255, 215, 0, 0.1);
                border-radius: 50%;
            "></div>
            <h1 style="
                color: #FFD700;
                margin: 0;
                font-size: 2.8rem;
                font-weight: 700;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                position: relative;
                z-index: 1;
            ">{icon} {title}</h1>
            <p style="
                color: #FFFFFF;
                margin: 0.8rem 0 0 0;
                font-size: 1.2rem;
                position: relative;
                z-index: 1;
            ">{subtitle}</p>
        </div>
    """

def create_section_divider(text=""):
    """Create a professional section divider"""
    if text:
        return f"""
            <div style="
                text-align: center;
                margin: 3rem 0 2rem 0;
            ">
                <div style="
                    display: inline-block;
                    background: linear-gradient(135deg, #003366 0%, #004080 100%);
                    color: #FFD700;
                    padding: 0.8rem 2rem;
                    border-radius: 25px;
                    font-weight: 700;
                    font-size: 1.1rem;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    border: 2px solid #FFD700;
                    text-transform: uppercase;
                    letter-spacing: 1.5px;
                ">{text}</div>
            </div>
        """
    else:
        return """
            <div style="
                height: 3px;
                background: linear-gradient(90deg, transparent, #FFD700, transparent);
                margin: 2rem 0;
                border-radius: 2px;
            "></div>
        """
