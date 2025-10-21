import streamlit as st
import pandas as pd
from utils.data_loader import DataLoader
from utils.data_processor import DataProcessor
from utils.metrics_calculator import MetricsCalculator
from utils.visualization import VisualizationHelper as vh

st.set_page_config(page_title="Quarterly Performance", page_icon="📅", layout="wide")

# Header
st.markdown("""
    <div style="background: linear-gradient(135deg, #003366 0%, #004080 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: #FFD700; margin: 0;">📅 Quarterly Performance Tracker</h1>
        <p style="color: white; margin: 0.5rem 0 0 0;">Funded Accounts Q1-Q3 2025 Analysis</p>
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

# Year selection
st.sidebar.markdown("### ⚙️ Settings")
selected_year = st.sidebar.selectbox("Year", [2024, 2025, 2026], index=1)

# Get quarterly data
quarterly_data = processor.get_quarterly_funded_accounts(selected_year)

# Summary metrics
st.markdown(f"### 📊 {selected_year} Quarterly Summary")

if len(quarterly_data) > 0:
    col1, col2, col3, col4 = st.columns(4)
    
    # Q1
    with col1:
        q1_data = quarterly_data[quarterly_data['quarter'] == f'Q1 {selected_year}']
        if len(q1_data) > 0:
            q1_value = q1_data.iloc[0]['funded_accounts']
            st.metric(
                label=f"Q1 {selected_year}",
                value=f"{q1_value:,}",
                help="Funded accounts in Q1"
            )
        else:
            st.metric(label=f"Q1 {selected_year}", value="N/A")
    
    # Q2
    with col2:
        q2_data = quarterly_data[quarterly_data['quarter'] == f'Q2 {selected_year}']
        if len(q2_data) > 0:
            q2_value = q2_data.iloc[0]['funded_accounts']
            # Calculate growth from Q1
            if len(q1_data) > 0 and q1_data.iloc[0]['funded_accounts'] > 0:
                growth = ((q2_value - q1_data.iloc[0]['funded_accounts']) / q1_data.iloc[0]['funded_accounts']) * 100
                st.metric(
                    label=f"Q2 {selected_year}",
                    value=f"{q2_value:,}",
                    delta=f"{growth:+.1f}%",
                    help="Funded accounts in Q2"
                )
            else:
                st.metric(label=f"Q2 {selected_year}", value=f"{q2_value:,}")
        else:
            st.metric(label=f"Q2 {selected_year}", value="N/A")
    
    # Q3
    with col3:
        q3_data = quarterly_data[quarterly_data['quarter'] == f'Q3 {selected_year}']
        if len(q3_data) > 0:
            q3_value = q3_data.iloc[0]['funded_accounts']
            # Calculate growth from Q2
            if len(q2_data) > 0 and q2_data.iloc[0]['funded_accounts'] > 0:
                growth = ((q3_value - q2_data.iloc[0]['funded_accounts']) / q2_data.iloc[0]['funded_accounts']) * 100
                st.metric(
                    label=f"Q3 {selected_year}",
                    value=f"{q3_value:,}",
                    delta=f"{growth:+.1f}%",
                    help="Funded accounts in Q3"
                )
            else:
                st.metric(label=f"Q3 {selected_year}", value=f"{q3_value:,}")
        else:
            st.metric(label=f"Q3 {selected_year}", value="N/A")
    
    # Total growth
    with col4:
        if len(q1_data) > 0 and len(q3_data) > 0:
            total_growth = ((q3_data.iloc[0]['funded_accounts'] - q1_data.iloc[0]['funded_accounts']) / q1_data.iloc[0]['funded_accounts']) * 100
            st.metric(
                label="Q1-Q3 Growth",
                value=f"{total_growth:+.1f}%",
                help="Total growth from Q1 to Q3"
            )
        else:
            st.metric(label="Q1-Q3 Growth", value="N/A")
    
    st.markdown("---")
    
    # Trend visualization
    st.markdown("### 📈 Quarterly Trend Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = vh.create_line_chart(
            quarterly_data,
            'quarter',
            'funded_accounts',
            f'Funded Accounts Trend ({selected_year})',
            color='#003366',
            show_markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Growth Rates")
        
        if len(quarterly_data) >= 2:
            growth_data = []
            for i in range(1, len(quarterly_data)):
                prev_q = quarterly_data.iloc[i-1]
                curr_q = quarterly_data.iloc[i]
                
                if prev_q['funded_accounts'] > 0:
                    growth = ((curr_q['funded_accounts'] - prev_q['funded_accounts']) / prev_q['funded_accounts']) * 100
                    growth_data.append({
                        'Period': f"{prev_q['quarter']} → {curr_q['quarter']}",
                        'Growth (%)': f"{growth:+.2f}%"
                    })
            
            if growth_data:
                growth_df = pd.DataFrame(growth_data)
                st.dataframe(growth_df, use_container_width=True, hide_index=True)
        else:
            st.info("Insufficient data for growth calculation")
    
    st.markdown("---")
    
    # Detailed breakdown
    st.markdown("### 📊 Detailed Quarterly Breakdown")
    
    # Format the quarterly data for display
    display_df = quarterly_data.copy()
    display_df['period_start'] = pd.to_datetime(display_df['period_start']).dt.strftime('%Y-%m-%d')
    display_df['period_end'] = pd.to_datetime(display_df['period_end']).dt.strftime('%Y-%m-%d')
    
    # Calculate quarter-on-quarter change
    display_df['qoq_change'] = display_df['funded_accounts'].diff()
    display_df['qoq_change_pct'] = display_df['funded_accounts'].pct_change() * 100
    
    # Rename columns
    display_df = display_df.rename(columns={
        'quarter': 'Quarter',
        'funded_accounts': 'Funded Accounts',
        'period_start': 'Period Start',
        'period_end': 'Period End',
        'qoq_change': 'QoQ Change',
        'qoq_change_pct': 'QoQ Change (%)'
    })
    
    st.dataframe(
        display_df[['Quarter', 'Funded Accounts', 'Period Start', 'Period End', 'QoQ Change', 'QoQ Change (%)']],
        use_container_width=True,
        hide_index=True
    )
    
else:
    st.warning(f"No quarterly data available for {selected_year}")

st.markdown("---")

# Product-wise quarterly analysis
st.markdown("### 📊 Quarterly Performance by Product Type")

accounts_df = loader.get_accounts_data()

if 'Product Name' in accounts_df.columns and 'ACNTS_OPENING_DATE' in accounts_df.columns:
    # Filter accounts for the selected year
    accounts_df['opening_year'] = pd.to_datetime(accounts_df['ACNTS_OPENING_DATE']).dt.year
    year_accounts = accounts_df[accounts_df['opening_year'] <= selected_year].copy()
    
    # Filter out closed accounts
    if 'ACNTS_CLOSURE_DATE' in year_accounts.columns:
        year_accounts = year_accounts[year_accounts['ACNTS_CLOSURE_DATE'].isna()]
    
    # Create quarter column
    year_accounts['last_txn_date'] = pd.to_datetime(year_accounts.get('ACNTS_LAST_TRAN_DATE'))
    
    # Group by product and count for each quarter
    product_quarterly = []
    for q in range(1, 4):
        q_start = pd.Timestamp(f'{selected_year}-{(q-1)*3+1:02d}-01')
        q_end = pd.Timestamp(f'{selected_year}-{q*3:02d}-01') + pd.offsets.MonthEnd(0)
        
        active_in_q = year_accounts[
            (year_accounts['ACNTS_OPENING_DATE'] <= q_end) &
            ((year_accounts['last_txn_date'].isna()) | (year_accounts['last_txn_date'] >= q_start))
        ]
        
        product_counts = active_in_q['Product Name'].value_counts().head(10)
        
        for product, count in product_counts.items():
            product_quarterly.append({
                'Quarter': f'Q{q}',
                'Product': product,
                'Accounts': count
            })
    
    if product_quarterly:
        product_df = pd.DataFrame(product_quarterly)
        
        # Get top 10 products overall
        top_products = product_df.groupby('Product')['Accounts'].sum().nlargest(10).index
        product_df_filtered = product_df[product_df['Product'].isin(top_products)]
        
        # Create pivot for stacked bar
        product_pivot = product_df_filtered.pivot(index='Product', columns='Quarter', values='Accounts').fillna(0)
        product_pivot = product_pivot.reset_index()
        
        if len(product_pivot) > 0:
            quarters = [col for col in product_pivot.columns if col.startswith('Q')]
            
            fig = vh.create_stacked_bar_chart(
                product_pivot,
                'Product',
                quarters,
                f'Top 10 Products: Quarterly Funded Accounts ({selected_year})'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No product-wise quarterly data available")
else:
    st.info("Product-wise analysis not available")

st.markdown("---")

# Branch-wise quarterly performance
if 'ACNTS_BRN_CODE' in accounts_df.columns and 'ACNTS_LAST_TRAN_DATE' in accounts_df.columns:
    st.markdown("### 🏢 Quarterly Performance by Branch")
    
    # Filter for funded accounts (those with transactions)
    funded_accounts = accounts_df[accounts_df['ACNTS_LAST_TRAN_DATE'].notna()].copy()
    
    branch_quarterly = []
    for q in range(1, 4):
        q_start = pd.Timestamp(f'{selected_year}-{(q-1)*3+1:02d}-01')
        q_end = pd.Timestamp(f'{selected_year}-{q*3:02d}-01') + pd.offsets.MonthEnd(0)
        
        # Count accounts with transactions in this quarter
        active_in_q = funded_accounts[
            (funded_accounts['ACNTS_LAST_TRAN_DATE'] >= q_start) &
            (funded_accounts['ACNTS_LAST_TRAN_DATE'] <= q_end)
        ]
        
        branch_counts = active_in_q['ACNTS_BRN_CODE'].value_counts().head(10)
        
        for branch, count in branch_counts.items():
            branch_quarterly.append({
                'Quarter': f'Q{q}',
                'Branch': str(branch),
                'Accounts': count
            })
    
    if branch_quarterly:
        branch_df = pd.DataFrame(branch_quarterly)
        
        # Get top 10 branches
        top_branches = branch_df.groupby('Branch')['Accounts'].sum().nlargest(10).index
        branch_df_filtered = branch_df[branch_df['Branch'].isin(top_branches)]
        
        # Pivot
        branch_pivot = branch_df_filtered.pivot(index='Branch', columns='Quarter', values='Accounts').fillna(0)
        branch_pivot = branch_pivot.reset_index()
        
        if len(branch_pivot) > 0:
            quarters = [col for col in branch_pivot.columns if col.startswith('Q')]
            
            fig = vh.create_stacked_bar_chart(
                branch_pivot,
                'Branch',
                quarters,
                f'Top 10 Branches: Quarterly Funded Accounts ({selected_year})'
            )
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Export functionality
st.markdown("### 📥 Export Quarterly Data")

if len(quarterly_data) > 0:
    csv = quarterly_data.to_csv(index=False)
    st.download_button(
        label="📄 Download Quarterly Performance CSV",
        data=csv,
        file_name=f"quarterly_performance_{selected_year}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem; border-top: 1px solid #eee; margin-top: 2rem;">
        <p>Quarterly Performance Tracker | Updated: October 21, 2025</p>
    </div>
""", unsafe_allow_html=True)
