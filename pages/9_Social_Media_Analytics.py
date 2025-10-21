import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from utils.branding import apply_nmb_branding, show_nmb_logo, show_nmb_footer, create_professional_banner
import numpy as np

st.set_page_config(page_title="Social Media Analytics", page_icon="📱", layout="wide")
apply_nmb_branding()

show_nmb_logo()

st.markdown(create_professional_banner(
    "Social Media Analytics",
    "Twitter, Facebook, LinkedIn & Instagram Performance Tracking",
    "📱"
), unsafe_allow_html=True)

# Template notice
st.info("""
🔧 **Template Dashboard - Awaiting Social Media Integration**

This dashboard tracks NMB Bank's social media presence across:
- **Twitter/X** (tweets, retweets, likes, followers, engagement rate)
- **Facebook** (posts, reactions, shares, comments, page likes)
- **LinkedIn** (posts, engagement, follower growth, company updates)
- **Instagram** (posts, likes, comments, followers, stories performance)

**To activate:** Provide social media API credentials or connect analytics tools.
""")

# Generate sample social media data
@st.cache_data
def generate_social_media_data():
    """Generate sample social media analytics"""
    
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    # Twitter metrics
    twitter_data = pd.DataFrame({
        'date': dates,
        'tweets': np.random.randint(3, 12, 30),
        'retweets': np.random.randint(20, 150, 30),
        'likes': np.random.randint(50, 300, 30),
        'replies': np.random.randint(5, 50, 30),
        'impressions': np.random.randint(5000, 25000, 30),
        'engagement_rate': np.random.uniform(2.5, 8.5, 30)
    })
    
    # Facebook metrics
    facebook_data = pd.DataFrame({
        'date': dates,
        'posts': np.random.randint(2, 8, 30),
        'reactions': np.random.randint(100, 500, 30),
        'comments': np.random.randint(20, 100, 30),
        'shares': np.random.randint(30, 150, 30),
        'reach': np.random.randint(10000, 50000, 30),
        'engagement_rate': np.random.uniform(3.0, 9.0, 30)
    })
    
    # Top performing posts
    top_posts = pd.DataFrame({
        'platform': ['Twitter', 'Facebook', 'LinkedIn', 'Twitter', 'Instagram'],
        'post_type': ['Promo', 'Update', 'Article', 'Customer Story', 'Visual'],
        'content': [
            'New savings account with 5% interest! Open today...',
            'NMB Mobile App updated with new features...',
            'How digital banking is transforming Zimbabwe...',
            'Meet Sarah, who achieved her dreams with our loan...',
            'Behind the scenes at NMB Head Office...'
        ],
        'engagement': [1250, 980, 720, 1100, 890],
        'reach': [45000, 38000, 22000, 35000, 28000],
        'date': pd.to_datetime(['2025-10-18', '2025-10-19', '2025-10-17', '2025-10-20', '2025-10-19'])
    })
    
    # Follower growth
    follower_growth = pd.DataFrame({
        'platform': ['Twitter', 'Facebook', 'LinkedIn', 'Instagram'],
        'current_followers': [15420, 28750, 12340, 8920],
        'new_followers_30d': [342, 520, 180, 245],
        'growth_rate': [2.3, 1.8, 1.5, 2.8]
    })
    
    # Content performance by type
    content_types = pd.DataFrame({
        'content_type': ['Promotional', 'Educational', 'Customer Stories', 'Product Updates', 'Financial Tips', 'Company News'],
        'posts': [45, 38, 22, 35, 42, 18],
        'avg_engagement': [5.2, 6.8, 8.1, 5.5, 7.2, 4.3],
        'avg_reach': [25000, 18000, 32000, 22000, 28000, 15000]
    })
    
    # Hashtag performance
    hashtags = pd.DataFrame({
        'hashtag': ['#NMBBank', '#DigitalBanking', '#SaveWithNMB', '#MobileApp', '#FinancialFreedom', '#Zimbabwe'],
        'uses': [156, 89, 72, 64, 98, 145],
        'reach': [125000, 78000, 62000, 55000, 85000, 230000],
        'engagement': [2850, 1920, 1540, 1280, 2100, 4250]
    })
    
    return twitter_data, facebook_data, top_posts, follower_growth, content_types, hashtags

twitter_data, facebook_data, top_posts, follower_growth, content_types, hashtags = generate_social_media_data()

# Key Metrics
st.markdown("### 📊 Social Media Overview (Last 30 Days)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_followers = follower_growth['current_followers'].sum()
    new_followers = follower_growth['new_followers_30d'].sum()
    st.metric(
        "Total Followers",
        f"{total_followers:,}",
        delta=f"+{new_followers}",
        help="Combined followers across all platforms"
    )

with col2:
    total_engagement = twitter_data['likes'].sum() + twitter_data['retweets'].sum() + facebook_data['reactions'].sum()
    st.metric(
        "Total Engagement",
        f"{total_engagement:,}",
        delta="↑ 15.2%",
        help="Likes, reactions, shares, retweets combined"
    )

with col3:
    avg_engagement_rate = (twitter_data['engagement_rate'].mean() + facebook_data['engagement_rate'].mean()) / 2
    st.metric(
        "Avg Engagement Rate",
        f"{avg_engagement_rate:.1f}%",
        delta="↑ 0.8%",
        help="Average engagement rate across platforms"
    )

with col4:
    total_posts = twitter_data['tweets'].sum() + facebook_data['posts'].sum()
    st.metric(
        "Total Posts",
        f"{total_posts}",
        delta="Same as last month",
        help="Total posts published across all platforms"
    )

st.markdown("---")

# Platform performance
st.markdown("### 📈 Platform Performance")

tab1, tab2, tab3 = st.tabs(["Twitter", "Facebook", "All Platforms"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Twitter Engagement Trend")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=twitter_data['date'],
            y=twitter_data['likes'],
            name='Likes',
            fill='tonexty',
            line=dict(color='#1DA1F2', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=twitter_data['date'],
            y=twitter_data['retweets'],
            name='Retweets',
            fill='tonexty',
            line=dict(color='#FFD700', width=2)
        ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Count",
            hovermode='x unified',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Twitter Metrics")
        
        metrics = pd.DataFrame({
            'Metric': ['Total Tweets', 'Total Retweets', 'Total Likes', 'Avg Engagement Rate'],
            'Value': [
                f"{twitter_data['tweets'].sum()}",
                f"{twitter_data['retweets'].sum():,}",
                f"{twitter_data['likes'].sum():,}",
                f"{twitter_data['engagement_rate'].mean():.1f}%"
            ]
        })
        
        st.dataframe(metrics, use_container_width=True, hide_index=True)
        
        st.metric("Current Followers", "15,420", delta="+342")

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Facebook Engagement Trend")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=facebook_data['date'],
            y=facebook_data['reactions'],
            name='Reactions',
            fill='tonexty',
            line=dict(color='#1877F2', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=facebook_data['date'],
            y=facebook_data['shares'],
            name='Shares',
            fill='tonexty',
            line=dict(color='#FFD700', width=2)
        ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Count",
            hovermode='x unified',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Facebook Metrics")
        
        metrics = pd.DataFrame({
            'Metric': ['Total Posts', 'Total Reactions', 'Total Shares', 'Avg Engagement Rate'],
            'Value': [
                f"{facebook_data['posts'].sum()}",
                f"{facebook_data['reactions'].sum():,}",
                f"{facebook_data['shares'].sum():,}",
                f"{facebook_data['engagement_rate'].mean():.1f}%"
            ]
        })
        
        st.dataframe(metrics, use_container_width=True, hide_index=True)
        
        st.metric("Page Likes", "28,750", delta="+520")

with tab3:
    st.markdown("#### Follower Growth by Platform")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current Followers',
        x=follower_growth['platform'],
        y=follower_growth['current_followers'],
        text=follower_growth['current_followers'],
        textposition='auto',
        marker_color='#003366'
    ))
    
    fig.add_trace(go.Bar(
        name='New Followers (30d)',
        x=follower_growth['platform'],
        y=follower_growth['new_followers_30d'],
        text=follower_growth['new_followers_30d'],
        textposition='auto',
        marker_color='#FFD700'
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title="Platform",
        yaxis_title="Followers",
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Top performing content
st.markdown("### 🏆 Top Performing Posts")

for _, post in top_posts.iterrows():
    platform_color = {
        'Twitter': '#1DA1F2',
        'Facebook': '#1877F2',
        'LinkedIn': '#0A66C2',
        'Instagram': '#E4405F'
    }.get(post['platform'], '#003366')
    
    st.markdown(f"""
    <div style="border-left: 4px solid {platform_color}; padding: 1rem; margin: 0.5rem 0; background: #f8f9fa; border-radius: 4px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span><strong>{post['platform']}</strong> • {post['post_type']}</span>
            <span style="font-size: 0.85rem; color: #666;">{post['date'].strftime('%b %d, %Y')}</span>
        </div>
        <div style="margin: 0.5rem 0;">{post['content']}</div>
        <div style="display: flex; gap: 2rem; font-size: 0.9rem; color: #666;">
            <span>💬 Engagement: {post['engagement']:,}</span>
            <span>👥 Reach: {post['reach']:,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Content analysis
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Content Performance by Type")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=content_types['content_type'],
        y=content_types['avg_engagement'],
        marker=dict(
            color=content_types['avg_engagement'],
            colorscale='Viridis',
            showscale=False
        ),
        text=content_types['avg_engagement'].apply(lambda x: f"{x:.1f}%"),
        textposition='auto'
    ))
    
    fig.update_layout(
        xaxis_title="Content Type",
        yaxis_title="Avg Engagement Rate (%)",
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### #️⃣ Top Performing Hashtags")
    
    hashtags_sorted = hashtags.sort_values('engagement', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=hashtags_sorted['engagement'],
        y=hashtags_sorted['hashtag'],
        orientation='h',
        marker_color='#003366',
        text=hashtags_sorted['engagement'],
        textposition='auto'
    ))
    
    fig.update_layout(
        xaxis_title="Total Engagement",
        yaxis_title="Hashtag",
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Best posting times (sample data)
st.markdown("### ⏰ Best Posting Times")

st.info("""
**Optimal Posting Schedule (Based on Engagement Data):**

- **Twitter:** Mon-Fri 9:00-11:00 AM, 1:00-3:00 PM
- **Facebook:** Tue-Thu 10:00 AM-2:00 PM, 6:00-8:00 PM
- **LinkedIn:** Tue-Thu 8:00-10:00 AM, 12:00-1:00 PM
- **Instagram:** Daily 6:00-9:00 PM, weekends 10:00 AM-12:00 PM

*Note: Times in Central Africa Time (CAT)*
""")

# Competitor benchmarking
st.markdown("### 🎯 Competitor Benchmarking (Sample)")

competitor_data = pd.DataFrame({
    'Bank': ['NMB Bank', 'Competitor A', 'Competitor B', 'Competitor C'],
    'Twitter Followers': [15420, 18750, 12300, 9800],
    'Facebook Likes': [28750, 35200, 22100, 18900],
    'Engagement Rate': ['5.8%', '4.2%', '6.1%', '3.8%'],
    'Posts/Week': [12, 18, 10, 8]
})

st.dataframe(
    competitor_data.style.highlight_max(subset=['Twitter Followers', 'Facebook Likes'], color='#90EE90'),
    use_container_width=True,
    hide_index=True
)

# Export
st.markdown("---")
if st.button("Download Social Media Report", key="download_social"):
    st.info("Export functionality will be activated when connected to social media APIs.")

# Integration guide
with st.expander("🔌 Social Media Integration Guide"):
    st.markdown("""
    ### Connect Your Social Media Accounts
    
    **Required API Access:**
    
    1. **Twitter/X API**
       - Developer account required
       - API keys: Consumer Key, Consumer Secret, Access Token, Access Token Secret
       - Metrics: Tweets, retweets, likes, replies, impressions
       - Rate limits: 900 requests/15 minutes
    
    2. **Facebook Graph API**
       - Facebook Business Manager access
       - Page Access Token
       - Metrics: Posts, reactions, comments, shares, reach, page likes
       - Permissions: pages_read_engagement, read_insights
    
    3. **LinkedIn API**
       - LinkedIn Developer app
       - OAuth 2.0 credentials
       - Metrics: Posts, engagement, follower count, impressions
    
    4. **Instagram Business API**
       - Instagram Business or Creator account
       - Connected to Facebook Page
       - Metrics: Posts, likes, comments, followers, stories
    
    **Alternative Integration:**
    - **Hootsuite/Buffer Export:** CSV export from social media management tools
    - **Manual Upload:** Monthly performance reports
    
    **Setup Steps:**
    1. Obtain API credentials for each platform
    2. Provide credentials to BI team
    3. Configure data sync schedule (hourly/daily)
    4. Validate data accuracy
    5. Dashboard activates automatically
    
    **Contact:** bi@nmbz.co.zw for social media integration
    """)

show_nmb_footer()
