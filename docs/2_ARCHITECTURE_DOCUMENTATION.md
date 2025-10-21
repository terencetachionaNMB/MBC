# Application Architecture Documentation
## NMB Bank Marketing & Brand Communications BI Portal

**Document Version:** 1.0  
**Last Updated:** October 21, 2025  
**Architecture Type:** Multi-tier Web Application with Data Layer  

---

## 1. Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Streamlit  │  │    Plotly   │  │   NMB Branding (CSS)    │ │
│  │  Framework  │  │ Visualize   │  │   Components            │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       APPLICATION LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ Data Loader  │  │   Data       │  │  Metrics           │   │
│  │   Module     │  │  Processor   │  │  Calculator        │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐                           │
│  │ Visualization│  │   Branding   │                           │
│  │   Helper     │  │   Utilities  │                           │
│  └──────────────┘  └──────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │  CSV Files   │  │  PostgreSQL  │  │  Environment       │   │
│  │  (Current)   │  │  (Planned)   │  │  Secrets           │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SYSTEMS                            │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │  Intellect/  │  │  Reference   │  │  Future: Social    │   │
│  │  IDC Core    │  │    Data      │  │  Media APIs        │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    REPLIT CLOUD PLATFORM                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │               Streamlit Application                    │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐ │ │
│  │  │  Main    │  │  Pages   │  │     Utils            │ │ │
│  │  │  App     │  │  (6)     │  │     Modules          │ │ │
│  │  └──────────┘  └──────────┘  └──────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↕                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              PostgreSQL Database (Neon)                │ │
│  │  - User authentication                                 │ │
│  │  - Bookmarks & favorites                              │ │
│  │  - Notifications                                       │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↕                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                File Storage (CSV)                      │ │
│  │  - Account data: 259,881 records                      │ │
│  │  - Customer data, transactions, revenue               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↕
┌─────────────────────────────────────────────────────────────┐
│                       END USERS                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Executives  │  │   Managers   │  │    Analysts      │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Component Architecture

### 2.1 Presentation Layer Components

#### Main Application (app.py)
**Purpose:** Entry point and homepage  
**Responsibilities:**
- Application configuration
- Welcome and overview display
- Quick stats dashboard
- Navigation to sub-dashboards
- Data governance section

**Key Features:**
- NMB logo display
- Professional banner with gradients
- Project acknowledgment section
- Custom footer

#### Dashboard Pages (pages/ directory)
**Multi-page Architecture:** Streamlit's native page routing

**Page Structure:**
1. **1_Executive_Summary.py**
   - KPIs: Total customers, active accounts, avg products
   - Visualizations: Quarterly trends, activity distribution
   - Product analysis charts

2. **2_Active_Email_Accounts.py**
   - Email validation and filtering
   - Searchable account listings
   - Branch and product segmentation

3. **3_Account_Activity.py**
   - 90-day activity threshold (configurable)
   - Active/inactive segmentation
   - Drill-down by branch, product, customer

4. **4_Customer_Metrics.py**
   - Month-over-month churn tracking
   - Customer retention analysis
   - Product holdings distribution

5. **5_Quarterly_Performance.py**
   - Q1-Q3 2025 funded accounts
   - Quarterly growth metrics
   - Branch performance comparison

6. **6_Campaign_Analysis.py**
   - Non-funded income campaign (June-Sept 2025)
   - Revenue attribution by GL account
   - Campaign participant analysis

**Common Page Structure:**
```python
# 1. Imports
import streamlit as st
from utils.data_loader import DataLoader
from utils.branding import apply_nmb_branding, show_nmb_logo, show_nmb_footer

# 2. Page configuration
st.set_page_config(title="...", layout="wide")
apply_nmb_branding()

# 3. Logo and banner
show_nmb_logo()
# Banner HTML

# 4. Data loading (cached)
@st.cache_resource
def load_data():
    return DataLoader()

# 5. Business logic and visualizations
# ...

# 6. Footer
show_nmb_footer()
```

### 2.2 Application Layer Components

#### DataLoader (utils/data_loader.py)
**Purpose:** Centralized data loading and schema management

**Responsibilities:**
- Load CSV files from data/ directory
- Parse dates in multiple formats (vectorized)
- Clean numeric values (remove commas)
- Column mapping for standardization
- Caching for performance

**Key Methods:**
```python
class DataLoader:
    def __init__(self)
    def get_accounts_data() -> pd.DataFrame
    def get_sector_data() -> pd.DataFrame
    def get_gl_data() -> pd.DataFrame
    def get_product_data() -> pd.DataFrame
    def get_product_volume() -> pd.DataFrame
    def get_revenue_data() -> pd.DataFrame
    def get_churn_data() -> pd.DataFrame
```

**Performance Optimizations:**
- Vectorized date parsing (format-specific + fallback)
- Vectorized numeric cleaning
- Single load per session (cached)

#### DataProcessor (utils/data_processor.py)
**Purpose:** Data transformation and preparation for visualizations

**Responsibilities:**
- Account activity segmentation
- Customer aggregations
- Quarterly calculations
- Product analysis
- Filter and search operations

**Key Methods:**
```python
class DataProcessor:
    def get_unique_customer_count() -> int
    def get_avg_products_per_customer() -> float
    def get_account_activity_segments(threshold_days=90)
    def get_quarterly_funded_accounts(year)
    def get_product_distribution()
    def search_accounts(search_term)
```

#### MetricsCalculator (utils/metrics_calculator.py)
**Purpose:** Complex KPI calculations

**Responsibilities:**
- Growth rate calculations
- CAGR (Compound Annual Growth Rate)
- Churn rate computation
- Customer lifetime value
- Campaign ROI metrics

**Key Methods:**
```python
class MetricsCalculator:
    def calculate_growth_rate(current, previous)
    def calculate_cagr(start_value, end_value, periods)
    def calculate_churn_rate(lost_customers, total_customers)
    def calculate_customer_ltv(...)
```

#### VisualizationHelper (utils/visualization.py)
**Purpose:** Standardized Plotly chart creation

**Responsibilities:**
- Consistent NMB brand colors
- Chart templates (line, bar, pie, scatter)
- Hover formatting
- Layout standardization

**Chart Types:**
```python
class VisualizationHelper:
    @staticmethod
    def create_line_chart(data, x, y, title, **kwargs)
    def create_bar_chart(data, x, y, title, **kwargs)
    def create_pie_chart(data, names, values, title, **kwargs)
    def create_scatter_plot(data, x, y, title, **kwargs)
    def create_grouped_bar_chart(...)
```

**Color Scheme:**
- Primary: #003366 (Navy)
- Accent: #FFD700 (Gold)
- Gradients for depth

#### Branding Module (utils/branding.py)
**Purpose:** Consistent NMB visual identity

**Components:**
```python
def apply_nmb_branding()  # CSS injection, hide Streamlit elements
def show_nmb_logo()  # Display logo
def show_nmb_footer()  # Fixed footer with custom message
def show_acknowledgment()  # Project recognition section
def create_professional_banner(title, subtitle, icon)
def create_section_divider(text)
```

---

## 3. Data Architecture

### 3.1 Current Data Storage (CSV-based)

**File Structure:**
```
data/
├── accounts_data.csv                                 # 259,881 records
├── accounts_datadictionary_*.csv                     # Schema definition
├── churn_customers.csv                               # Monthly customer counts
├── product_volume.csv                                # Product holdings
├── revenue_gls.csv                                   # Revenue tracking
├── transactions.csv                                  # Transaction history
├── GL CATEGORY LOOKUP TABLE_*.csv                    # GL mappings
├── PRODUCT TYPE LOOKUP TABLE_*.csv                   # Product definitions
└── RBZ SECTOR CLASSIFICATION LOOKUP TABLE_*.csv      # Sector codes
```

**Data Characteristics:**
- **Volume:** 259,881 account records
- **Customers:** 190,560 unique
- **Format:** CSV (comma-separated)
- **Updates:** Manual file replacement
- **Size:** ~46MB (accounts_data.csv)

### 3.2 Data Model

#### Core Entities

**Account (ACNTS_*):**
```
Account Record:
- ACNTS_BRN_CODE: Branch code
- ACCOUNT_NUMBER: Unique account identifier
- ACNTBAL_CURR_CODE: Currency code
- BASE_CURR_BAL: Balance in base currency
- LOCAL_CURR_BAL: Balance in local currency
- ACNTS_PROD_CODE: Product code (FK)
- PRODUCT_NAME: Product description
- CLIENTS_TYPE_FLG: Client type indicator
- ACNTS_CLIENT_NUM: Customer ID (FK)
- ACCOUNT_NAME: Account holder name
- ACNTS_LAST_TRAN_DATE: Last transaction timestamp
- ACNTS_NONSYS_LAST_DATE: Non-system last date
- ... (93 total fields)
```

**Customer (Derived):**
```
Customer Entity (aggregated from accounts):
- Customer ID (ACNTS_CLIENT_NUM)
- Account Count: Number of accounts
- Product Holdings: Distinct products owned
- Email Address: INDCLIENT_EMAIL_ADDR1
- Phone: CLCONTACT_RES_PHONE
- Birth Date: INDCLIENT_BIRTH_DATE
- Gender: INDCLIENT_SEX
```

**Churn Tracking:**
```
Churn Record:
- TRAN_MONTH: Month number (2-10 for 2025)
- COMMON_CUSTOMERS: Active customer count
```

**Product Volume:**
```
Product Holding:
- Product Code
- Product Type
- Product Name
- Volume Count
```

**Revenue:**
```
Revenue Record:
- GL Account
- Product Association
- Revenue Amount
- Period
```

### 3.3 Future Database Schema (PostgreSQL)

**Planned Tables:**

```sql
-- User Management
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_level INT NOT NULL,  -- 1-5 for RBAC
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Role Definitions
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    role_level INT UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB  -- Dashboard access, export rights, etc.
);

-- User Bookmarks
CREATE TABLE bookmarks (
    bookmark_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    dashboard_name VARCHAR(100),
    filter_config JSONB,  -- Saved filters/parameters
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(200)
);

-- User Favorites
CREATE TABLE favorites (
    favorite_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    favorite_type VARCHAR(50),  -- 'account', 'customer', 'product'
    favorite_id_ref VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    message TEXT NOT NULL,
    notification_type VARCHAR(50),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    link_to_dashboard VARCHAR(200)
);

-- Audit Log
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    action VARCHAR(100),
    dashboard_accessed VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(50)
);
```

---

## 4. Security Architecture

### 4.1 Current State (No Authentication)

**Open Access:**
- No login required
- All dashboards publicly accessible
- No user tracking
- No data export restrictions

**Risks:**
- Unauthorized access to business data
- No audit trail
- No personalization

### 4.2 Planned Security Model (5-Level RBAC)

#### Role Levels

**Level 1: Executive**
- **Access:** All dashboards + admin functions
- **Permissions:** View, Export (CSV/Excel), Create custom views
- **Users:** C-suite, VPs

**Level 2: Manager**
- **Access:** All dashboards except admin
- **Permissions:** View, Limited export (own dashboard data only)
- **Users:** Department heads, senior managers

**Level 3: Analyst**
- **Access:** Operational dashboards only
- **Permissions:** View, No export
- **Users:** Marketing analysts, BI team

**Level 4: Read-Only**
- **Access:** Selected dashboards
- **Permissions:** View only (no drill-down, no export)
- **Users:** Junior staff, contractors

**Level 5: External Stakeholder**
- **Access:** Executive Summary only (limited KPIs)
- **Permissions:** View high-level metrics only
- **Users:** Board members, external consultants

#### Authentication Flow

```
User Request → Login Page → Credentials Validation
                                ↓
                        Check PostgreSQL users table
                                ↓
                        Password hash comparison
                                ↓
                        ┌─────────────┬──────────────┐
                     Valid         Invalid
                        ↓              ↓
              Create session    Return error
                        ↓
              Store role_level in session
                        ↓
              Redirect to appropriate dashboard
                        ↓
              Apply role-based filters
```

#### Session Management

```python
# Streamlit session state
st.session_state['authenticated'] = True
st.session_state['user_id'] = user_id
st.session_state['role_level'] = role_level
st.session_state['username'] = username
st.session_state['permissions'] = load_permissions(role_level)
```

### 4.3 Data Security

**Encryption:**
- Passwords: bcrypt hashing
- Database: TLS connection (Replit/Neon provides)
- Secrets: Environment variables (not in code)

**Access Control:**
```python
def check_access(required_level):
    if not st.session_state.get('authenticated'):
        st.error("Please log in")
        st.stop()
    
    user_level = st.session_state.get('role_level')
    if user_level > required_level:
        st.error("Insufficient permissions")
        st.stop()
```

---

## 5. Integration Architecture

### 5.1 Current Integrations

**Replit Platform:**
- Hosting and deployment
- Environment secrets management
- PostgreSQL database (Neon-backed)
- Git version control

**None (No External APIs currently)**

### 5.2 Planned Integrations

#### Social Media APIs

**Twitter/X API:**
```
Purpose: Analytics for marketing tweets/campaigns
Data Points:
- Tweet impressions, engagement rate
- Follower growth
- Hashtag performance
- Campaign reach

Authentication: OAuth 2.0
Rate Limits: Consider API tier
```

**Facebook Graph API:**
```
Purpose: Page analytics and ad performance
Data Points:
- Post reach and engagement
- Ad campaign metrics
- Audience demographics
- Conversion tracking

Authentication: App token + Page access token
```

#### Sentiment Analysis

**Options:**
1. **Cloud API (Google NLP, AWS Comprehend):**
   - Pros: Accurate, maintained
   - Cons: Cost per API call

2. **Open Source (VADER, TextBlob):**
   - Pros: Free, offline
   - Cons: Less accurate, needs training

**Data Flow:**
```
Customer Feedback → Sentiment API → Score (-1 to +1)
                                          ↓
                            Store in database with metadata
                                          ↓
                            Aggregate for dashboard visualization
```

#### LLM Integration (Planned)

**OpenAI GPT API:**
```
Purpose: AI assistant for natural language queries
Example Queries:
- "What's our churn rate this month?"
- "Show top performing products"
- "Alert me if churn exceeds 2%"

Architecture:
User Query → LLM API → SQL generation → Execute → Format response
```

**Search Integration:**
```python
# Use Replit's search_integrations tool
search_integrations("openai") 
# OR
search_integrations("anthropic claude")
```

---

## 6. Performance Architecture

### 6.1 Caching Strategy

**Resource-Level Caching:**
```python
@st.cache_resource
def load_data():
    """Cached for entire session, shared across users"""
    return DataLoader()
```

**Data-Level Caching:**
```python
@st.cache_data
def calculate_expensive_metric(df):
    """Cached based on input data hash"""
    return complex_calculation(df)
```

**Cache Invalidation:**
- Manual: Clear cache button in UI
- Automatic: TTL-based (configurable)
- Data update: New file upload clears cache

### 6.2 Data Processing Optimization

**Vectorization:**
```python
# SLOW (row-by-row)
df['date'] = df['date'].apply(parse_date)  # ❌

# FAST (vectorized)
df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y', errors='coerce')  # ✅
```

**Lazy Loading:**
- Load only required columns
- Filter early in pipeline
- Aggregate before display

### 6.3 Scalability Considerations

**Current Capacity:**
- 259,881 records: 2-5 second load time
- Estimated max (with vectorization): 1M+ records

**Scaling Strategies:**
1. **Horizontal:** Add more Replit cores
2. **Database:** Move from CSV to PostgreSQL with indexing
3. **CDN:** Cache static assets
4. **Pagination:** Large result sets split across pages

---

## 7. Development Architecture

### 7.1 Development Environment

**Replit IDE:**
- Cloud-based development
- No local setup required
- Integrated terminal and file browser

**Version Control:**
- Git (automatic commits on Replit)
- Branch strategy (planned):
  - `main`: Production-ready code
  - `dev`: Development/testing
  - `feature/*`: Individual features

### 7.2 Deployment Pipeline

**Current (Manual):**
```
Code Change → Save → Auto-restart workflow → Live
```

**Planned (CI/CD):**
```
Code Change → Git Commit → Automated Tests → Build → Deploy
```

### 7.3 Testing Strategy

**Current:**
- Manual testing via UI
- Data validation checks

**Planned:**
- Unit tests for utils/ modules
- Integration tests for dashboards
- E2E tests with Playwright (via run_test tool)
- Data quality tests

---

## 8. Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Frontend** | Streamlit | 1.x | Web UI framework |
| **Visualization** | Plotly | Latest | Interactive charts |
| **Data Processing** | Pandas | 2.x | Data manipulation |
| **Data Processing** | NumPy | 1.x | Numerical operations |
| **Database (Future)** | PostgreSQL | 15+ | Relational data storage |
| **ORM (Future)** | SQLAlchemy | 2.x | Database abstraction |
| **Auth (Future)** | bcrypt | Latest | Password hashing |
| **Deployment** | Replit | N/A | Cloud hosting |
| **Language** | Python | 3.11 | Core programming |

---

## 9. Configuration Management

### 9.1 Environment Variables

**Database:**
```
DATABASE_URL=postgresql://user:pass@host:port/db
PGHOST=hostname
PGPORT=5432
PGUSER=username
PGPASSWORD=password
PGDATABASE=database_name
```

**Application:**
```
SESSION_SECRET=random_secret_key
ENVIRONMENT=production|development
```

### 9.2 Configuration Files

**.streamlit/config.toml:**
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
# NMB colors could be defined here if needed
```

---

## 10. Monitoring and Logging (Planned)

**Application Logs:**
- User login/logout events
- Dashboard access tracking
- Error logging
- Performance metrics

**Database Monitoring:**
- Query performance
- Connection pool status
- Storage usage

**Alerting:**
- System errors → Email/SMS
- Performance degradation → Dashboard notification
- Security events → Admin alert

---

## 11. Disaster Recovery and Backup

**Data Backup:**
- PostgreSQL: Automatic Neon backups
- CSV files: Version controlled in Git
- User data: Daily database snapshots

**Recovery Plan:**
1. Database corruption → Restore from Neon backup
2. Code issues → Rollback Git commit
3. Data loss → Restore from daily snapshot

---

**Document Status:** Living Document - Updated as architecture evolves  
**Next Review:** After authentication implementation  
**Owner:** Terence Tachiona, NMB Business Intelligence  
