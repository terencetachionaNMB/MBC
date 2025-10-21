import streamlit as st
import pandas as pd
from utils.data_loader import DataLoader
from utils.data_processor import DataProcessor
from utils.metrics_calculator import MetricsCalculator
from utils.visualization import VisualizationHelper as vh
from utils.branding import apply_nmb_branding, show_nmb_logo, show_nmb_footer
import plotly.graph_objects as go

st.set_page_config(page_title="Executive Summary", page_icon="📊", layout="wide")
apply_nmb_branding()

# NMB Logo
show_nmb_logo()

# Header
st.markdown("""
    <div style="background: linear-gradient(135deg, #003366 0%, #004080 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: #FFD700; margin: 0;">📊 Executive Summary Dashboard</h1>
        <p style="color: white; margin: 0.5rem 0 0 0;">High-level KPIs and Performance Overview</p>
    </div>
""", unsafe_allow_html=True)

# Load data
@st.cache_resource
def load_data():
    return DataLoader()

loader = load_data()

if loader.get_accounts_data() is None:
    st.error("⚠️ No account data available. Please upload the accounts data file to the 'data' folder.")
    st.info("""
    **Required file:** `accounts_data.csv`
    
    This file should contain the actual account records with columns matching the data dictionary schema.
    Place the file in the `data/` folder and refresh the page.
    """)
    st.stop()

processor = DataProcessor(loader)
calculator = MetricsCalculator(processor)

# Get key metrics
total_customers = processor.get_unique_customer_count()
avg_products = processor.get_avg_products_per_customer()
active_accounts, inactive_accounts = processor.get_account_activity_segments()
quarterly_data = processor.get_quarterly_funded_accounts(2025)

# Key Performance Indicators
st.markdown("### 🎯 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Customers",
        value=f"{total_customers:,}",
        delta=None,
        help="Total number of unique customers"
    )

with col2:
    st.metric(
        label="Active Accounts",
        value=f"{len(active_accounts):,}",
        delta=None,
        help="Accounts with transactions in last 90 days"
    )

with col3:
    st.metric(
        label="Avg Products/Customer",
        value=f"{avg_products:.2f}",
        delta=None,
        help="Average products per customer (excl. Account/Card types)"
    )

with col4:
    if len(quarterly_data) > 0:
        latest_q_accounts = quarterly_data.iloc[-1]['funded_accounts']
        st.metric(
            label="Q3 2025 Funded Accounts",
            value=f"{latest_q_accounts:,}",
            delta=None,
            help="Funded accounts in Q3 2025"
        )
    else:
        st.metric(label="Q3 2025 Funded Accounts", value="N/A")

st.markdown("---")

# Two column layout for charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Quarterly Performance Trend")
    
    if len(quarterly_data) > 0:
        fig = vh.create_line_chart(
            quarterly_data,
            'quarter',
            'funded_accounts',
            'Funded Accounts by Quarter (2025)',
            color='#003366',
            show_markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No quarterly data available")

with col2:
    st.markdown("### 🎯 Account Activity Distribution")
    
    activity_data = pd.DataFrame({
        'Status': ['Active', 'Inactive'],
        'Count': [len(active_accounts), len(inactive_accounts)]
    })
    
    fig = vh.create_pie_chart(
        activity_data,
        'Status',
        'Count',
        'Active vs Inactive Accounts (90-day threshold)'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Product penetration analysis
st.markdown("### 📊 Product Penetration Analysis")

product_penetration = calculator.calculate_product_penetration()

if len(product_penetration) > 0:
    # Show top 10 products
    top_products = product_penetration.head(10)
    
    fig = vh.create_bar_chart(
        top_products,
        'Product Name' if 'Product Name' in top_products.columns else 'product_code',
        'penetration_rate',
        'Top 10 Products by Customer Penetration Rate',
        orientation='h',
        color='#FFD700'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    with st.expander("📋 View Detailed Product Penetration Data"):
        st.dataframe(
            product_penetration[[
                'Product Name' if 'Product Name' in product_penetration.columns else 'product_code',
                'unique_customers',
                'total_accounts',
                'penetration_rate'
            ]].rename(columns={
                'unique_customers': 'Unique Customers',
                'total_accounts': 'Total Accounts',
                'penetration_rate': 'Penetration Rate (%)'
            }),
            use_container_width=True
        )
else:
    st.info("No product penetration data available")

st.markdown("---")

# Channel adoption metrics
st.markdown("### 📱 Digital Channel Adoption")

channel_data = calculator.calculate_channel_adoption()

if len(channel_data) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        fig = vh.create_bar_chart(
            channel_data,
            'channel',
            'adoption_rate',
            'Channel Adoption Rates (%)',
            orientation='h',
            color='#003366'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Show top 3 channels as gauges
        for i, row in channel_data.head(3).iterrows():
            fig = vh.create_gauge_chart(
                row['adoption_rate'],
                row['channel'],
                max_value=100,
                thresholds=[40, 70]
            )
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No channel adoption data available")

st.markdown("---")

# Account concentration
st.markdown("### 🎯 Customer Concentration Analysis")

concentration = calculator.calculate_account_concentration()

if concentration:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Customers",
            value=f"{concentration['total_customers']:,}"
        )
        st.metric(
            label="Total Accounts",
            value=f"{concentration['total_accounts']:,}"
        )
    
    with col2:
        st.metric(
            label="Top 10% Customers",
            value=f"{concentration['top_10_pct_customers']:,}"
        )
        st.metric(
            label="Their Account Share",
            value=f"{concentration['top_10_pct_share']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="Top 20% Customers",
            value=f"{concentration['top_20_pct_customers']:,}"
        )
        st.metric(
            label="Their Account Share",
            value=f"{concentration['top_20_pct_share']:.1f}%"
        )
    
    # Visualization
    conc_df = pd.DataFrame({
        'Segment': ['Top 10%', 'Top 20%', 'Others'],
        'Share': [
            concentration['top_10_pct_share'],
            concentration['top_20_pct_share'] - concentration['top_10_pct_share'],
            100 - concentration['top_20_pct_share']
        ]
    })
    
    fig = vh.create_pie_chart(conc_df, 'Segment', 'Share', 'Account Concentration by Customer Segment')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Export functionality
st.markdown("### 📥 Export Executive Summary")

col1, col2 = st.columns([3, 1])

with col2:
    if st.button("📊 Generate Excel Report", use_container_width=True):
        st.info("Excel export functionality would be implemented here using openpyxl")
        # In production, this would generate an Excel file with all metrics

# Footer
show_nmb_footer()
