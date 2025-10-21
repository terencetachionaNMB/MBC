import streamlit as st
import pandas as pd
from utils.data_loader import DataLoader
from utils.data_processor import DataProcessor
from utils.visualization import VisualizationHelper as vh
from utils.branding import apply_nmb_branding, show_nmb_logo, show_nmb_footer
from datetime import datetime, timedelta

st.set_page_config(page_title="Account Activity", page_icon="⚡", layout="wide")
apply_nmb_branding()

# NMB Logo
show_nmb_logo()

# Header
st.markdown("""
    <div style="background: linear-gradient(135deg, #003366 0%, #004080 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: #FFD700; margin: 0;">⚡ Account Activity Analysis</h1>
        <p style="color: white; margin: 0.5rem 0 0 0;">90-Day Activity Segmentation and Drill-Down Analysis</p>
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

# Activity threshold control
st.sidebar.markdown("### ⚙️ Activity Settings")
activity_threshold = st.sidebar.slider(
    "Activity Threshold (days)",
    min_value=30,
    max_value=180,
    value=90,
    step=30,
    help="Number of days since last transaction to consider account inactive"
)

# Get activity segments
active_accounts, inactive_accounts = processor.get_account_activity_segments(activity_threshold)

# Filters
st.sidebar.markdown("### 🔍 Filters")

# Branch filter
if 'ACNTS_BRN_CODE' in accounts_df.columns:
    branches = ['All'] + sorted(accounts_df['ACNTS_BRN_CODE'].dropna().unique().tolist())
    selected_branch = st.sidebar.selectbox("Branch", branches)
else:
    selected_branch = 'All'

# Product filter
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

# Apply filters to both active and inactive dataframes
def apply_filters(df):
    filtered = df.copy()
    
    if selected_branch != 'All' and 'ACNTS_BRN_CODE' in filtered.columns:
        filtered = filtered[filtered['ACNTS_BRN_CODE'] == selected_branch]
    
    if selected_product != 'All' and 'Product Name' in filtered.columns:
        filtered = filtered[filtered['Product Name'] == selected_product]
    
    if selected_currency != 'All' and 'ACNTS_CURR_CODE' in filtered.columns:
        filtered = filtered[filtered['ACNTS_CURR_CODE'] == selected_currency]
    
    return filtered

active_filtered = apply_filters(active_accounts)
inactive_filtered = apply_filters(inactive_accounts)

# Summary metrics
st.markdown("### 📊 Activity Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_accounts = len(active_filtered) + len(inactive_filtered)
    st.metric(
        label="Total Accounts",
        value=f"{total_accounts:,}"
    )

with col2:
    st.metric(
        label="Active Accounts",
        value=f"{len(active_filtered):,}",
        delta=f"{(len(active_filtered)/total_accounts*100):.1f}%" if total_accounts > 0 else "0%",
        help=f"Accounts with transactions in last {activity_threshold} days"
    )

with col3:
    st.metric(
        label="Inactive Accounts",
        value=f"{len(inactive_filtered):,}",
        delta=f"-{(len(inactive_filtered)/total_accounts*100):.1f}%" if total_accounts > 0 else "0%",
        delta_color="inverse",
        help=f"Accounts with no transactions in last {activity_threshold} days"
    )

with col4:
    if 'ACNTS_CLIENT_NUM' in accounts_df.columns:
        all_filtered = pd.concat([active_filtered, inactive_filtered])
        unique_customers = all_filtered['ACNTS_CLIENT_NUM'].nunique() if len(all_filtered) > 0 else 0
        st.metric(
            label="Unique Customers",
            value=f"{unique_customers:,}"
        )
    else:
        st.metric(label="Unique Customers", value="N/A")

st.markdown("---")

# Activity trend visualization
st.markdown("### 📈 Activity Distribution")

col1, col2 = st.columns(2)

with col1:
    # Pie chart of active vs inactive
    activity_data = pd.DataFrame({
        'Status': ['Active', 'Inactive'],
        'Count': [len(active_filtered), len(inactive_filtered)]
    })
    
    fig = vh.create_pie_chart(
        activity_data,
        'Status',
        'Count',
        f'Account Activity Status ({activity_threshold}-day threshold)'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Days since last transaction histogram
    if 'days_since_last_txn' in active_filtered.columns or 'days_since_last_txn' in inactive_filtered.columns:
        all_data = pd.concat([active_filtered, inactive_filtered])
        
        if 'days_since_last_txn' in all_data.columns:
            # Create bins
            bins = [0, 30, 60, 90, 120, 150, 180, 365, float('inf')]
            labels = ['0-30', '31-60', '61-90', '91-120', '121-150', '151-180', '181-365', '365+']
            
            all_data['days_bin'] = pd.cut(
                all_data['days_since_last_txn'],
                bins=bins,
                labels=labels,
                include_lowest=True
            )
            
            bin_counts = all_data['days_bin'].value_counts().sort_index().reset_index()
            bin_counts.columns = ['Days Since Last Transaction', 'Count']
            
            fig = vh.create_bar_chart(
                bin_counts,
                'Days Since Last Transaction',
                'Count',
                'Distribution by Days Since Last Transaction',
                color='#FFD700'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Transaction date data not available for histogram")

st.markdown("---")

# Product-wise activity analysis
st.markdown("### 📊 Activity by Product Type")

if 'Product Name' in active_filtered.columns and 'Product Name' in inactive_filtered.columns:
    all_data = pd.concat([active_filtered, inactive_filtered])
    
    product_activity = all_data.groupby(['Product Name', 'activity_status']).size().unstack(fill_value=0).reset_index()
    
    # Calculate activity rate
    product_activity['Total'] = product_activity.get('Active', 0) + product_activity.get('Inactive', 0)
    product_activity['Activity Rate'] = (product_activity.get('Active', 0) / product_activity['Total'] * 100).round(1)
    
    # Sort by total accounts
    product_activity = product_activity.sort_values('Total', ascending=False).head(15)
    
    fig = vh.create_stacked_bar_chart(
        product_activity,
        'Product Name',
        ['Active', 'Inactive'] if 'Active' in product_activity.columns and 'Inactive' in product_activity.columns else [],
        'Top 15 Products: Active vs Inactive Accounts'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Show detailed table
    with st.expander("📋 View Detailed Product Activity Data"):
        display_cols = ['Product Name', 'Active', 'Inactive', 'Total', 'Activity Rate']
        available_cols = [col for col in display_cols if col in product_activity.columns]
        st.dataframe(
            product_activity[available_cols].rename(columns={'Activity Rate': 'Activity Rate (%)'}),
            use_container_width=True,
            hide_index=True
        )
else:
    st.info("Product activity analysis not available")

st.markdown("---")

# Branch-wise activity analysis
if 'ACNTS_BRN_CODE' in active_filtered.columns and 'ACNTS_BRN_CODE' in inactive_filtered.columns:
    st.markdown("### 🏢 Activity by Branch")
    
    all_data = pd.concat([active_filtered, inactive_filtered])
    
    branch_activity = all_data.groupby(['ACNTS_BRN_CODE', 'activity_status']).size().unstack(fill_value=0).reset_index()
    branch_activity['Total'] = branch_activity.get('Active', 0) + branch_activity.get('Inactive', 0)
    branch_activity['Activity Rate'] = (branch_activity.get('Active', 0) / branch_activity['Total'] * 100).round(1)
    branch_activity = branch_activity.sort_values('Total', ascending=False).head(15)
    
    fig = vh.create_bar_chart(
        branch_activity,
        'ACNTS_BRN_CODE',
        'Activity Rate',
        'Top 15 Branches by Activity Rate (%)',
        color='#003366'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Detailed listings with tabs
st.markdown("### 📋 Account Details")

tab1, tab2 = st.tabs(["✅ Active Accounts", "⏸️ Inactive Accounts"])

def show_account_list(df, title):
    if len(df) == 0:
        st.info(f"No {title.lower()} found with current filters")
        return
    
    # Select columns
    display_columns = []
    if 'ACNTS_ACCOUNT_NUMBER' in df.columns:
        display_columns.append('ACNTS_ACCOUNT_NUMBER')
    if 'ACNTS_AC_NAME1' in df.columns:
        display_columns.append('ACNTS_AC_NAME1')
    if 'Product Name' in df.columns:
        display_columns.append('Product Name')
    if 'ACNTS_BRN_CODE' in df.columns:
        display_columns.append('ACNTS_BRN_CODE')
    if 'ACNTS_LAST_TRAN_DATE' in df.columns:
        display_columns.append('ACNTS_LAST_TRAN_DATE')
    if 'days_since_last_txn' in df.columns:
        display_columns.append('days_since_last_txn')
    if 'ACNTS_CURR_CODE' in df.columns:
        display_columns.append('ACNTS_CURR_CODE')
    
    if display_columns:
        display_df = df[display_columns].copy()
        
        column_mapping = {
            'ACNTS_ACCOUNT_NUMBER': 'Account Number',
            'ACNTS_AC_NAME1': 'Account Name',
            'Product Name': 'Product',
            'ACNTS_BRN_CODE': 'Branch',
            'ACNTS_LAST_TRAN_DATE': 'Last Transaction',
            'days_since_last_txn': 'Days Since Last Txn',
            'ACNTS_CURR_CODE': 'Currency'
        }
        
        display_df = display_df.rename(columns=column_mapping)
        
        # Search
        search = st.text_input(f"🔍 Search {title.lower()}", key=f"search_{title}")
        if search:
            mask = display_df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
            display_df = display_df[mask]
        
        # Pagination
        page_size = 50
        total_pages = len(display_df) // page_size + (1 if len(display_df) % page_size > 0 else 0)
        
        if total_pages > 0:
            page = st.number_input(f"Page ({title})", min_value=1, max_value=total_pages, value=1, key=f"page_{title}")
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            
            st.dataframe(
                display_df.iloc[start_idx:end_idx],
                use_container_width=True,
                hide_index=True
            )
            
            st.caption(f"Showing {start_idx + 1} to {min(end_idx, len(display_df))} of {len(display_df):,} records")
        
        # Export
        csv = display_df.to_csv(index=False)
        st.download_button(
            label=f"📄 Download {title} CSV",
            data=csv,
            file_name=f"{title.lower().replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key=f"download_{title}"
        )

with tab1:
    show_account_list(active_filtered, "Active Accounts")

with tab2:
    show_account_list(inactive_filtered, "Inactive Accounts")

# Footer
show_nmb_footer()
