import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from utils.branding import apply_nmb_branding, show_nmb_logo, show_nmb_footer, create_professional_banner
import numpy as np

st.set_page_config(page_title="Promotions Analytics", page_icon="🎁", layout="wide")
apply_nmb_branding()

show_nmb_logo()

st.markdown(create_professional_banner(
    "Promotions Analytics Dashboard",
    "Promotional Campaign Performance & Customer Response Tracking",
    "🎁"
), unsafe_allow_html=True)

# Template notice
st.info("""
🔧 **Template Dashboard - Awaiting Promotions Data**

This dashboard analyzes promotional campaigns including:
- **Discount Promotions** - Interest rate discounts, fee waivers
- **Reward Programs** - Cashback, points, loyalty rewards
- **Seasonal Offers** - Holiday specials, limited-time offers
- **Product Bundles** - Package deals and cross-sell promotions
- **Referral Programs** - Customer-get-customer incentives

**To activate:** Provide promotion tracking data, redemption records, and campaign results.
""")

# Generate sample promotions data
@st.cache_data
def generate_promotions_data():
    """Generate sample promotions analytics"""
    
    # Active promotions
    promotions = pd.DataFrame({
        'promo_name': [
            'Zero Monthly Fees - 6 Months',
            'Cashback on USD Transactions',
            'Student Account Package',
            '5% Savings Boost',
            'Refer & Earn $20',
            'Free International Transfers',
            'Loan Rate Discount 2%',
            'Mobile Banking Rewards'
        ],
        'type': ['Fee Waiver', 'Cashback', 'Package Deal', 'Interest Boost', 
                 'Referral', 'Fee Waiver', 'Rate Discount', 'Rewards Points'],
        'start_date': pd.to_datetime(['2025-09-01', '2025-08-15', '2025-07-01', '2025-09-15',
                                       '2025-08-01', '2025-09-10', '2025-08-20', '2025-09-05']),
        'end_date': pd.to_datetime(['2025-12-31', '2025-11-15', '2025-12-31', '2025-12-31',
                                     '2025-12-31', '2025-11-30', '2025-11-30', '2025-11-30']),
        'target_customers': [5000, 15000, 3000, 20000, 10000, 8000, 4000, 25000],
        'actual_participants': [4250, 12800, 2650, 16200, 8400, 6100, 3200, 18500],
        'redemptions': [4250, 9800, 2650, 16200, 6200, 5500, 3200, 14200],
        'cost': [18000, 95000, 22000, 145000, 168000, 42000, 85000, 125000],
        'revenue_impact': [85000, 285000, 125000, 425000, 520000, 180000, 380000, 295000]
    })
    
    promotions['participation_rate'] = (promotions['actual_participants'] / promotions['target_customers']) * 100
    promotions['redemption_rate'] = (promotions['redemptions'] / promotions['actual_participants']) * 100
    promotions['roi'] = ((promotions['revenue_impact'] - promotions['cost']) / promotions['cost']) * 100
    promotions['status'] = 'Active'
    
    # Historical performance by month
    months = pd.date_range(end=datetime.now(), periods=6, freq='M')
    monthly_performance = pd.DataFrame({
        'month': months,
        'promotions_run': [5, 6, 7, 8, 7, 8],
        'total_participants': np.random.randint(25000, 45000, 6),
        'total_redemptions': np.random.randint(18000, 35000, 6),
        'total_cost': np.random.randint(300000, 600000, 6),
        'total_revenue': np.random.randint(800000, 1500000, 6)
    })
    
    monthly_performance['avg_participation'] = (monthly_performance['total_participants'] / monthly_performance['promotions_run'])
    monthly_performance['redemption_rate'] = (monthly_performance['total_redemptions'] / monthly_performance['total_participants']) * 100
    monthly_performance['roi'] = ((monthly_performance['total_revenue'] - monthly_performance['total_cost']) / monthly_performance['total_cost']) * 100
    
    # Customer segments
    segments = pd.DataFrame({
        'segment': ['Young Professionals', 'Students', 'SME Owners', 'Salaried Employees', 'Retirees', 'Diaspora'],
        'promotions_offered': [12, 8, 10, 15, 6, 9],
        'participation': [8400, 2650, 4200, 12500, 1800, 5100],
        'avg_redemption_rate': [72.5, 88.2, 65.8, 68.3, 52.1, 78.5],
        'revenue_per_participant': [425, 380, 1250, 520, 280, 890]
    })
    
    segments['total_revenue'] = segments['participation'] * segments['revenue_per_participant']
    
    # Promotion types effectiveness
    promo_types = pd.DataFrame({
        'type': ['Fee Waiver', 'Cashback', 'Rate Discount', 'Rewards Points', 'Referral', 'Package Deal'],
        'campaigns_run': [8, 6, 4, 5, 3, 4],
        'avg_participation_rate': [78.5, 82.3, 68.2, 72.8, 85.2, 88.5],
        'avg_redemption_rate': [95.2, 78.5, 98.5, 68.2, 72.5, 100.0],
        'avg_roi': [285, 195, 325, 145, 412, 468]
    })
    
    return promotions, monthly_performance, segments, promo_types

promotions, monthly_performance, segments, promo_types = generate_promotions_data()

# Key Metrics
st.markdown("### 📊 Active Promotions Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    active_promos = len(promotions)
    st.metric(
        "Active Promotions",
        f"{active_promos}",
        delta="2 new this month",
        help="Number of currently running promotions"
    )

with col2:
    total_participants = promotions['actual_participants'].sum()
    st.metric(
        "Total Participants",
        f"{total_participants:,}",
        delta="↑ 15.3%",
        help="Customers participating in active promotions"
    )

with col3:
    avg_redemption = promotions['redemption_rate'].mean()
    st.metric(
        "Avg Redemption Rate",
        f"{avg_redemption:.1f}%",
        delta="↑ 5.2%",
        help="Average redemption rate across all promotions"
    )

with col4:
    total_roi = promotions['roi'].mean()
    st.metric(
        "Avg ROI",
        f"{total_roi:.0f}%",
        delta="↑ 18.5%",
        help="Average return on investment"
    )

st.markdown("---")

# Active Promotions Table
st.markdown("### 🎯 Active Promotions Performance")

# Calculate days remaining
promotions['days_remaining'] = (promotions['end_date'] - datetime.now()).dt.days

st.dataframe(
    promotions[['promo_name', 'type', 'participation_rate', 'redemption_rate', 
                'roi', 'days_remaining', 'status']]
    .style.background_gradient(subset=['roi'], cmap='RdYlGn')
    .format({
        'participation_rate': '{:.1f}%',
        'redemption_rate': '{:.1f}%',
        'roi': '{:.0f}%',
        'days_remaining': '{:.0f} days'
    }),
    use_container_width=True,
    hide_index=True
)

# Performance trends
st.markdown("### 📈 Historical Promotion Performance")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Participation & Redemption Trend")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_performance['month'],
        y=monthly_performance['total_participants'],
        mode='lines+markers',
        name='Participants',
        line=dict(color='#003366', width=2),
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly_performance['month'],
        y=monthly_performance['total_redemptions'],
        mode='lines+markers',
        name='Redemptions',
        line=dict(color='#FFD700', width=2),
        yaxis='y'
    ))
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Count",
        hovermode='x unified',
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### ROI Trend")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=monthly_performance['month'],
        y=monthly_performance['roi'],
        marker_color='#00AA00',
        text=monthly_performance['roi'].apply(lambda x: f"{x:.0f}%"),
        textposition='outside'
    ))
    
    fig.add_hline(y=200, line_dash="dash", line_color="red",
                  annotation_text="Target ROI (200%)")
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="ROI (%)",
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Promotion types comparison
st.markdown("### 🔍 Promotion Type Effectiveness")

col1, col2 = st.columns([2, 1])

with col1:
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Participation Rate',
        x=promo_types['type'],
        y=promo_types['avg_participation_rate'],
        marker_color='#003366'
    ))
    
    fig.add_trace(go.Bar(
        name='Redemption Rate',
        x=promo_types['type'],
        y=promo_types['avg_redemption_rate'],
        marker_color='#FFD700'
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title="Promotion Type",
        yaxis_title="Rate (%)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### ROI by Type")
    
    promo_types_sorted = promo_types.sort_values('avg_roi', ascending=False)
    
    for _, row in promo_types_sorted.iterrows():
        st.metric(
            row['type'],
            f"{row['avg_roi']:.0f}%",
            help=f"Average ROI from {row['campaigns_run']} campaigns"
        )

# Customer segment analysis
st.markdown("### 👥 Performance by Customer Segment")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Participation by Segment")
    
    fig = px.pie(
        segments,
        values='participation',
        names='segment',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Revenue per Participant")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=segments['segment'],
        x=segments['revenue_per_participant'],
        orientation='h',
        marker=dict(
            color=segments['revenue_per_participant'],
            colorscale='Greens',
            showscale=False
        ),
        text=segments['revenue_per_participant'].apply(lambda x: f"${x:.0f}"),
        textposition='auto'
    ))
    
    fig.update_layout(
        xaxis_title="Revenue per Participant ($)",
        yaxis_title="Segment",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Top performing promotions
st.markdown("### 🏆 Top Performing Promotions")

top_promos = promotions.nlargest(5, 'roi')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Highest ROI")
    for _, promo in top_promos.iterrows():
        st.markdown(f"""
        <div style="border-left: 4px solid #00AA00; padding: 0.5rem; margin: 0.5rem 0; background: #f8f9fa;">
            <strong>{promo['promo_name']}</strong><br/>
            <span style="color: #00AA00; font-size: 1.2rem;">{promo['roi']:.0f}%</span> ROI
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("#### Highest Participation")
    top_participation = promotions.nlargest(5, 'participation_rate')
    for _, promo in top_participation.iterrows():
        st.markdown(f"""
        <div style="border-left: 4px solid #003366; padding: 0.5rem; margin: 0.5rem 0; background: #f8f9fa;">
            <strong>{promo['promo_name']}</strong><br/>
            <span style="color: #003366; font-size: 1.2rem;">{promo['participation_rate']:.1f}%</span> participation
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown("#### Highest Redemption")
    top_redemption = promotions.nlargest(5, 'redemption_rate')
    for _, promo in top_redemption.iterrows():
        st.markdown(f"""
        <div style="border-left: 4px solid #FFD700; padding: 0.5rem; margin: 0.5rem 0; background: #f8f9fa;">
            <strong>{promo['promo_name']}</strong><br/>
            <span style="color: #cc8800; font-size: 1.2rem;">{promo['redemption_rate']:.1f}%</span> redeemed
        </div>
        """, unsafe_allow_html=True)

# Recommendations
st.markdown("### 💡 Recommendations & Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🟢 What's Working
    
    1. **Package Deals** show highest ROI (468%)
       - Continue bundling products
       - Expand to more segments
    
    2. **Referral Programs** drive growth (412% ROI)
       - Increase referral incentives
       - Launch viral campaigns
    
    3. **Students** have highest redemption (88.2%)
       - Create more student-focused offers
       - Partner with universities
    
    4. **Fee Waivers** achieve 95% redemption
       - Simple, clear value proposition
       - Replicate for other products
    """)

with col2:
    st.markdown("""
    #### 🔴 Areas for Improvement
    
    1. **Rewards Points** underperforming (145% ROI)
       - Simplify redemption process
       - Increase point values
    
    2. **Retirees** low participation (52% redemption)
       - Tailor offers to this segment
       - Improve communication channels
    
    3. **Rate Discounts** low participation (68%)
       - Better promotion visibility
       - Clearer terms and conditions
    
    4. **Mid-month promotions** lag behind
       - Shift major launches to month-start
       - Align with salary cycles
    """)

# Export
st.markdown("---")
if st.button("Download Promotions Report", key="download_promos"):
    st.info("Export functionality will be activated when connected to real promotions data.")

# Integration guide
with st.expander("🔌 Promotions Data Integration Guide"):
    st.markdown("""
    ### Activate Promotions Analytics
    
    **Required Data Sources:**
    
    1. **Promotion Campaign Data**
       - Campaign name, type, start/end dates
       - Target audience and eligibility criteria
       - Promotion terms (discount %, fee waiver, cashback amount)
    
    2. **Participation Tracking**
       - Customer opt-ins
       - Promo code usage
       - Eligibility verification
    
    3. **Redemption Data**
       - Redemption timestamps
       - Redemption amounts/values
       - Product/service redeemed
    
    4. **Cost Tracking**
       - Promotion setup costs
       - Discount amounts granted
       - Operational costs
    
    5. **Revenue Attribution**
       - Revenue from promotion participants
       - Incremental revenue vs. baseline
       - Customer retention post-promotion
    
    **Integration Steps:**
    1. Link promotion management system
    2. Connect customer participation tracking
    3. Set up redemption event tracking
    4. Configure cost allocation model
    5. Link revenue attribution system
    6. Validate data flows
    7. Dashboard activates automatically
    
    **Contact:** bi@nmbz.co.zw for promotions data integration
    """)

show_nmb_footer()
