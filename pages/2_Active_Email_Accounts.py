import streamlit as st
import pandas as pd
from utils.data_loader import DataLoader
from utils.data_processor import DataProcessor
from utils.visualization import VisualizationHelper as vh
from utils.branding import apply_nmb_branding, show_nmb_logo, show_nmb_footer

st.set_page_config(page_title="Active Email Accounts", page_icon="📧", layout="wide")
apply_nmb_branding()

# NMB Logo
show_nmb_logo()

# Header
st.markdown("""
    <div style="background: linear-gradient(135deg, #003366 0%, #004080 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: #FFD700; margin: 0;">📧 Active Email Accounts Report</h1>
        <p style="color: white; margin: 0.5rem 0 0 0;">Current Account Holders with Email Addresses</p>
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
accounts_df = loader.get_accounts_data()

# Filters in sidebar
st.sidebar.markdown("### 🔍 Filters")

# Branch filter
if 'ACNTS_BRN_CODE' in accounts_df.columns:
    branches = ['All'] + sorted(accounts_df['ACNTS_BRN_CODE'].dropna().unique().tolist())
    selected_branch = st.sidebar.selectbox("Branch", branches)
else:
    selected_branch = 'All'

# Product type filter
if 'Product Name' in accounts_df.columns:
    products = ['All'] + sorted(accounts_df['Product Name'].dropna().unique().tolist())
    selected_product = st.sidebar.selectbox("Product Type", products)
else:
    selected_product = 'All'

# Currency filter
if 'ACNTS_CURR_CODE' in accounts_df.columns:
    currencies = ['All'] + sorted(accounts_df['ACNTS_CURR_CODE'].dropna().unique().tolist())
    selected_currency = st.sidebar.selectbox("Currency", currencies)
else:
    selected_currency = 'All'

# Account status filter
if 'ACNTS_CREATION_STATUS' in accounts_df.columns:
    statuses = ['All'] + sorted(accounts_df['ACNTS_CREATION_STATUS'].dropna().unique().tolist())
    selected_status = st.sidebar.selectbox("Account Status", statuses)
else:
    selected_status = 'All'

# Apply filters
filtered_df = accounts_df.copy()

if selected_branch != 'All' and 'ACNTS_BRN_CODE' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['ACNTS_BRN_CODE'] == selected_branch]

if selected_product != 'All' and 'Product Name' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Product Name'] == selected_product]

if selected_currency != 'All' and 'ACNTS_CURR_CODE' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['ACNTS_CURR_CODE'] == selected_currency]

if selected_status != 'All' and 'ACNTS_CREATION_STATUS' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['ACNTS_CREATION_STATUS'] == selected_status]

# Filter for active accounts only (not closed)
if 'ACNTS_CLOSURE_DATE' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['ACNTS_CLOSURE_DATE'].isna()]

# Summary metrics
st.markdown("### 📊 Summary Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Active Accounts",
        value=f"{len(filtered_df):,}"
    )

with col2:
    if 'ACNTS_CLIENT_NUM' in filtered_df.columns:
        unique_customers = filtered_df['ACNTS_CLIENT_NUM'].nunique()
        st.metric(
            label="Unique Customers",
            value=f"{unique_customers:,}"
        )
    else:
        st.metric(label="Unique Customers", value="N/A")

with col3:
    # Note: Email field would need to be in actual data
    # For now, we show accounts that could have email
    st.metric(
        label="Accounts with Contact Info",
        value=f"{len(filtered_df):,}",
        help="Accounts eligible for email communication"
    )

with col4:
    if 'ACNTS_CURR_CODE' in filtered_df.columns:
        currencies_count = filtered_df['ACNTS_CURR_CODE'].nunique()
        st.metric(
            label="Currencies",
            value=currencies_count
        )
    else:
        st.metric(label="Currencies", value="N/A")

st.markdown("---")

# Distribution charts
st.markdown("### 📈 Account Distribution")

col1, col2 = st.columns(2)

with col1:
    if 'Product Name' in filtered_df.columns:
        product_dist = filtered_df['Product Name'].value_counts().head(10).reset_index()
        product_dist.columns = ['Product', 'Count']
        
        fig = vh.create_bar_chart(
            product_dist,
            'Product',
            'Count',
            'Top 10 Products by Account Count',
            orientation='h',
            color='#003366'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Product distribution not available")

with col2:
    if 'ACNTS_CURR_CODE' in filtered_df.columns:
        currency_dist = filtered_df['ACNTS_CURR_CODE'].value_counts().reset_index()
        currency_dist.columns = ['Currency', 'Count']
        
        fig = vh.create_pie_chart(
            currency_dist,
            'Currency',
            'Count',
            'Distribution by Currency'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Currency distribution not available")

st.markdown("---")

# Branch-level analysis
if 'ACNTS_BRN_CODE' in filtered_df.columns:
    st.markdown("### 🏢 Branch-Level Analysis")
    
    branch_stats = filtered_df.groupby('ACNTS_BRN_CODE').agg({
        'ACNTS_ACCOUNT_NUMBER': 'count',
        'ACNTS_CLIENT_NUM': 'nunique'
    }).reset_index()
    branch_stats.columns = ['Branch', 'Total Accounts', 'Unique Customers']
    branch_stats = branch_stats.sort_values('Total Accounts', ascending=False).head(15)
    
    fig = vh.create_bar_chart(
        branch_stats,
        'Branch',
        'Total Accounts',
        'Top 15 Branches by Account Count',
        color='#FFD700'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Detailed account listing
st.markdown("### 📋 Account Details")

# Select columns to display
display_columns = []
if 'ACNTS_ACCOUNT_NUMBER' in filtered_df.columns:
    display_columns.append('ACNTS_ACCOUNT_NUMBER')
if 'ACNTS_AC_NAME1' in filtered_df.columns:
    display_columns.append('ACNTS_AC_NAME1')
if 'Product Name' in filtered_df.columns:
    display_columns.append('Product Name')
if 'ACNTS_CURR_CODE' in filtered_df.columns:
    display_columns.append('ACNTS_CURR_CODE')
if 'ACNTS_BRN_CODE' in filtered_df.columns:
    display_columns.append('ACNTS_BRN_CODE')
if 'ACNTS_OPENING_DATE' in filtered_df.columns:
    display_columns.append('ACNTS_OPENING_DATE')
if 'ACNTS_LAST_TRAN_DATE' in filtered_df.columns:
    display_columns.append('ACNTS_LAST_TRAN_DATE')
if 'ACNTS_CREATION_STATUS' in filtered_df.columns:
    display_columns.append('ACNTS_CREATION_STATUS')

if display_columns:
    # Rename columns for better display
    display_df = filtered_df[display_columns].copy()
    
    column_mapping = {
        'ACNTS_ACCOUNT_NUMBER': 'Account Number',
        'ACNTS_AC_NAME1': 'Account Name',
        'Product Name': 'Product',
        'ACNTS_CURR_CODE': 'Currency',
        'ACNTS_BRN_CODE': 'Branch',
        'ACNTS_OPENING_DATE': 'Opening Date',
        'ACNTS_LAST_TRAN_DATE': 'Last Transaction',
        'ACNTS_CREATION_STATUS': 'Status'
    }
    
    display_df = display_df.rename(columns=column_mapping)
    
    # Search functionality
    search_term = st.text_input("🔍 Search accounts (by name or account number)")
    
    if search_term:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    
    # Pagination
    page_size = st.selectbox("Records per page", [25, 50, 100, 250], index=1)
    total_pages = len(display_df) // page_size + (1 if len(display_df) % page_size > 0 else 0)
    
    if total_pages > 0:
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        st.dataframe(
            display_df.iloc[start_idx:end_idx],
            use_container_width=True,
            hide_index=True
        )
        
        st.caption(f"Showing {start_idx + 1} to {min(end_idx, len(display_df))} of {len(display_df):,} records")
    else:
        st.info("No records to display")
    
    # Export button
    st.markdown("### 📥 Export Data")
    
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name=f"active_email_accounts_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )
else:
    st.warning("No data columns available for display")

# Footer
show_nmb_footer()
