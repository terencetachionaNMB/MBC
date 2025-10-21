import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.branding import apply_nmb_branding, show_nmb_logo, show_nmb_footer, create_professional_banner

st.set_page_config(page_title="Customer Engagement Analytics", page_icon="📱", layout="wide")
apply_nmb_branding()

show_nmb_logo()

st.markdown(create_professional_banner(
    "Customer Engagement Analytics",
    "Multi-Channel Customer Interaction & Engagement Metrics",
    "📱"
), unsafe_allow_html=True)

# Template data notice
st.info("""
🔧 **Template Dashboard - Awaiting Data Integration**

This dashboard is ready for customer engagement data from:
- Email campaigns (opens, clicks, conversions)
- SMS campaigns (delivery, response rates)
- Mobile app usage (sessions, feature usage)
- Website analytics (page views, time on site)
- Customer portal interactions

**To activate:** Provide engagement data CSV files or API credentials.
""")

# Generate sample template data
@st.cache_data
def generate_sample_engagement_data():
    """Generate sample engagement metrics for demonstration"""
    import numpy as np
    
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    
    # Email engagement
    email_data = pd.DataFrame({
        'date': dates,
        'emails_sent': np.random.randint(5000, 15000, 90),
        'emails_opened': np.random.randint(1500, 8000, 90),
        'emails_clicked': np.random.randint(500, 3000, 90),
        'conversions': np.random.randint(50, 500, 90)
    })
    
    # SMS engagement
    sms_data = pd.DataFrame({
        'date': dates,
        'sms_sent': np.random.randint(2000, 8000, 90),
        'sms_delivered': np.random.randint(1800, 7500, 90),
        'sms_responses': np.random.randint(100, 1000, 90)
    })
    
    # App engagement
    app_data = pd.DataFrame({
        'date': dates,
        'active_users': np.random.randint(10000, 30000, 90),
        'sessions': np.random.randint(15000, 45000, 90),
        'avg_session_duration': np.random.uniform(3, 12, 90)  # minutes
    })
    
    # Web engagement
    web_data = pd.DataFrame({
        'date': dates,
        'page_views': np.random.randint(50000, 150000, 90),
        'unique_visitors': np.random.randint(20000, 60000, 90),
        'bounce_rate': np.random.uniform(25, 55, 90)  # percentage
    })
    
    # Channel engagement by segment
    channel_segments = pd.DataFrame({
        'channel': ['Email', 'SMS', 'Mobile App', 'Web Portal', 'WhatsApp', 'Push Notifications'] * 3,
        'segment': ['Retail'] * 6 + ['Corporate'] * 6 + ['SME'] * 6,
        'engagement_rate': [45.2, 38.5, 62.1, 51.3, 55.8, 42.9,
                            52.3, 44.2, 68.5, 58.7, 61.2, 48.5,
                            48.7, 41.3, 65.2, 54.8, 58.3, 45.6],
        'active_users': [25000, 15000, 35000, 28000, 18000, 22000,
                         12000, 8000, 15000, 13000, 7000, 9000,
                         8000, 6000, 10000, 9000, 5000, 7000]
    })
    
    return email_data, sms_data, app_data, web_data, channel_segments

email_data, sms_data, app_data, web_data, channel_segments = generate_sample_engagement_data()

# Key Metrics
st.markdown("### 📊 Key Engagement Metrics (Last 30 Days)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_email_open = email_data['emails_opened'].tail(30).sum() / email_data['emails_sent'].tail(30).sum() * 100
    st.metric(
        "Email Open Rate",
        f"{avg_email_open:.1f}%",
        delta="↑ 2.3%",
        help="Percentage of emails opened from total sent"
    )

with col2:
    avg_sms_delivery = sms_data['sms_delivered'].tail(30).sum() / sms_data['sms_sent'].tail(30).sum() * 100
    st.metric(
        "SMS Delivery Rate",
        f"{avg_sms_delivery:.1f}%",
        delta="↑ 1.5%",
        help="Percentage of SMS successfully delivered"
    )

with col3:
    avg_app_users = int(app_data['active_users'].tail(30).mean())
    st.metric(
        "Avg Daily Active Users",
        f"{avg_app_users:,}",
        delta="↑ 1,234",
        help="Average mobile app active users per day"
    )

with col4:
    avg_web_visitors = int(web_data['unique_visitors'].tail(30).mean())
    st.metric(
        "Avg Daily Web Visitors",
        f"{avg_web_visitors:,}",
        delta="↑ 2,567",
        help="Average unique web portal visitors per day"
    )

st.markdown("---")

# Multi-channel engagement trends
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📧 Email Campaign Performance")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=email_data['date'],
        y=email_data['emails_sent'],
        name='Emails Sent',
        line=dict(color='#003366', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=email_data['date'],
        y=email_data['emails_opened'],
        name='Emails Opened',
        line=dict(color='#FFD700', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=email_data['date'],
        y=email_data['emails_clicked'],
        name='Emails Clicked',
        line=dict(color='#00AA00', width=2)
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Count",
        hovermode='x unified',
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📱 Mobile App Engagement")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=app_data['date'],
        y=app_data['active_users'],
        name='Active Users',
        line=dict(color='#003366', width=2),
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=app_data['date'],
        y=app_data['avg_session_duration'],
        name='Avg Session (min)',
        line=dict(color='#FFD700', width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis=dict(title="Active Users"),
        yaxis2=dict(title="Session Duration (min)", overlaying='y', side='right'),
        hovermode='x unified',
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Channel comparison
st.markdown("### 📊 Engagement Rate by Channel and Segment")

fig = go.Figure()

for segment in ['Retail', 'Corporate', 'SME']:
    segment_data = channel_segments[channel_segments['segment'] == segment]
    
    fig.add_trace(go.Bar(
        name=segment,
        x=segment_data['channel'],
        y=segment_data['engagement_rate'],
        text=segment_data['engagement_rate'].apply(lambda x: f"{x:.1f}%"),
        textposition='auto'
    ))

fig.update_layout(
    barmode='group',
    xaxis_title="Channel",
    yaxis_title="Engagement Rate (%)",
    height=400,
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

# Engagement funnel
st.markdown("### 🎯 Customer Engagement Funnel (This Month)")

col1, col2 = st.columns([2, 1])

with col1:
    funnel_data = pd.DataFrame({
        'stage': ['Reached', 'Opened/Viewed', 'Clicked/Engaged', 'Converted'],
        'count': [350000, 185000, 72000, 15400],
        'conversion_rate': [100, 52.9, 20.6, 4.4]
    })
    
    fig = go.Figure(go.Funnel(
        y=funnel_data['stage'],
        x=funnel_data['count'],
        textinfo="value+percent initial",
        marker=dict(color=['#003366', '#004080', '#0066AA', '#FFD700'])
    ))
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Funnel Metrics")
    
    for _, row in funnel_data.iterrows():
        st.metric(
            row['stage'],
            f"{row['count']:,}",
            delta=f"{row['conversion_rate']:.1f}% of total"
        )

# Best performing campaigns
st.markdown("### 🏆 Top Performing Campaigns (Sample Data)")

top_campaigns = pd.DataFrame({
    'Campaign': ['Summer Savings Promo', 'Salary Advance Offer', 'Rewards Program Launch', 
                 'Mobile Banking Update', 'Foreign Currency Account'],
    'Channel': ['Email', 'SMS', 'Push Notification', 'In-App', 'Email'],
    'Sent': [45000, 32000, 28000, 52000, 38000],
    'Engaged': [18900, 14720, 16800, 31200, 15960],
    'Engagement Rate': ['42.0%', '46.0%', '60.0%', '60.0%', '42.0%'],
    'Conversions': [1260, 1840, 1120, 2080, 1140]
})

st.dataframe(
    top_campaigns.style.background_gradient(subset=['Engaged'], cmap='YlGn'),
    use_container_width=True
)

# Download section
st.markdown("---")
st.markdown("### 📥 Export Data")

if st.button("Download Engagement Report (CSV)", key="download_engagement"):
    st.info("Export functionality will be activated when connected to real data sources.")

# Data integration instructions
with st.expander("🔌 Data Integration Guide"):
    st.markdown("""
    ### How to Activate This Dashboard
    
    **Required Data Sources:**
    
    1. **Email Campaign Platform** (e.g., Mailchimp, SendGrid)
       - API credentials or CSV exports
       - Metrics: sent, opened, clicked, bounced, unsubscribed
    
    2. **SMS Platform** (e.g., Twilio, Africa's Talking)
       - API credentials or delivery reports
       - Metrics: sent, delivered, failed, responses
    
    3. **Mobile App Analytics** (e.g., Firebase, Mixpanel)
       - SDK integration or API
       - Metrics: DAU, MAU, sessions, session duration, feature usage
    
    4. **Web Analytics** (e.g., Google Analytics)
       - API credentials
       - Metrics: page views, unique visitors, bounce rate, time on site
    
    5. **Customer Portal Logs**
       - Database access or export
       - Metrics: logins, feature usage, support tickets
    
    **Integration Steps:**
    1. Provide API credentials or data export access
    2. Map data fields to portal schema
    3. Set up automated data sync (daily/hourly)
    4. Validate data quality
    5. Dashboard activates automatically
    
    **Contact:** bi@nmbz.co.zw for integration support
    """)

show_nmb_footer()
