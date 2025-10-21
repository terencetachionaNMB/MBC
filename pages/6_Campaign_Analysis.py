import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import DataLoader
from utils.data_processor import DataProcessor
from utils.visualization import VisualizationHelper as vh
from datetime import datetime, timedelta

st.set_page_config(page_title="Campaign Analysis", page_icon="🎯", layout="wide")

# Header
st.markdown("""
    <div style="background: linear-gradient(135deg, #003366 0%, #004080 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: #FFD700; margin: 0;">🎯 Campaign Analysis Dashboard</h1>
        <p style="color: white; margin: 0.5rem 0 0 0;">Non-Funded Income Campaign Performance | June - September 2025</p>
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
gl_df = loader.get_gl_data()

# Campaign settings
st.sidebar.markdown("### 🎯 Campaign Settings")

campaign_start = st.sidebar.date_input(
    "Campaign Start Date",
    value=datetime(2025, 6, 1),
    min_value=datetime(2024, 1, 1),
    max_value=datetime(2026, 12, 31)
)

campaign_end = st.sidebar.date_input(
    "Campaign End Date",
    value=datetime(2025, 9, 30),
    min_value=datetime(2024, 1, 1),
    max_value=datetime(2026, 12, 31)
)

# Baseline period for comparison
baseline_start = st.sidebar.date_input(
    "Baseline Start (for comparison)",
    value=datetime(2025, 4, 1),
    min_value=datetime(2024, 1, 1),
    max_value=datetime(2026, 12, 31)
)

# Filters
st.sidebar.markdown("### 🔍 Filters")

# Product filter
if 'Product Name' in accounts_df.columns:
    products = ['All'] + sorted(accounts_df['Product Name'].dropna().unique().tolist())
    selected_product = st.sidebar.selectbox("Product Type", products)
else:
    selected_product = 'All'

# Branch filter
if 'ACNTS_BRN_CODE' in accounts_df.columns:
    branches = ['All'] + sorted(accounts_df['ACNTS_BRN_CODE'].dropna().unique().tolist())
    selected_branch = st.sidebar.selectbox("Branch", branches)
else:
    selected_branch = 'All'

# Currency filter
if 'ACNTS_CURR_CODE' in accounts_df.columns:
    currencies = ['All'] + sorted(accounts_df['ACNTS_CURR_CODE'].dropna().unique().tolist())
    selected_currency = st.sidebar.selectbox("Currency", currencies)
else:
    selected_currency = 'All'

# Check for GL transaction data
has_gl_data = gl_df is not None and len(gl_df) > 0

# Get campaign revenue data
campaign_revenue = processor.get_campaign_revenue_analysis(
    campaign_start=campaign_start.strftime('%Y-%m-%d'),
    campaign_end=campaign_end.strftime('%Y-%m-%d')
)

# Information about data availability
if not has_gl_data:
    st.warning("""
    ⚠️ **Note:** GL transaction data is not available. 
    
    This dashboard is designed to analyze non-funded income revenue from GL transactions. 
    To see actual campaign performance, please ensure GL transaction data is loaded.
    
    **Required data includes:**
    - Fee income (account maintenance, transaction fees)
    - Commission income (forex, trade finance, guarantees)
    - Service charges
    - Other non-interest income
    
    The structure below shows how the analysis will appear once data is available.
    """)

# Summary metrics
st.markdown("### 📊 Campaign Performance Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Total campaign revenue
    if len(campaign_revenue) > 0 and has_gl_data:
        total_revenue = campaign_revenue['revenue'].sum()
        st.metric(
            label="Total Campaign Revenue",
            value=f"${total_revenue:,.2f}",
            help="Total non-funded income during campaign period"
        )
    else:
        st.metric(
            label="Total Campaign Revenue",
            value="No Data",
            help="GL transaction data required"
        )

with col2:
    # Average monthly revenue
    if len(campaign_revenue) > 0 and has_gl_data:
        avg_monthly = campaign_revenue['revenue'].mean()
        st.metric(
            label="Avg Monthly Revenue",
            value=f"${avg_monthly:,.2f}",
            help="Average monthly revenue during campaign"
        )
    else:
        st.metric(
            label="Avg Monthly Revenue",
            value="No Data"
        )

with col3:
    # Month-on-month growth
    if len(campaign_revenue) > 1 and has_gl_data:
        latest_mom = campaign_revenue.iloc[-1]['mom_change']
        if pd.notna(latest_mom):
            st.metric(
                label="Latest MoM Growth",
                value=f"{latest_mom:+.1f}%",
                help="Latest month-on-month growth rate"
            )
        else:
            st.metric(label="Latest MoM Growth", value="N/A")
    else:
        st.metric(label="Latest MoM Growth", value="No Data")

with col4:
    # Best performing month
    if len(campaign_revenue) > 0 and has_gl_data:
        best_month = campaign_revenue.loc[campaign_revenue['revenue'].idxmax()]
        st.metric(
            label="Best Month",
            value=best_month['month_name'],
            help=f"Revenue: ${best_month['revenue']:,.2f}"
        )
    else:
        st.metric(label="Best Month", value="No Data")

st.markdown("---")

# Revenue trend analysis
st.markdown("### 📈 Revenue Trend Analysis")

if len(campaign_revenue) > 0:
    # Extend data to include baseline months
    baseline_months = pd.period_range(
        start=baseline_start.strftime('%Y-%m'),
        end=campaign_start.strftime('%Y-%m'),
        freq='M'
    )
    
    # Create extended dataset
    extended_revenue = campaign_revenue.copy()
    
    # Add baseline months if not already present
    for month in baseline_months:
        if month.to_timestamp() not in extended_revenue['month'].values:
            extended_revenue = pd.concat([
                pd.DataFrame({
                    'month': [month.to_timestamp()],
                    'month_name': [month.strftime('%B %Y')],
                    'revenue': [0 if not has_gl_data else np.nan],
                    'non_funded_income': [0 if not has_gl_data else np.nan],
                    'mom_change': [0],
                    'mom_change_abs': [0]
                }),
                extended_revenue
            ])
    
    extended_revenue = extended_revenue.sort_values('month').reset_index(drop=True)
    extended_revenue['month_str'] = extended_revenue['month'].dt.strftime('%b %Y')
    
    # Recalculate MoM changes
    extended_revenue['mom_change'] = extended_revenue['revenue'].pct_change() * 100
    extended_revenue['mom_change_abs'] = extended_revenue['revenue'].diff()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Revenue trend line chart
        fig = vh.create_line_chart(
            extended_revenue,
            'month_str',
            'revenue',
            'Monthly Revenue Trend (Baseline + Campaign Period)',
            color='#003366',
            show_markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Campaign Statistics")
        
        if has_gl_data and extended_revenue['revenue'].sum() > 0:
            campaign_only = extended_revenue[
                (extended_revenue['month'] >= pd.Timestamp(campaign_start)) &
                (extended_revenue['month'] <= pd.Timestamp(campaign_end))
            ]
            
            if len(campaign_only) > 0:
                stats_df = pd.DataFrame({
                    'Metric': [
                        'Total Revenue',
                        'Average Monthly',
                        'Highest Month',
                        'Lowest Month',
                        'Avg MoM Growth'
                    ],
                    'Value': [
                        f"${campaign_only['revenue'].sum():,.2f}",
                        f"${campaign_only['revenue'].mean():,.2f}",
                        f"${campaign_only['revenue'].max():,.2f}",
                        f"${campaign_only['revenue'].min():,.2f}",
                        f"{campaign_only['mom_change'].mean():.2f}%"
                    ]
                })
                
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
        else:
            st.info("Statistics will be displayed when GL transaction data is available")
    
    st.markdown("---")
    
    # Month-on-month change analysis
    st.markdown("### 📊 Month-on-Month Revenue Change")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # MoM percentage change
        fig = vh.create_bar_chart(
            extended_revenue[extended_revenue['mom_change'].notna()],
            'month_str',
            'mom_change',
            'Month-on-Month Revenue Change (%)',
            color='#FFD700'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # MoM absolute change
        fig = vh.create_bar_chart(
            extended_revenue[extended_revenue['mom_change_abs'].notna()],
            'month_str',
            'mom_change_abs',
            'Month-on-Month Revenue Change (Absolute)',
            color='#003366'
        )
        st.plotly_chart(fig, use_container_width=True)
    
else:
    st.info("""
    Revenue trend analysis requires GL transaction data. 
    
    Once available, this section will display:
    - Monthly revenue trends from baseline period through campaign
    - Month-on-month growth rates
    - Campaign performance statistics
    - Comparative analysis with pre-campaign period
    """)

st.markdown("---")

# Revenue breakdown by income type
st.markdown("### 💰 Non-Funded Income Breakdown")

if has_gl_data and gl_df is not None:
    # Filter GL data for income categories
    income_categories = gl_df[gl_df['Gl Type'].isin(['I', 'Income'])] if 'Gl Type' in gl_df.columns else pd.DataFrame()
    
    if len(income_categories) > 0:
        # Categorize income types
        income_summary = income_categories.groupby('Gl Name').size().reset_index(name='Count')
        income_summary = income_summary.nlargest(10, 'Count')
        
        fig = vh.create_pie_chart(
            income_summary,
            'Gl Name',
            'Count',
            'Top 10 Non-Funded Income Categories'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed breakdown
        with st.expander("📋 View All Income Categories"):
            full_summary = income_categories.groupby('Gl Name').size().reset_index(name='GL Accounts')
            full_summary = full_summary.sort_values('GL Accounts', ascending=False)
            st.dataframe(full_summary, use_container_width=True, hide_index=True)
    else:
        st.info("Income category data not available in GL master")
else:
    st.info("""
    This section will show breakdown of non-funded income by category:
    - Commission income (guarantees, LC, forex)
    - Service charges (account maintenance, transactions)
    - Fee income (processing, advisory)
    - Other non-interest income
    
    Requires GL transaction data with income type classification.
    """)

st.markdown("---")

# Product-wise campaign performance
st.markdown("### 📊 Campaign Performance by Product")

# Filter accounts data
filtered_accounts = accounts_df.copy()

if selected_product != 'All' and 'Product Name' in filtered_accounts.columns:
    filtered_accounts = filtered_accounts[filtered_accounts['Product Name'] == selected_product]

if selected_branch != 'All' and 'ACNTS_BRN_CODE' in filtered_accounts.columns:
    filtered_accounts = filtered_accounts[filtered_accounts['ACNTS_BRN_CODE'] == selected_branch]

if selected_currency != 'All' and 'ACNTS_CURR_CODE' in filtered_accounts.columns:
    filtered_accounts = filtered_accounts[filtered_accounts['ACNTS_CURR_CODE'] == selected_currency]

if 'Product Name' in filtered_accounts.columns:
    # Account activity during campaign period
    if 'ACNTS_LAST_TRAN_DATE' in filtered_accounts.columns:
        filtered_accounts['last_txn'] = pd.to_datetime(filtered_accounts['ACNTS_LAST_TRAN_DATE'])
        
        campaign_accounts = filtered_accounts[
            (filtered_accounts['last_txn'] >= pd.Timestamp(campaign_start)) &
            (filtered_accounts['last_txn'] <= pd.Timestamp(campaign_end))
        ]
        
        if len(campaign_accounts) > 0:
            product_activity = campaign_accounts['Product Name'].value_counts().head(15).reset_index()
            product_activity.columns = ['Product', 'Active Accounts']
            
            fig = vh.create_bar_chart(
                product_activity,
                'Product',
                'Active Accounts',
                'Top 15 Products by Active Accounts (Campaign Period)',
                orientation='h',
                color='#003366'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Active Products",
                    value=campaign_accounts['Product Name'].nunique()
                )
            
            with col2:
                st.metric(
                    label="Active Accounts",
                    value=f"{len(campaign_accounts):,}"
                )
            
            with col3:
                if 'ACNTS_CLIENT_NUM' in campaign_accounts.columns:
                    st.metric(
                        label="Active Customers",
                        value=f"{campaign_accounts['ACNTS_CLIENT_NUM'].nunique():,}"
                    )
        else:
            st.info("No account activity found during campaign period with current filters")
    else:
        st.info("Transaction date data not available for product analysis")
else:
    st.info("Product information not available")

st.markdown("---")

# Branch performance during campaign
if 'ACNTS_BRN_CODE' in filtered_accounts.columns:
    st.markdown("### 🏢 Branch Performance During Campaign")
    
    if 'ACNTS_LAST_TRAN_DATE' in filtered_accounts.columns:
        campaign_branches = campaign_accounts.groupby('ACNTS_BRN_CODE').agg({
            'ACNTS_ACCOUNT_NUMBER': 'count',
            'ACNTS_CLIENT_NUM': 'nunique'
        }).reset_index()
        
        campaign_branches.columns = ['Branch', 'Active Accounts', 'Active Customers']
        campaign_branches = campaign_branches.sort_values('Active Accounts', ascending=False).head(15)
        
        if len(campaign_branches) > 0:
            fig = vh.create_bar_chart(
                campaign_branches,
                'Branch',
                'Active Accounts',
                'Top 15 Branches by Activity (Campaign Period)',
                color='#FFD700'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            with st.expander("📋 View All Branch Performance Data"):
                all_branches = campaign_accounts.groupby('ACNTS_BRN_CODE').agg({
                    'ACNTS_ACCOUNT_NUMBER': 'count',
                    'ACNTS_CLIENT_NUM': 'nunique'
                }).reset_index()
                all_branches.columns = ['Branch', 'Active Accounts', 'Active Customers']
                all_branches = all_branches.sort_values('Active Accounts', ascending=False)
                
                st.dataframe(all_branches, use_container_width=True, hide_index=True)

st.markdown("---")

# Campaign effectiveness metrics
st.markdown("### 🎯 Campaign Effectiveness Metrics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📊 Key Performance Indicators")
    
    if has_gl_data and len(campaign_revenue) > 0:
        # Calculate campaign KPIs
        campaign_period = campaign_revenue[
            (campaign_revenue['month'] >= pd.Timestamp(campaign_start)) &
            (campaign_revenue['month'] <= pd.Timestamp(campaign_end))
        ]
        
        baseline_period = extended_revenue[
            (extended_revenue['month'] >= pd.Timestamp(baseline_start)) &
            (extended_revenue['month'] < pd.Timestamp(campaign_start))
        ]
        
        if len(campaign_period) > 0 and len(baseline_period) > 0:
            baseline_avg = baseline_period['revenue'].mean()
            campaign_avg = campaign_period['revenue'].mean()
            
            if baseline_avg > 0:
                improvement = ((campaign_avg - baseline_avg) / baseline_avg) * 100
                
                kpi_df = pd.DataFrame({
                    'KPI': [
                        'Baseline Avg Revenue',
                        'Campaign Avg Revenue',
                        'Revenue Improvement',
                        'Best Campaign Month',
                        'Campaign Consistency'
                    ],
                    'Value': [
                        f"${baseline_avg:,.2f}",
                        f"${campaign_avg:,.2f}",
                        f"{improvement:+.1f}%",
                        campaign_period.loc[campaign_period['revenue'].idxmax()]['month_name'],
                        f"{(1 - campaign_period['revenue'].std() / campaign_avg):.1%}" if campaign_avg > 0 else "N/A"
                    ]
                })
                
                st.dataframe(kpi_df, use_container_width=True, hide_index=True)
            else:
                st.info("Baseline revenue data needed for comparison")
        else:
            st.info("Insufficient data for KPI calculation")
    else:
        st.info("KPIs will be calculated when GL transaction data is available")

with col2:
    st.markdown("#### 📈 Growth Analysis")
    
    if has_gl_data and len(campaign_revenue) > 0:
        campaign_period = campaign_revenue[
            (campaign_revenue['month'] >= pd.Timestamp(campaign_start)) &
            (campaign_revenue['month'] <= pd.Timestamp(campaign_end))
        ]
        
        if len(campaign_period) > 1:
            # Calculate cumulative growth
            campaign_period_copy = campaign_period.copy()
            campaign_period_copy['cumulative_growth'] = (
                (campaign_period_copy['revenue'] / campaign_period_copy['revenue'].iloc[0] - 1) * 100
            )
            
            fig = vh.create_line_chart(
                campaign_period_copy,
                'month_str',
                'cumulative_growth',
                'Cumulative Revenue Growth During Campaign (%)',
                color='#003366',
                show_markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Multiple months required for growth analysis")
    else:
        st.info("Growth analysis requires GL transaction data")

st.markdown("---")

# Detailed revenue table
st.markdown("### 📋 Detailed Revenue Data")

if len(campaign_revenue) > 0:
    display_revenue = extended_revenue.copy()
    display_revenue['month'] = display_revenue['month'].dt.strftime('%Y-%m-%d')
    
    display_revenue = display_revenue.rename(columns={
        'month': 'Month',
        'month_name': 'Month Name',
        'revenue': 'Total Revenue',
        'non_funded_income': 'Non-Funded Income',
        'mom_change': 'MoM Change (%)',
        'mom_change_abs': 'MoM Change (Abs)'
    })
    
    st.dataframe(
        display_revenue[['Month Name', 'Total Revenue', 'Non-Funded Income', 'MoM Change (%)', 'MoM Change (Abs)']],
        use_container_width=True,
        hide_index=True
    )
    
    # Export functionality
    st.markdown("### 📥 Export Campaign Data")
    
    csv = display_revenue.to_csv(index=False)
    st.download_button(
        label="📄 Download Campaign Analysis CSV",
        data=csv,
        file_name=f"campaign_analysis_{campaign_start.strftime('%Y%m%d')}_{campaign_end.strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
else:
    st.info("Revenue data will be displayed here when GL transactions are available")

st.markdown("---")

# Campaign insights and recommendations
st.markdown("### 💡 Insights & Recommendations")

with st.expander("📊 View Campaign Insights"):
    if has_gl_data and len(campaign_revenue) > 0:
        st.markdown("""
        Based on the campaign analysis:
        
        **Performance Highlights:**
        - Monitor month-on-month growth trends
        - Identify high-performing products and branches
        - Track revenue consistency across campaign period
        
        **Recommendations:**
        - Focus on products showing highest non-funded income
        - Replicate successful branch strategies
        - Consider extending campaign for top-performing segments
        - Analyze customer behavior during peak months
        """)
    else:
        st.markdown("""
        **Campaign Analysis Framework:**
        
        Once GL transaction data is available, this analysis will provide:
        
        1. **Revenue Performance:**
           - Total non-funded income generated
           - Month-on-month growth trends
           - Comparison with baseline period
        
        2. **Income Breakdown:**
           - Commission income (LC, guarantees, forex)
           - Service charges and fees
           - Other non-interest income sources
        
        3. **Segment Analysis:**
           - Performance by product type
           - Branch-level contributions
           - Customer segment insights
        
        4. **Effectiveness Metrics:**
           - Campaign ROI indicators
           - Customer engagement rates
           - Revenue consistency measures
        
        **Data Requirements:**
        - GL transaction data with income classification
        - Transaction timestamps for monthly aggregation
        - Product and branch attribution
        """)

# Footer
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem; border-top: 1px solid #eee; margin-top: 2rem;">
        <p>Campaign Analysis Dashboard | Updated: October 21, 2025</p>
        <p style="font-size: 0.8rem;">Non-Funded Income Campaign: June - September 2025</p>
    </div>
""", unsafe_allow_html=True)
