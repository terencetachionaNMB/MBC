import streamlit as st
import pandas as pd
from utils.data_loader import DataLoader
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Marketing & Brand BI Portal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for branding (navy blue and gold theme)
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #003366 0%, #004080 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: #FFD700;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .main-header p {
        color: #FFFFFF;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #FFD700;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-value {
        color: #003366;
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>📊 Marketing & Brand Communications BI Portal</h1>
            <p>Executive Performance Dashboard | Data-Driven Insights for Strategic Decision Making</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize data loader
    @st.cache_resource
    def load_data():
        try:
            loader = DataLoader()
            return loader
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None
    
    loader = load_data()
    
    if loader is None:
        st.error("⚠️ Unable to load data. Please ensure all required CSV files are in the 'data' folder.")
        st.info("""
        Required files:
        - accounts_datadictionary_*.csv
        - RBZ SECTOR CLASSIFICATION LOOKUP TABLE_*.csv
        - GL CATEGORY LOOKUP TABLE_*.csv
        - PRODUCT TYPE LOOKUP TABLE_*.csv
        """)
        return
    
    # Welcome message
    st.markdown("### Welcome to the BI Portal")
    st.markdown("""
    This portal provides comprehensive analytics and insights for the Marketing and Brand Communications department.
    Navigate through the sidebar to access different dashboards and reports.
    """)
    
    # Quick stats
    st.markdown("### Quick Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Total Dashboards</div>
                <div class="metric-value">6</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Data Sources</div>
                <div class="metric-value">4</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Last Updated</div>
                <div class="metric-value">Today</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        current_date = datetime.now().strftime("%B %Y")
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Current Period</div>
                <div class="metric-value" style="font-size: 1.3rem;">{current_date}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Dashboard navigation guide
    st.markdown("### 📑 Available Dashboards")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Executive Level
        - **Executive Summary** - High-level KPIs and performance overview
        - **Quarterly Performance** - Funded accounts tracking Q1-Q3 2025
        - **Campaign Analysis** - Non-funded income campaign insights
        """)
    
    with col2:
        st.markdown("""
        #### Operational Level
        - **Active Email Accounts** - Current account holder contact information
        - **Account Activity** - 90-day activity segmentation analysis
        - **Customer Metrics** - Churn rates and product holdings analysis
        """)
    
    st.markdown("---")
    
    # Data governance section
    st.markdown("### 📋 Data Governance")
    
    with st.expander("View Data Quality Indicators"):
        if loader.accounts_df is not None:
            st.markdown("#### Account Data")
            st.write(f"Total Records: {len(loader.accounts_df):,}")
            st.write(f"Columns: {len(loader.accounts_df.columns)}")
            
        if loader.sector_df is not None:
            st.markdown("#### RBZ Sector Classification")
            st.write(f"Total Records: {len(loader.sector_df):,}")
            
        if loader.gl_df is not None:
            st.markdown("#### GL Categories")
            st.write(f"Total Records: {len(loader.gl_df):,}")
            
        if loader.product_df is not None:
            st.markdown("#### Product Types")
            st.write(f"Total Records: {len(loader.product_df):,}")
    
    with st.expander("Data Refresh Information"):
        st.markdown("""
        **Data Update Frequency:** Daily  
        **Last Refresh:** October 21, 2025  
        **Source System:** Core Banking System  
        **Data Retention:** 24 months rolling  
        """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 2rem; border-top: 1px solid #eee; margin-top: 2rem;">
            <p>Marketing & Brand Communications | Business Intelligence Portal</p>
            <p style="font-size: 0.8rem;">Powered by Streamlit | Data as of October 21, 2025</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
