import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from utils.branding import apply_nmb_branding, show_nmb_logo, show_nmb_footer, create_professional_banner
import numpy as np

st.set_page_config(page_title="Sentiment Analysis", page_icon="💬", layout="wide")
apply_nmb_branding()

show_nmb_logo()

st.markdown(create_professional_banner(
    "Sentiment Analysis Dashboard",
    "Customer Feedback & Brand Perception Analytics",
    "💬"
), unsafe_allow_html=True)

# Template data notice
st.info("""
🔧 **Template Dashboard - Awaiting Sentiment Data**

This dashboard analyzes customer sentiment from:
- **Customer surveys** (NPS, CSAT, feedback forms)
- **Social media mentions** (Twitter, Facebook comments)
- **Customer service interactions** (chat transcripts, call center notes)
- **Product reviews** (app store reviews, website feedback)
- **Email responses** (campaign replies, support emails)

**To activate:** Provide sentiment data sources or API access to sentiment analysis tools.
""")

# Generate sample sentiment data
@st.cache_data
def generate_sample_sentiment_data():
    """Generate sample sentiment analysis data"""
    
    # Daily sentiment trends (last 90 days)
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    
    sentiment_trends = pd.DataFrame({
        'date': dates,
        'positive': np.random.randint(300, 800, 90),
        'neutral': np.random.randint(200, 500, 90),
        'negative': np.random.randint(50, 200, 90),
        'sentiment_score': np.random.uniform(0.6, 0.85, 90)  # -1 to 1 scale
    })
    
    # Calculate total mentions
    sentiment_trends['total_mentions'] = (
        sentiment_trends['positive'] + 
        sentiment_trends['neutral'] + 
        sentiment_trends['negative']
    )
    
    # Sentiment by source
    sentiment_by_source = pd.DataFrame({
        'source': ['Social Media', 'Customer Surveys', 'App Reviews', 'Call Center', 'Email Feedback'],
        'positive': [2450, 1850, 980, 1240, 620],
        'neutral': [1200, 980, 450, 780, 320],
        'negative': [480, 220, 180, 360, 120],
        'avg_sentiment': [0.68, 0.78, 0.65, 0.58, 0.71]
    })
    
    # Topic analysis
    topics = pd.DataFrame({
        'topic': ['Customer Service', 'Mobile App', 'Interest Rates', 'Branch Experience', 
                  'Online Banking', 'Card Services', 'Loan Process', 'ATM Network'],
        'mentions': [1250, 980, 1450, 720, 1100, 650, 890, 420],
        'sentiment_score': [0.72, 0.81, 0.45, 0.68, 0.75, 0.70, 0.52, 0.65],
        'trend': ['↑', '↑', '↓', '→', '↑', '→', '↑', '→']
    })
    
    # NPS data
    nps_data = pd.DataFrame({
        'month': ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
        'promoters': [65, 68, 70, 72, 74, 76],
        'passives': [25, 24, 22, 21, 20, 18],
        'detractors': [10, 8, 8, 7, 6, 6],
        'nps_score': [55, 60, 62, 65, 68, 70]
    })
    
    # Sample customer feedback
    sample_feedback = pd.DataFrame({
        'date': pd.to_datetime(['2025-10-20', '2025-10-20', '2025-10-19', '2025-10-19', '2025-10-18']),
        'source': ['App Review', 'Social Media', 'Survey', 'Call Center', 'Email'],
        'sentiment': ['Positive', 'Negative', 'Positive', 'Neutral', 'Positive'],
        'topic': ['Mobile App', 'Interest Rates', 'Customer Service', 'Branch Experience', 'Online Banking'],
        'feedback': [
            'Love the new mobile app update! Much faster and easier to use.',
            'Disappointed with the new interest rates. Expected better from NMB.',
            'Excellent service at Harare branch. Staff very helpful and professional.',
            'Waited 30 minutes for a simple transaction. Could be faster.',
            'Online banking works great. Very convenient for international transfers.'
        ],
        'score': [0.92, -0.65, 0.88, 0.15, 0.85]
    })
    
    return sentiment_trends, sentiment_by_source, topics, nps_data, sample_feedback

sentiment_trends, sentiment_by_source, topics, nps_data, sample_feedback = generate_sample_sentiment_data()

# Key Metrics
st.markdown("### 📊 Sentiment Overview (Last 30 Days)")

col1, col2, col3, col4 = st.columns(4)

recent_sentiment = sentiment_trends.tail(30)

with col1:
    avg_score = recent_sentiment['sentiment_score'].mean()
    sentiment_label = "Positive" if avg_score > 0.6 else "Neutral" if avg_score > 0.4 else "Negative"
    st.metric(
        "Overall Sentiment",
        sentiment_label,
        delta=f"{avg_score:.2f}",
        help="Average sentiment score: -1 (very negative) to +1 (very positive)"
    )

with col2:
    total_mentions = recent_sentiment['total_mentions'].sum()
    st.metric(
        "Total Mentions",
        f"{total_mentions:,}",
        delta="↑ 12.3%",
        help="Total customer feedback mentions across all channels"
    )

with col3:
    positive_pct = (recent_sentiment['positive'].sum() / total_mentions * 100)
    st.metric(
        "Positive Feedback",
        f"{positive_pct:.1f}%",
        delta="↑ 3.2%",
        help="Percentage of positive mentions"
    )

with col4:
    current_nps = nps_data['nps_score'].iloc[-1]
    st.metric(
        "Net Promoter Score",
        f"{current_nps}",
        delta="+2",
        help="NPS Score: Promoters % - Detractors %"
    )

st.markdown("---")

# Sentiment trends
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Sentiment Trends (90 Days)")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sentiment_trends['date'],
        y=sentiment_trends['positive'],
        name='Positive',
        fill='tonexty',
        line=dict(color='#00AA00', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=sentiment_trends['date'],
        y=sentiment_trends['neutral'],
        name='Neutral',
        fill='tonexty',
        line=dict(color='#FFD700', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=sentiment_trends['date'],
        y=sentiment_trends['negative'],
        name='Negative',
        fill='tonexty',
        line=dict(color='#FF4444', width=2)
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Mentions",
        hovermode='x unified',
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📊 Sentiment Distribution by Source")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Positive',
        x=sentiment_by_source['source'],
        y=sentiment_by_source['positive'],
        marker_color='#00AA00'
    ))
    
    fig.add_trace(go.Bar(
        name='Neutral',
        x=sentiment_by_source['source'],
        y=sentiment_by_source['neutral'],
        marker_color='#FFD700'
    ))
    
    fig.add_trace(go.Bar(
        name='Negative',
        x=sentiment_by_source['source'],
        y=sentiment_by_source['negative'],
        marker_color='#FF4444'
    ))
    
    fig.update_layout(
        barmode='stack',
        xaxis_title="Source",
        yaxis_title="Mentions",
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Topic analysis
st.markdown("### 🎯 Sentiment by Topic")

col1, col2 = st.columns([2, 1])

with col1:
    # Sort by sentiment score
    topics_sorted = topics.sort_values('sentiment_score', ascending=True)
    
    fig = go.Figure(go.Bar(
        x=topics_sorted['sentiment_score'],
        y=topics_sorted['topic'],
        orientation='h',
        marker=dict(
            color=topics_sorted['sentiment_score'],
            colorscale=[[0, '#FF4444'], [0.5, '#FFD700'], [1, '#00AA00']],
            showscale=True,
            colorbar=dict(title="Sentiment")
        ),
        text=topics_sorted['sentiment_score'].apply(lambda x: f"{x:.2f}"),
        textposition='auto'
    ))
    
    fig.update_layout(
        xaxis_title="Sentiment Score",
        yaxis_title="Topic",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Topic Details")
    
    topics_display = topics.copy()
    topics_display['sentiment_score'] = topics_display['sentiment_score'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(
        topics_display[['topic', 'mentions', 'sentiment_score', 'trend']],
        use_container_width=True,
        height=400
    )

# NPS Tracking
st.markdown("### 📊 Net Promoter Score (NPS) Trend")

col1, col2 = st.columns([2, 1])

with col1:
    fig = go.Figure()
    
    # Stacked area for promoters, passives, detractors
    fig.add_trace(go.Bar(
        name='Promoters',
        x=nps_data['month'],
        y=nps_data['promoters'],
        marker_color='#00AA00'
    ))
    
    fig.add_trace(go.Bar(
        name='Passives',
        x=nps_data['month'],
        y=nps_data['passives'],
        marker_color='#FFD700'
    ))
    
    fig.add_trace(go.Bar(
        name='Detractors',
        x=nps_data['month'],
        y=nps_data['detractors'],
        marker_color='#FF4444'
    ))
    
    # Add NPS score line
    fig.add_trace(go.Scatter(
        name='NPS Score',
        x=nps_data['month'],
        y=nps_data['nps_score'],
        yaxis='y2',
        line=dict(color='#003366', width=3),
        mode='lines+markers+text',
        text=nps_data['nps_score'],
        textposition='top center'
    ))
    
    fig.update_layout(
        barmode='stack',
        xaxis_title="Month",
        yaxis=dict(title="Respondents (%)"),
        yaxis2=dict(title="NPS Score", overlaying='y', side='right', range=[0, 100]),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### NPS Interpretation")
    
    current_nps = nps_data['nps_score'].iloc[-1]
    
    if current_nps >= 70:
        nps_rating = "Excellent"
        nps_color = "#00AA00"
        nps_desc = "World-class customer loyalty"
    elif current_nps >= 50:
        nps_rating = "Great"
        nps_color = "#88CC00"
        nps_desc = "Strong customer loyalty"
    elif current_nps >= 30:
        nps_rating = "Good"
        nps_color = "#FFD700"
        nps_desc = "Positive customer sentiment"
    elif current_nps >= 0:
        nps_rating = "Needs Improvement"
        nps_color = "#FF8800"
        nps_desc = "Room for growth"
    else:
        nps_rating = "Critical"
        nps_color = "#FF4444"
        nps_desc = "Urgent action required"
    
    st.markdown(f"""
    <div style="background: {nps_color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
        <h2 style="margin: 0;">{current_nps}</h2>
        <h4 style="margin: 0.5rem 0;">{nps_rating}</h4>
        <p style="margin: 0; font-size: 0.9rem;">{nps_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Breakdown")
    st.metric("Promoters (9-10)", f"{nps_data['promoters'].iloc[-1]}%")
    st.metric("Passives (7-8)", f"{nps_data['passives'].iloc[-1]}%")
    st.metric("Detractors (0-6)", f"{nps_data['detractors'].iloc[-1]}%")

# Recent feedback
st.markdown("### 💬 Recent Customer Feedback")

for _, row in sample_feedback.iterrows():
    sentiment_color = '#00AA00' if row['sentiment'] == 'Positive' else '#FF4444' if row['sentiment'] == 'Negative' else '#FFD700'
    
    st.markdown(f"""
    <div style="border-left: 4px solid {sentiment_color}; padding: 1rem; margin: 0.5rem 0; background: #f8f9fa; border-radius: 4px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span><strong>{row['source']}</strong> • {row['topic']}</span>
            <span style="color: {sentiment_color}; font-weight: bold;">{row['sentiment']} ({row['score']:.2f})</span>
        </div>
        <div style="font-style: italic;">"{row['feedback']}"</div>
        <div style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">{row['date'].strftime('%B %d, %Y')}</div>
    </div>
    """, unsafe_allow_html=True)

# Action items based on sentiment
st.markdown("### 🎯 Recommended Actions")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🔴 Priority Issues (Negative Sentiment)
    
    1. **Interest Rates** (Score: 0.45, Trending Down)
       - Action: Review competitive positioning
       - Action: Improve rate communication strategy
    
    2. **Loan Process** (Score: 0.52)
       - Action: Streamline approval workflow
       - Action: Enhance transparency in requirements
    
    3. **Branch Wait Times** (Mentioned in feedback)
       - Action: Optimize staffing during peak hours
       - Action: Implement queue management system
    """)

with col2:
    st.markdown("""
    #### 🟢 Winning Strategies (Positive Sentiment)
    
    1. **Mobile App** (Score: 0.81, Trending Up)
       - Strategy: Promote app features more widely
       - Strategy: Continue regular updates
    
    2. **Customer Service** (Score: 0.78)
       - Strategy: Share best practices across branches
       - Strategy: Staff recognition program
    
    3. **Online Banking** (Score: 0.75)
       - Strategy: Expand feature set
       - Strategy: Market convenience benefits
    """)

# Export
st.markdown("---")
if st.button("Download Sentiment Analysis Report", key="download_sentiment"):
    st.info("Export functionality will be activated when connected to real sentiment data sources.")

# Data source integration guide
with st.expander("🔌 Sentiment Data Integration Guide"):
    st.markdown("""
    ### Activate Sentiment Analysis
    
    **Option 1: Use Sentiment Analysis API**
    - Google Cloud Natural Language API
    - AWS Comprehend
    - Azure Text Analytics
    - MonkeyLearn
    
    **Option 2: Collect Structured Feedback**
    - Customer surveys (NPS, CSAT)
    - App store reviews (iOS, Android)
    - Social media mentions (Twitter API, Facebook Graph API)
    - Support ticket analysis
    
    **Option 3: Analyze Existing Text Data**
    - Email responses
    - Chat transcripts
    - Call center notes
    - Product reviews
    
    **Integration Steps:**
    1. Choose sentiment data source(s)
    2. Provide API credentials or data exports
    3. Configure sentiment scoring scale
    4. Set up automated data collection
    5. Validate sentiment accuracy
    6. Dashboard updates automatically
    
    **Contact:** bi@nmbz.co.zw for sentiment analysis setup
    """)

show_nmb_footer()
