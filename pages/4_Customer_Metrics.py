import streamlit as st
import pandas as pd
from utils.data_loader import DataLoader
from utils.data_processor import DataProcessor
from utils.metrics_calculator import MetricsCalculator
from utils.visualization import VisualizationHelper as vh
from datetime import datetime, timedelta

st.set_page_config(page_title="Customer Metrics", page_icon="👥", layout="wide")

# Header
st.markdown("""
    <div style="background: linear-gradient(135deg, #003366 0%, #004080 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: #FFD700; margin: 0;">👥 Customer Metrics Dashboard</h1>
        <p style="color: white; margin: 0.5rem 0 0 0;">Churn Analysis, Product Holdings, and Customer Insights</p>
    </div>
""", unsafe_allow_html=True)

# Load data
@st.cache_resource
def load_data():
    return DataLoader()

loader = load_data()

if loader.get_accounts_data() is None:
    st.error("⚠️ No account data available.")
    st.stop()

processor = DataProcessor(loader)
calculator = MetricsCalculator(processor)

# Calculate key metrics
total_customers = processor.get_unique_customer_count()
avg_products = processor.get_avg_products_per_customer()
churn_data = processor.calculate_monthly_churn_rate()

# Summary metrics
st.markdown("### 📊 Key Customer Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Customers",
        value=f"{total_customers:,}",
        help="Total unique customers in the system"
    )

with col2:
    st.metric(
        label="Avg Products/Customer",
        value=f"{avg_products:.2f}",
        help="Average number of products per customer (excl. Account/Card types)"
    )

with col3:
    if len(churn_data) > 0:
        latest_churn = churn_data.iloc[-1]['churn_rate']
        st.metric(
            label="Latest Monthly Churn Rate",
            value=f"{latest_churn:.2f}%",
            help="Most recent month's churn rate"
        )
    else:
        st.metric(
            label="Latest Monthly Churn Rate",
            value="N/A"
        )

with col4:
    # Customer lifetime value (in years)
    clv = calculator.calculate_customer_lifetime_value()
    st.metric(
        label="Avg Customer Tenure",
        value=f"{clv:.1f} years",
        help="Average customer relationship duration"
    )

st.markdown("---")

# Churn analysis
st.markdown("### 📉 Monthly Churn Rate Analysis")

if len(churn_data) > 0:
    # Convert period to string for display
    churn_data_display = churn_data.copy()
    churn_data_display['month_str'] = churn_data_display['month'].astype(str)
    
    fig = vh.create_line_chart(
        churn_data_display,
        'month_str',
        'churn_rate',
        'Monthly Churn Rate Trend (%)',
        color='#003366',
        show_markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Show detailed churn data
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Churn Statistics")
        if len(churn_data) > 0:
            avg_churn = churn_data['churn_rate'].mean()
            max_churn = churn_data['churn_rate'].max()
            min_churn = churn_data['churn_rate'].min()
            
            metrics_df = pd.DataFrame({
                'Metric': ['Average Churn Rate', 'Maximum Churn Rate', 'Minimum Churn Rate'],
                'Value': [f"{avg_churn:.2f}%", f"{max_churn:.2f}%", f"{min_churn:.2f}%"]
            })
            
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 📋 Monthly Churn Details")
        display_churn = churn_data.copy()
        display_churn['month'] = display_churn['month'].astype(str)
        display_churn = display_churn.rename(columns={
            'month': 'Month',
            'churned_customers': 'Churned Customers',
            'churn_rate': 'Churn Rate (%)'
        })
        
        st.dataframe(
            display_churn[['Month', 'Churned Customers', 'Churn Rate (%)']].tail(12),
            use_container_width=True,
            hide_index=True
        )
else:
    st.info("No churn data available. This requires account closure date information.")

st.markdown("---")

# Product holding analysis
st.markdown("### 🎯 Product Holding Analysis")

accounts_df = loader.get_accounts_data()

if 'ACNTS_CLIENT_NUM' in accounts_df.columns and 'ACNTS_PROD_CODE' in accounts_df.columns:
    # Calculate products per customer distribution
    products_per_customer = accounts_df.groupby('ACNTS_CLIENT_NUM')['ACNTS_PROD_CODE'].nunique().reset_index()
    products_per_customer.columns = ['customer', 'product_count']
    
    # Create distribution
    distribution = products_per_customer['product_count'].value_counts().sort_index().reset_index()
    distribution.columns = ['Number of Products', 'Number of Customers']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = vh.create_bar_chart(
            distribution,
            'Number of Products',
            'Number of Customers',
            'Distribution of Products per Customer',
            color='#FFD700'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Statistics
        st.markdown("#### 📊 Product Holding Statistics")
        
        stats_df = pd.DataFrame({
            'Metric': [
                'Customers with 1 Product',
                'Customers with 2 Products',
                'Customers with 3+ Products',
                'Max Products Held'
            ],
            'Value': [
                f"{len(products_per_customer[products_per_customer['product_count'] == 1]):,}",
                f"{len(products_per_customer[products_per_customer['product_count'] == 2]):,}",
                f"{len(products_per_customer[products_per_customer['product_count'] >= 3]):,}",
                f"{products_per_customer['product_count'].max()}"
            ]
        })
        
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
else:
    st.info("Product holding analysis not available")

st.markdown("---")

# Customer segmentation
st.markdown("### 🎯 Customer Segmentation")

if 'ACNTS_CLIENT_NUM' in accounts_df.columns:
    # Segment by number of accounts
    accounts_per_customer = accounts_df.groupby('ACNTS_CLIENT_NUM').size().reset_index(name='account_count')
    
    # Create segments
    def segment_customer(count):
        if count == 1:
            return 'Single Account'
        elif count <= 3:
            return '2-3 Accounts'
        elif count <= 5:
            return '4-5 Accounts'
        else:
            return '6+ Accounts'
    
    accounts_per_customer['segment'] = accounts_per_customer['account_count'].apply(segment_customer)
    
    segment_dist = accounts_per_customer['segment'].value_counts().reset_index()
    segment_dist.columns = ['Segment', 'Customer Count']
    
    # Ensure proper order
    segment_order = ['Single Account', '2-3 Accounts', '4-5 Accounts', '6+ Accounts']
    segment_dist['Segment'] = pd.Categorical(segment_dist['Segment'], categories=segment_order, ordered=True)
    segment_dist = segment_dist.sort_values('Segment')
    
    fig = vh.create_pie_chart(
        segment_dist,
        'Segment',
        'Customer Count',
        'Customer Segmentation by Number of Accounts'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed segment analysis
    with st.expander("📋 View Detailed Segment Analysis"):
        segment_analysis = accounts_per_customer.groupby('segment').agg({
            'account_count': ['count', 'mean', 'min', 'max']
        }).reset_index()
        
        segment_analysis.columns = ['Segment', 'Number of Customers', 'Avg Accounts', 'Min Accounts', 'Max Accounts']
        segment_analysis['Segment'] = pd.Categorical(segment_analysis['Segment'], categories=segment_order, ordered=True)
        segment_analysis = segment_analysis.sort_values('Segment')
        
        st.dataframe(segment_analysis, use_container_width=True, hide_index=True)

st.markdown("---")

# Product penetration
st.markdown("### 📊 Product Penetration Rates")

product_penetration = calculator.calculate_product_penetration()

if len(product_penetration) > 0:
    # Show top 15 products
    top_products = product_penetration.head(15)
    
    fig = vh.create_bar_chart(
        top_products,
        'Product Name' if 'Product Name' in top_products.columns else 'product_code',
        'penetration_rate',
        'Top 15 Products by Penetration Rate (%)',
        orientation='h',
        color='#003366'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    with st.expander("📋 View All Product Penetration Data"):
        display_cols = ['Product Name' if 'Product Name' in product_penetration.columns else 'product_code',
                       'unique_customers', 'total_accounts', 'penetration_rate']
        available_cols = [col for col in display_cols if col in product_penetration.columns]
        
        if available_cols:
            display_df = product_penetration[available_cols].rename(columns={
                'unique_customers': 'Unique Customers',
                'total_accounts': 'Total Accounts',
                'penetration_rate': 'Penetration Rate (%)'
            })
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("Product penetration data not available")

st.markdown("---")

# Account concentration
st.markdown("### 🎯 Customer Concentration Metrics")

concentration = calculator.calculate_account_concentration()

if concentration:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top Customer Segments")
        
        conc_df = pd.DataFrame({
            'Segment': ['Top 10% Customers', 'Top 20% Customers', 'Remaining Customers'],
            'Customers': [
                concentration['top_10_pct_customers'],
                concentration['top_20_pct_customers'] - concentration['top_10_pct_customers'],
                concentration['total_customers'] - concentration['top_20_pct_customers']
            ],
            'Accounts': [
                concentration['top_10_pct_accounts'],
                concentration['top_20_pct_accounts'] - concentration['top_10_pct_accounts'],
                concentration['total_accounts'] - concentration['top_20_pct_accounts']
            ],
            'Account Share (%)': [
                concentration['top_10_pct_share'],
                concentration['top_20_pct_share'] - concentration['top_10_pct_share'],
                100 - concentration['top_20_pct_share']
            ]
        })
        
        st.dataframe(conc_df, use_container_width=True, hide_index=True)
    
    with col2:
        fig = vh.create_pie_chart(
            conc_df,
            'Segment',
            'Account Share (%)',
            'Account Concentration Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem; border-top: 1px solid #eee; margin-top: 2rem;">
        <p>Customer Metrics Dashboard | Updated: October 21, 2025</p>
    </div>
""", unsafe_allow_html=True)
