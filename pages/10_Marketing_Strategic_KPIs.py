import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from utils.branding import apply_nmb_branding, show_nmb_logo, show_nmb_footer, create_professional_banner
import numpy as np

st.set_page_config(page_title="Marketing Strategic KPIs", page_icon="📊", layout="wide")
apply_nmb_branding()

show_nmb_logo()

st.markdown(create_professional_banner(
    "Marketing Strategic KPIs Dashboard",
    "Executive-Level Marketing Performance Indicators & Business Impact",
    "📊"
), unsafe_allow_html=True)

# Template notice
st.info("""
🔧 **Template Dashboard - Awaiting Marketing Data Integration**

This dashboard tracks strategic marketing KPIs including:
- **Customer Acquisition Cost (CAC)** - Cost to acquire new customers
- **Customer Lifetime Value (CLV)** - Projected revenue per customer
- **Marketing ROI** - Return on marketing investment
- **Brand Awareness** - Market share and brand recognition metrics
- **Lead Conversion Rate** - Lead-to-customer conversion efficiency
- **Channel Performance** - Multi-channel marketing effectiveness

**To activate:** Provide marketing spend data, attribution models, and conversion tracking.
""")

# Generate sample KPI data
@st.cache_data
def generate_marketing_kpis():
    """Generate sample marketing KPI data"""
    
    months = pd.date_range(end=datetime.now(), periods=12, freq='M')
    
    # Core marketing KPIs
    kpis = pd.DataFrame({
        'month': months,
        'new_customers': np.random.randint(800, 1500, 12),
        'marketing_spend': np.random.randint(50000, 120000, 12),
        'revenue_generated': np.random.randint(200000, 500000, 12),
        'leads_generated': np.random.randint(3000, 6000, 12),
        'leads_converted': np.random.randint(800, 1500, 12),
        'brand_awareness': np.random.uniform(45, 75, 12),  # percentage
        'customer_satisfaction': np.random.uniform(70, 90, 12)  # percentage
    })
    
    # Calculate derived metrics
    kpis['cac'] = kpis['marketing_spend'] / kpis['new_customers']
    kpis['roi'] = ((kpis['revenue_generated'] - kpis['marketing_spend']) / kpis['marketing_spend']) * 100
    kpis['conversion_rate'] = (kpis['leads_converted'] / kpis['leads_generated']) * 100
    kpis['clv'] = np.random.uniform(5000, 15000, 12)  # Estimated CLV
    
    # Channel performance
    channels = pd.DataFrame({
        'channel': ['Digital Advertising', 'Social Media', 'Email Marketing', 'Content Marketing', 
                    'Events & Sponsorships', 'Referral Program', 'TV/Radio', 'Print Media'],
        'spend': [45000, 28000, 12000, 18000, 35000, 8000, 42000, 15000],
        'leads': [2850, 3200, 1800, 1400, 950, 1200, 1600, 800],
        'conversions': [420, 580, 280, 210, 140, 280, 220, 95],
        'revenue': [180000, 245000, 125000, 95000, 68000, 135000, 98000, 42000]
    })
    
    channels['cpl'] = channels['spend'] / channels['leads']  # Cost per lead
    channels['cpa'] = channels['spend'] / channels['conversions']  # Cost per acquisition
    channels['roi'] = ((channels['revenue'] - channels['spend']) / channels['spend']) * 100
    
    # Campaign performance
    campaigns = pd.DataFrame({
        'campaign': ['Summer Savings Drive', 'Digital Account Opening', 'Youth Banking Initiative', 
                     'SME Growth Package', 'Diaspora Remittance Promo'],
        'budget': [85000, 65000, 55000, 75000, 45000],
        'actual_spend': [82000, 68000, 52000, 73000, 43000],
        'leads': [4200, 5800, 3100, 2400, 1800],
        'conversions': [520, 890, 385, 310, 245],
        'revenue': [285000, 445000, 195000, 380000, 165000],
        'status': ['Completed', 'Completed', 'Completed', 'Completed', 'Completed']
    })
    
    campaigns['roi'] = ((campaigns['revenue'] - campaigns['actual_spend']) / campaigns['actual_spend']) * 100
    campaigns['conversion_rate'] = (campaigns['conversions'] / campaigns['leads']) * 100
    
    # Market share trend
    market_share = pd.DataFrame({
        'quarter': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025'],
        'nmb_share': [18.5, 19.2, 19.8, 20.1, 20.5, 21.2, 21.8],
        'target_share': [19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0]
    })
    
    return kpis, channels, campaigns, market_share

kpis, channels, campaigns, market_share = generate_marketing_kpis()

# Key Metrics Dashboard
st.markdown("### 📊 Strategic Marketing KPIs (Current Month)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    current_cac = kpis['cac'].iloc[-1]
    prev_cac = kpis['cac'].iloc[-2]
    delta_cac = ((current_cac - prev_cac) / prev_cac) * 100
    st.metric(
        "Customer Acquisition Cost",
        f"${current_cac:.2f}",
        delta=f"{delta_cac:.1f}%",
        delta_color="inverse",
        help="Average cost to acquire one new customer"
    )

with col2:
    current_roi = kpis['roi'].iloc[-1]
    st.metric(
        "Marketing ROI",
        f"{current_roi:.1f}%",
        delta="↑ 5.2%",
        help="Return on marketing investment"
    )

with col3:
    current_clv = kpis['clv'].iloc[-1]
    st.metric(
        "Customer Lifetime Value",
        f"${current_clv:,.0f}",
        delta="↑ $450",
        help="Estimated revenue per customer over lifetime"
    )

with col4:
    current_conversion = kpis['conversion_rate'].iloc[-1]
    st.metric(
        "Lead Conversion Rate",
        f"{current_conversion:.1f}%",
        delta="↑ 2.1%",
        help="Percentage of leads converted to customers"
    )

st.markdown("---")

# CLV vs CAC Ratio
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💰 CLV to CAC Ratio Trend")
    
    kpis['clv_cac_ratio'] = kpis['clv'] / kpis['cac']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=kpis['month'],
        y=kpis['clv_cac_ratio'],
        mode='lines+markers',
        name='CLV:CAC Ratio',
        line=dict(color='#003366', width=3),
        marker=dict(size=8)
    ))
    
    # Add target line (3:1 is healthy)
    fig.add_hline(y=3, line_dash="dash", line_color="green", 
                  annotation_text="Healthy Ratio (3:1)")
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Ratio",
        hovermode='x unified',
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    current_ratio = kpis['clv_cac_ratio'].iloc[-1]
    if current_ratio >= 3:
        st.success(f"✅ Current ratio: {current_ratio:.1f}:1 (Healthy)")
    else:
        st.warning(f"⚠️ Current ratio: {current_ratio:.1f}:1 (Below target)")

with col2:
    st.markdown("### 📈 Marketing ROI Trend")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=kpis['month'],
        y=kpis['roi'],
        marker_color='#FFD700',
        text=kpis['roi'].apply(lambda x: f"{x:.0f}%"),
        textposition='outside'
    ))
    
    fig.add_hline(y=200, line_dash="dash", line_color="green",
                  annotation_text="Target ROI (200%)")
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="ROI (%)",
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Channel Performance Analysis
st.markdown("### 📡 Channel Performance Comparison")

channel_metric = st.selectbox(
    "Select Metric to Compare",
    ["ROI (%)", "Cost per Lead", "Cost per Acquisition", "Conversion Rate"]
)

if channel_metric == "ROI (%)":
    metric_col = 'roi'
    title = "ROI by Channel"
    format_func = lambda x: f"{x:.0f}%"
elif channel_metric == "Cost per Lead":
    metric_col = 'cpl'
    title = "Cost per Lead by Channel"
    format_func = lambda x: f"${x:.2f}"
elif channel_metric == "Cost per Acquisition":
    metric_col = 'cpa'
    title = "Cost per Acquisition by Channel"
    format_func = lambda x: f"${x:.2f}"
else:
    channels['conversion_rate'] = (channels['conversions'] / channels['leads']) * 100
    metric_col = 'conversion_rate'
    title = "Conversion Rate by Channel"
    format_func = lambda x: f"{x:.1f}%"

channels_sorted = channels.sort_values(metric_col, ascending=False)

fig = go.Figure()

fig.add_trace(go.Bar(
    y=channels_sorted['channel'],
    x=channels_sorted[metric_col],
    orientation='h',
    marker=dict(
        color=channels_sorted[metric_col],
        colorscale='Viridis',
        showscale=False
    ),
    text=channels_sorted[metric_col].apply(format_func),
    textposition='auto'
))

fig.update_layout(
    title=title,
    xaxis_title=channel_metric,
    yaxis_title="Channel",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Campaign Performance
st.markdown("### 🎯 Campaign Performance Summary")

# Calculate additional metrics
campaigns['efficiency'] = campaigns['roi'] / (campaigns['actual_spend'] / 1000)  # ROI per $1K spent

st.dataframe(
    campaigns[['campaign', 'actual_spend', 'leads', 'conversions', 'revenue', 'roi', 'conversion_rate']]
    .style.background_gradient(subset=['roi'], cmap='RdYlGn')
    .format({
        'actual_spend': '${:,.0f}',
        'leads': '{:,}',
        'conversions': '{:,}',
        'revenue': '${:,.0f}',
        'roi': '{:.1f}%',
        'conversion_rate': '{:.1f}%'
    }),
    use_container_width=True,
    hide_index=True
)

# Market Share Trend
st.markdown("### 📊 Market Share Performance")

col1, col2 = st.columns([2, 1])

with col1:
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=market_share['quarter'],
        y=market_share['nmb_share'],
        mode='lines+markers',
        name='Actual Market Share',
        line=dict(color='#003366', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=market_share['quarter'],
        y=market_share['target_share'],
        mode='lines+markers',
        name='Target Market Share',
        line=dict(color='#FFD700', width=2, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        xaxis_title="Quarter",
        yaxis_title="Market Share (%)",
        hovermode='x unified',
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Market Position")
    
    current_share = market_share['nmb_share'].iloc[-1]
    target_share = market_share['target_share'].iloc[-1]
    gap = current_share - target_share
    
    st.metric("Current Market Share", f"{current_share}%")
    st.metric("Target Market Share", f"{target_share}%")
    
    if gap >= 0:
        st.success(f"✅ On target (+{gap:.1f}%)")
    else:
        st.warning(f"⚠️ Below target ({gap:.1f}%)")
    
    st.markdown("#### Competitive Position")
    st.info("Rank: #3 in Zimbabwe banking sector")

# Marketing Funnel
st.markdown("### 🎯 Marketing Funnel Analysis")

col1, col2 = st.columns([2, 1])

with col1:
    # Last month funnel
    total_reach = 150000
    awareness = kpis['leads_generated'].iloc[-1]
    consideration = awareness * 0.65
    intent = kpis['leads_converted'].iloc[-1]
    customers = kpis['new_customers'].iloc[-1]
    
    funnel_data = pd.DataFrame({
        'stage': ['Total Reach', 'Awareness (Leads)', 'Consideration', 'Intent (Qualified)', 'Customers'],
        'count': [total_reach, awareness, consideration, intent, customers]
    })
    
    fig = go.Figure(go.Funnel(
        y=funnel_data['stage'],
        x=funnel_data['count'],
        textinfo="value+percent initial",
        marker=dict(color=['#004080', '#003366', '#0066AA', '#FFD700', '#00AA00'])
    ))
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Conversion Rates")
    
    st.metric(
        "Reach → Awareness",
        f"{(awareness/total_reach*100):.1f}%",
        help="Percentage of reached audience that became leads"
    )
    
    st.metric(
        "Awareness → Consideration",
        f"{(consideration/awareness*100):.1f}%",
        help="Leads showing interest"
    )
    
    st.metric(
        "Consideration → Intent",
        f"{(intent/consideration*100):.1f}%",
        help="Qualified leads ready to convert"
    )
    
    st.metric(
        "Intent → Customer",
        f"{(customers/intent*100):.1f}%",
        help="Final conversion to customers"
    )

# Brand Health Metrics
st.markdown("### 🏆 Brand Health Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Brand Awareness")
    current_awareness = kpis['brand_awareness'].iloc[-1]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_awareness,
        delta={'reference': 65, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#003366"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 65
            }
        }
    ))
    
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Customer Satisfaction")
    current_csat = kpis['customer_satisfaction'].iloc[-1]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_csat,
        delta={'reference': 80, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#FFD700"},
            'steps': [
                {'range': [0, 70], 'color': "lightgray"},
                {'range': [70, 85], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown("#### Net Promoter Score")
    nps_score = 68
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=nps_score,
        delta={'reference': 60, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [-100, 100]},
            'bar': {'color': "#00AA00"},
            'steps': [
                {'range': [-100, 0], 'color': "lightcoral"},
                {'range': [0, 50], 'color': "lightyellow"},
                {'range': [50, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "green", 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)

# Export
st.markdown("---")
if st.button("Download Marketing KPIs Report", key="download_kpis"):
    st.info("Export functionality will be activated when connected to real marketing data sources.")

# Integration guide
with st.expander("🔌 Marketing Data Integration Guide"):
    st.markdown("""
    ### Activate Marketing KPIs Dashboard
    
    **Required Data Sources:**
    
    1. **Marketing Spend Data**
       - Budget allocation by channel
       - Actual spend tracking
       - Campaign-specific costs
    
    2. **Lead Generation & Conversion**
       - CRM system integration (Salesforce, HubSpot)
       - Lead source attribution
       - Conversion tracking throughout funnel
    
    3. **Revenue Attribution**
       - Link customers to marketing touchpoints
       - Campaign revenue tracking
       - Customer lifetime value calculations
    
    4. **Brand Metrics**
       - Market research data (brand awareness surveys)
       - NPS surveys
       - Customer satisfaction scores
       - Market share reports (industry sources)
    
    5. **Web & Digital Analytics**
       - Google Analytics or similar
       - Ad platform data (Google Ads, Facebook Ads)
       - Email marketing metrics
    
    **Integration Steps:**
    1. Connect CRM system API
    2. Link marketing spend tracking system
    3. Set up attribution model (first-touch, last-touch, multi-touch)
    4. Configure revenue tracking
    5. Import brand health surveys
    6. Validate data accuracy
    7. Dashboard activates automatically
    
    **Contact:** bi@nmbz.co.zw for marketing data integration
    """)

show_nmb_footer()
