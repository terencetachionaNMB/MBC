import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from utils.branding import apply_nmb_branding, show_nmb_logo, show_nmb_footer, create_professional_banner
import numpy as np

st.set_page_config(page_title="Advertising Performance", page_icon="📺", layout="wide")
apply_nmb_branding()

show_nmb_logo()

st.markdown(create_professional_banner(
    "Advertising Performance Dashboard",
    "Multi-Channel Advertising Campaign Metrics & Attribution Analysis",
    "📺"
), unsafe_allow_html=True)

# Template notice
st.info("""
🔧 **Template Dashboard - Awaiting Advertising Data**

This dashboard tracks advertising performance across:
- **Digital Ads** - Google Ads, Facebook Ads, LinkedIn Ads, programmatic display
- **Traditional Media** - TV, radio, print, outdoor (billboards)
- **Video Advertising** - YouTube, TikTok, streaming platforms
- **Search Marketing** - SEM/PPC campaigns, keyword performance
- **Display Advertising** - Banner ads, native advertising

**To activate:** Connect ad platforms APIs, media buying data, and attribution tracking.
""")

# Generate sample advertising data
@st.cache_data
def generate_advertising_data():
    """Generate sample advertising performance data"""
    
    # Ad campaigns
    campaigns = pd.DataFrame({
        'campaign': [
            'Google Search - Savings Accounts',
            'Facebook - Youth Banking',
            'YouTube - Digital Banking',
            'TV Campaign - Brand Awareness',
            'LinkedIn - SME Banking',
            'Radio - Personal Loans',
            'Billboard - Branch Locations',
            'Display Network - Credit Cards'
        ],
        'channel': ['Search', 'Social Media', 'Video', 'TV', 'Social Media', 'Radio', 'OOH', 'Display'],
        'budget': [45000, 32000, 28000, 95000, 22000, 18000, 42000, 25000],
        'spend': [43500, 31200, 27500, 92000, 21500, 17800, 42000, 24200],
        'impressions': [2850000, 5420000, 3250000, 8500000, 980000, 6200000, 4500000, 7800000],
        'clicks': [85500, 162600, 97500, 0, 29400, 0, 0, 234000],
        'conversions': [1280, 2438, 1462, 3400, 441, 1240, 950, 3510],
        'revenue': [185000, 365000, 219000, 680000, 88000, 248000, 190000, 526000]
    })
    
    # Calculate metrics
    campaigns['cpm'] = (campaigns['spend'] / campaigns['impressions']) * 1000
    campaigns['ctr'] = np.where(campaigns['clicks'] > 0, (campaigns['clicks'] / campaigns['impressions']) * 100, 0)
    campaigns['cpc'] = np.where(campaigns['clicks'] > 0, campaigns['spend'] / campaigns['clicks'], 0)
    campaigns['cpa'] = campaigns['spend'] / campaigns['conversions']
    campaigns['roas'] = (campaigns['revenue'] / campaigns['spend']) * 100
    campaigns['roi'] = ((campaigns['revenue'] - campaigns['spend']) / campaigns['spend']) * 100
    
    # Daily performance (last 30 days)
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    daily_performance = pd.DataFrame({
        'date': dates,
        'impressions': np.random.randint(800000, 1500000, 30),
        'clicks': np.random.randint(25000, 50000, 30),
        'spend': np.random.randint(8000, 15000, 30),
        'conversions': np.random.randint(350, 700, 30)
    })
    
    daily_performance['ctr'] = (daily_performance['clicks'] / daily_performance['impressions']) * 100
    daily_performance['cvr'] = (daily_performance['conversions'] / daily_performance['clicks']) * 100
    
    # Channel comparison
    channel_summary = campaigns.groupby('channel').agg({
        'spend': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    channel_summary['roi'] = ((channel_summary['revenue'] - channel_summary['spend']) / channel_summary['spend']) * 100
    channel_summary['cpa'] = channel_summary['spend'] / channel_summary['conversions']
    channel_summary['ctr'] = np.where(channel_summary['clicks'] > 0, 
                                      (channel_summary['clicks'] / channel_summary['impressions']) * 100, 0)
    
    # Ad creative performance
    creatives = pd.DataFrame({
        'creative_id': ['CR-001', 'CR-002', 'CR-003', 'CR-004', 'CR-005'],
        'type': ['Image', 'Video', 'Carousel', 'Video', 'Image'],
        'headline': [
            'Save More with 5% Interest',
            'Banking Made Simple',
            'Your Financial Partner',
            'Digital Banking Revolution',
            'Loans Up to $50K'
        ],
        'impressions': [1250000, 2180000, 980000, 1650000, 1120000],
        'clicks': [37500, 87200, 29400, 66000, 33600],
        'conversions': [562, 1308, 441, 990, 504],
        'spend': [12500, 21800, 9800, 16500, 11200]
    })
    
    creatives['ctr'] = (creatives['clicks'] / creatives['impressions']) * 100
    creatives['cvr'] = (creatives['conversions'] / creatives['clicks']) * 100
    creatives['cpa'] = creatives['spend'] / creatives['conversions']
    
    # Audience segments
    audiences = pd.DataFrame({
        'segment': ['18-24 Youth', '25-34 Young Prof', '35-44 Established', '45-54 Mid-Career', '55+ Retirees'],
        'impressions': [2850000, 4200000, 3500000, 2100000, 1450000],
        'spend': [28500, 42000, 35000, 21000, 14500],
        'conversions': [428, 630, 525, 315, 218],
        'engagement_rate': [4.2, 5.8, 4.5, 3.2, 2.8]
    })
    
    audiences['cpa'] = audiences['spend'] / audiences['conversions']
    
    return campaigns, daily_performance, channel_summary, creatives, audiences

campaigns, daily_performance, channel_summary, creatives, audiences = generate_advertising_data()

# Key Metrics
st.markdown("### 📊 Advertising Performance Overview (Current Month)")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_spend = campaigns['spend'].sum()
    budget_utilization = (total_spend / campaigns['budget'].sum()) * 100
    st.metric(
        "Total Ad Spend",
        f"${total_spend:,.0f}",
        delta=f"{budget_utilization:.0f}% of budget",
        help="Total advertising expenditure this month"
    )

with col2:
    total_impressions = campaigns['impressions'].sum()
    st.metric(
        "Total Impressions",
        f"{total_impressions/1000000:.1f}M",
        delta="↑ 12.5%",
        help="Total ad impressions across all channels"
    )

with col3:
    total_clicks = campaigns['clicks'].sum()
    avg_ctr = (total_clicks / total_impressions) * 100
    st.metric(
        "Avg Click-Through Rate",
        f"{avg_ctr:.2f}%",
        delta="↑ 0.3%",
        help="Average CTR across all digital campaigns"
    )

with col4:
    total_conversions = campaigns['conversions'].sum()
    st.metric(
        "Total Conversions",
        f"{total_conversions:,}",
        delta="↑ 18.2%",
        help="Total conversions from advertising"
    )

with col5:
    avg_roas = campaigns['roas'].mean()
    st.metric(
        "Avg ROAS",
        f"{avg_roas:.0f}%",
        delta="↑ 25%",
        help="Average Return on Ad Spend"
    )

st.markdown("---")

# Campaign Performance Table
st.markdown("### 🎯 Campaign Performance Breakdown")

st.dataframe(
    campaigns[['campaign', 'channel', 'spend', 'impressions', 'clicks', 'conversions', 
               'ctr', 'cpa', 'roas']]
    .style.background_gradient(subset=['roas'], cmap='RdYlGn')
    .format({
        'spend': '${:,.0f}',
        'impressions': '{:,.0f}',
        'clicks': '{:,.0f}',
        'conversions': '{:,}',
        'ctr': '{:.2f}%',
        'cpa': '${:.2f}',
        'roas': '{:.0f}%'
    }),
    use_container_width=True,
    hide_index=True
)

# Daily trends
st.markdown("### 📈 Daily Performance Trends (Last 30 Days)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Impressions & Clicks")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_performance['date'],
        y=daily_performance['impressions'],
        name='Impressions',
        line=dict(color='#003366', width=2),
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_performance['date'],
        y=daily_performance['clicks'],
        name='Clicks',
        line=dict(color='#FFD700', width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis=dict(title="Impressions"),
        yaxis2=dict(title="Clicks", overlaying='y', side='right'),
        hovermode='x unified',
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### CTR & CVR Trends")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_performance['date'],
        y=daily_performance['ctr'],
        name='CTR',
        line=dict(color='#003366', width=2),
        fill='tonexty'
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_performance['date'],
        y=daily_performance['cvr'],
        name='CVR',
        line=dict(color='#00AA00', width=2),
        fill='tonexty'
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Rate (%)",
        hovermode='x unified',
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Channel comparison
st.markdown("### 📡 Channel Performance Comparison")

metric_choice = st.selectbox(
    "Select Metric to Compare",
    ["ROI", "Cost per Acquisition", "Click-Through Rate", "Total Conversions"]
)

col1, col2 = st.columns([2, 1])

with col1:
    if metric_choice == "ROI":
        metric_col = 'roi'
        title = "ROI by Channel"
        format_str = "{:.0f}%"
    elif metric_choice == "Cost per Acquisition":
        metric_col = 'cpa'
        title = "Cost per Acquisition by Channel"
        format_str = "${:.2f}"
    elif metric_choice == "Click-Through Rate":
        metric_col = 'ctr'
        title = "CTR by Channel"
        format_str = "{:.2f}%"
    else:
        metric_col = 'conversions'
        title = "Total Conversions by Channel"
        format_str = "{:,.0f}"
    
    channel_sorted = channel_summary.sort_values(metric_col, ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=channel_sorted['channel'],
        x=channel_sorted[metric_col],
        orientation='h',
        marker=dict(
            color=channel_sorted[metric_col],
            colorscale='Viridis',
            showscale=False
        ),
        text=channel_sorted[metric_col].apply(lambda x: format_str.format(x)),
        textposition='auto'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=metric_choice,
        yaxis_title="Channel",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Channel Summary")
    
    for _, row in channel_sorted.iterrows():
        with st.container():
            st.markdown(f"**{row['channel']}**")
            st.write(f"Spend: ${row['spend']:,.0f}")
            st.write(f"Conv: {row['conversions']:,.0f}")
            st.write(f"ROI: {row['roi']:.0f}%")
            st.markdown("---")

# Creative performance
st.markdown("### 🎨 Ad Creative Performance")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### Top Performing Creatives")
    
    creatives_top = creatives.nlargest(5, 'cvr')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=creatives_top['ctr'],
        y=creatives_top['cvr'],
        mode='markers+text',
        marker=dict(
            size=creatives_top['conversions']/10,
            color=creatives_top['cpa'],
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="CPA ($)")
        ),
        text=creatives_top['creative_id'],
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>CTR: %{x:.2f}%<br>CVR: %{y:.2f}%<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title="Click-Through Rate (%)",
        yaxis_title="Conversion Rate (%)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Creative Details")
    
    st.dataframe(
        creatives[['creative_id', 'type', 'ctr', 'cvr', 'cpa']]
        .style.format({
            'ctr': '{:.2f}%',
            'cvr': '{:.2f}%',
            'cpa': '${:.2f}'
        }),
        use_container_width=True,
        hide_index=True,
        height=350
    )

# Audience performance
st.markdown("### 👥 Audience Segment Performance")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Conversions by Age Group")
    
    fig = px.pie(
        audiences,
        values='conversions',
        names='segment',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Cost per Acquisition by Segment")
    
    audiences_sorted = audiences.sort_values('cpa')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=audiences_sorted['segment'],
        y=audiences_sorted['cpa'],
        marker_color='#003366',
        text=audiences_sorted['cpa'].apply(lambda x: f"${x:.2f}"),
        textposition='outside'
    ))
    
    fig.update_layout(
        xaxis_title="Age Segment",
        yaxis_title="Cost per Acquisition ($)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Budget allocation
st.markdown("### 💰 Budget Allocation & Utilization")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Spend by Channel")
    
    fig = px.pie(
        channel_summary,
        values='spend',
        names='channel',
        color_discrete_sequence=px.colors.sequential.YlGnBu_r
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label+value',
                     texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}')
    fig.update_layout(height=350)
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Campaign Budget vs Actual")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Budget',
        x=campaigns['campaign'].str[:20],
        y=campaigns['budget'],
        marker_color='lightgray'
    ))
    
    fig.add_trace(go.Bar(
        name='Actual Spend',
        x=campaigns['campaign'].str[:20],
        y=campaigns['spend'],
        marker_color='#003366'
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title="Campaign",
        yaxis_title="Amount ($)",
        height=350,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Recommendations
st.markdown("### 💡 Optimization Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🟢 Scale These Winners
    
    1. **Facebook - Youth Banking** (565% ROAS)
       - Increase budget by 50%
       - Expand to similar audiences
       - Test additional creatives
    
    2. **Display Network** (2073% ROAS)
       - Scale impressions
       - Optimize placements
       - A/B test new creatives
    
    3. **Video Creatives** perform best
       - Allocate 40% budget to video
       - Produce more video content
       - Test different lengths
    
    4. **25-34 Age Group** most responsive
       - Focus ad targeting
       - Tailor messaging
       - Higher budget allocation
    """)

with col2:
    st.markdown("""
    #### 🔴 Optimize or Pause
    
    1. **LinkedIn - SME Banking** (309% ROAS)
       - Below average performance
       - Review targeting criteria
       - Consider reducing budget
    
    2. **Radio Campaigns** - Hard to track
       - Implement unique promo codes
       - Better attribution methods
       - Compare with digital channels
    
    3. **Billboard/OOH** - Low conversion tracking
       - Add QR codes for tracking
       - Use location-based targeting
       - Measure brand lift surveys
    
    4. **55+ Retirees** - Higher CPA
       - Adjust creative messaging
       - Test different channels
       - Simplify conversion process
    """)

# Export
st.markdown("---")
if st.button("Download Advertising Report", key="download_ads"):
    st.info("Export functionality will be activated when connected to real advertising platforms.")

# Integration guide
with st.expander("🔌 Advertising Data Integration Guide"):
    st.markdown("""
    ### Activate Advertising Performance Dashboard
    
    **Required Platform Integrations:**
    
    1. **Google Ads API**
       - Campaign performance data
       - Keyword metrics
       - Ad creative performance
       - Audience insights
    
    2. **Facebook Ads Manager API**
       - Campaign metrics
       - Ad set performance
       - Creative analytics
       - Audience demographics
    
    3. **LinkedIn Campaign Manager**
       - B2B campaign data
       - Professional targeting metrics
       - Lead generation forms
    
    4. **YouTube Analytics API**
       - Video ad performance
       - View-through rates
       - Audience retention
    
    5. **Traditional Media Tracking**
       - TV viewership data (Nielsen, GRPs)
       - Radio listenership metrics
       - Print circulation data
       - Billboard location/impressions
    
    6. **Attribution Platform**
       - Multi-touch attribution
       - Conversion path analysis
       - Cross-channel ROI
    
    **Integration Steps:**
    1. Obtain API credentials for each platform
    2. Set up data connectors
    3. Configure conversion tracking pixels
    4. Link attribution system
    5. Validate data accuracy
    6. Set up automated daily sync
    7. Dashboard activates automatically
    
    **Contact:** bi@nmbz.co.zw for advertising platform integration
    """)

show_nmb_footer()
