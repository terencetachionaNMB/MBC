# Technical Specifications Document
## NMB Bank Marketing & Brand Communications BI Portal

**Document Version:** 1.0  
**Last Updated:** October 21, 2025  
**Classification:** Technical Reference  

---

## 1. System Overview

### 1.1 Product Information

**Product Name:** Marketing & Brand Communications BI Portal  
**Product Version:** 1.0 (Production)  
**Platform:** Web-based (Streamlit Python Application)  
**Deployment:** Replit Cloud Platform  
**Target Users:** NMB Bank MBC Department (Executives, Managers, Analysts)  

### 1.2 System Purpose

Provide interactive business intelligence dashboards for:
- Customer account analysis (259,881 records)
- Marketing campaign performance tracking
- Customer churn and retention metrics
- Quarterly funded accounts monitoring
- Product holdings and distribution analysis

---

## 2. System Requirements

### 2.1 Functional Requirements

#### FR-001: Data Loading and Processing
**Description:** System shall load and process banking data from CSV files  
**Priority:** High  
**Requirements:**
- Load 259,881+ account records within 5 seconds
- Support multiple date formats (ISO, US, UK, month names)
- Handle numeric values with comma separators
- Validate data integrity on load
- Cache processed data for performance

**Acceptance Criteria:**
- ✅ Data loads in < 5 seconds
- ✅ All date formats parsed correctly
- ✅ Numeric values cleaned and converted
- ✅ Missing data handled gracefully

#### FR-002: Executive Summary Dashboard
**Description:** Display high-level KPIs for executive viewing  
**Priority:** High  
**Requirements:**
- Show total customers (190,560)
- Show active accounts (99.5% in 90-day window)
- Calculate avg products per customer (excl. Account/Card)
- Display quarterly performance trend
- Visualize active vs inactive distribution

**Acceptance Criteria:**
- ✅ All KPIs display accurately
- ✅ Charts render within 2 seconds
- ✅ Interactive drill-down functional
- ✅ Export to CSV available

#### FR-003: Active Email Accounts Dashboard
**Description:** List and filter accounts with valid email addresses  
**Priority:** Medium  
**Requirements:**
- Identify valid vs placeholder emails
- Enable search by account number, name, email
- Filter by branch and product
- Display 68,118 valid contactable customers
- Export filtered results

**Acceptance Criteria:**
- ✅ Email validation logic correct
- ✅ Search returns relevant results
- ✅ Filters apply correctly
- ✅ Export matches filtered view

#### FR-004: Account Activity Dashboard
**Description:** Segment accounts by 90-day activity threshold  
**Priority:** High  
**Requirements:**
- Configurable activity threshold (default 90 days)
- Active/inactive segmentation
- Branch-level breakdown
- Product-level breakdown
- Individual account detail view

**Acceptance Criteria:**
- ✅ Activity calculation correct
- ✅ Threshold adjustable via slider
- ✅ Drill-down to account level
- ✅ Transaction dates visible

#### FR-005: Customer Metrics Dashboard
**Description:** Track customer churn and product holdings  
**Priority:** High  
**Requirements:**
- Month-over-month churn tracking (Feb-Oct 2025)
- Calculate churn rates (non-negative)
- Display customer retention trends
- Show product holdings distribution
- Identify top product combinations

**Acceptance Criteria:**
- ✅ Churn based on actual customer count (190,560)
- ✅ Monthly variations realistic (0.2-1.8%)
- ✅ Negative growth shown as 0% churn
- ✅ Product exclusions applied (Account/Card types)

#### FR-006: Quarterly Performance Dashboard
**Description:** Track funded accounts Q1-Q3 2025  
**Priority:** High  
**Requirements:**
- Display quarterly funded account counts
- Calculate quarter-over-quarter growth
- Show branch-level performance
- Product contribution analysis
- Handle missing ACNTS_OPENING_DATE gracefully

**Acceptance Criteria:**
- ✅ Uses ACNTS_LAST_TRAN_DATE for funded logic
- ✅ Quarterly aggregations correct
- ✅ Growth percentages calculated accurately
- ✅ Branch comparison chart renders

#### FR-007: Campaign Analysis Dashboard
**Description:** Analyze non-funded income campaign (June-Sept 2025)  
**Priority:** Medium  
**Requirements:**
- Identify campaign participants
- Link GL revenue to accounts
- Show campaign metrics over time
- Branch and product attribution
- Calculate campaign ROI indicators

**Acceptance Criteria:**
- ✅ Campaign period filtering correct
- ✅ Revenue attribution logic accurate
- ✅ Participant count matches data
- ✅ Timeline visualization functional

### 2.2 Non-Functional Requirements

#### NFR-001: Performance
**Description:** System shall respond quickly under load  
**Specifications:**
- Page load time: < 5 seconds (initial)
- Chart rendering: < 2 seconds
- Data refresh: < 3 seconds
- Support: 10+ concurrent users (current), 100+ (future)

**Implementation:**
- Vectorized data operations (Pandas)
- @st.cache_resource for data loader
- @st.cache_data for expensive calculations
- Lazy loading of visualizations

#### NFR-002: Usability
**Description:** System shall be intuitive for non-technical users  
**Specifications:**
- No training required for basic navigation
- Clear labeling and tooltips
- Professional NMB branding throughout
- Responsive layout (desktop-optimized)
- Help text and documentation accessible

**Implementation:**
- Streamlit's built-in UI components
- Hover help on metrics
- Consistent navigation sidebar
- Visual hierarchy with colors and spacing

#### NFR-003: Reliability
**Description:** System shall be available and stable  
**Specifications:**
- Uptime: 99.5% (Replit platform SLA)
- Error handling: Graceful degradation
- Data validation: On every load
- Crash recovery: Auto-restart (Replit workflow)

**Implementation:**
- Try-catch blocks around data loading
- Null checks before operations
- Error messages to users
- Auto-restart on crash

#### NFR-004: Scalability
**Description:** System shall handle data growth  
**Specifications:**
- Current: 259,881 records
- Target: 500,000 records within 10 seconds
- Future: 1M+ records (with database migration)

**Implementation:**
- Vectorized operations (not loops)
- Database indexing (when migrated)
- Pagination for large result sets
- Incremental loading strategies

#### NFR-005: Security (Planned)
**Description:** System shall protect sensitive data  
**Specifications:**
- Authentication: Username/password + bcrypt
- Authorization: 5-level RBAC
- Session: Secure token-based
- Data: Encrypted at rest (PostgreSQL)
- Audit: Log all user actions

**Implementation:**
- PostgreSQL user table with password hashes
- Session state for authentication
- Role-based dashboard filtering
- Audit log table

#### NFR-006: Maintainability
**Description:** Code shall be maintainable and documented  
**Specifications:**
- Code comments: All complex functions
- Docstrings: All modules and classes
- Separation of concerns: Utils vs pages
- Version control: Git with meaningful commits
- Documentation: Comprehensive (this doc + others)

**Implementation:**
- Modular architecture (utils/ directory)
- Clear naming conventions
- Type hints where applicable
- README and docs/ folder

---

## 3. Technical Specifications

### 3.1 Programming Languages

**Primary Language:**
- **Python 3.11**
  - Used for: All application logic, data processing, visualization
  - Justification: Streamlit framework requirement, excellent data libraries

**Markup/Styling:**
- **HTML/CSS** (embedded in Python)
  - Used for: Custom branding, professional styling
  - Justification: Streamlit supports markdown and HTML injection

### 3.2 Frameworks and Libraries

| Library | Version | Purpose | Criticality |
|---------|---------|---------|-------------|
| streamlit | 1.x | Web application framework | Critical |
| pandas | 2.x | Data manipulation and analysis | Critical |
| numpy | 1.x | Numerical operations | High |
| plotly | 5.x | Interactive visualizations | High |
| openpyxl | 3.x | Excel export support | Medium |
| sqlalchemy | 2.x | Database ORM (future) | Medium |
| bcrypt | 4.x | Password hashing (future) | Medium |
| pathlib | stdlib | File path handling | Low |
| glob | stdlib | File pattern matching | Low |
| datetime | stdlib | Date/time operations | High |

**Installation:**
```bash
# Current dependencies
pip install streamlit pandas numpy plotly openpyxl

# Future dependencies
pip install sqlalchemy bcrypt psycopg2-binary
```

### 3.3 Database Specifications

#### Current: CSV Files

**Storage Format:**
- File type: Comma-separated values (.csv)
- Encoding: UTF-8
- Line endings: LF (Unix-style)
- Delimiter: Comma (,)
- Quote character: Double quote (")

**File Specifications:**

| File | Records | Size | Columns | Update Frequency |
|------|---------|------|---------|------------------|
| accounts_data.csv | 259,881 | 46MB | 17 | Daily |
| churn_customers.csv | 9 | <1KB | 2 | Monthly |
| product_volume.csv | 98 | 6KB | 3 | Weekly |
| revenue_gls.csv | ~400 | 21KB | 4+ | Daily |
| transactions.csv | ~100K | 5.2MB | 8+ | Daily |

#### Future: PostgreSQL Database

**Database Server:**
- **Provider:** Replit (Neon-backed PostgreSQL)
- **Version:** PostgreSQL 15+
- **Connection:** DATABASE_URL environment variable
- **SSL:** Required (TLS 1.2+)
- **Max Connections:** 100 (Neon default)

**Schema Design:**
```sql
-- See Architecture Documentation Section 3.3 for full schema
-- Key tables:
-- - users (authentication)
-- - roles (RBAC)
-- - bookmarks (user preferences)
-- - favorites (saved items)
-- - notifications (user alerts)
-- - audit_log (access tracking)
```

**Indexing Strategy:**
```sql
-- Performance indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_bookmarks_user_id ON bookmarks(user_id);
CREATE INDEX idx_audit_log_user_timestamp ON audit_log(user_id, timestamp DESC);
```

### 3.4 Data Processing Specifications

#### Date Parsing

**Supported Formats:**
```python
formats = [
    '%B %d, %Y',   # October 17, 2025 (primary format)
    '%Y-%m-%d',    # 2025-10-17 (ISO 8601)
    '%d/%m/%Y',    # 17/10/2025 (UK format)
    '%m/%d/%Y',    # 10/17/2025 (US format)
    '%d-%m-%Y',    # 17-10-2025
    '%Y/%m/%d'     # 2025/10/17
]
```

**Parsing Algorithm:**
1. Try primary format ('%B %d, %Y') with `pd.to_datetime(format=..., errors='coerce')`
2. For NaT (Not-a-Time) results, fallback to general `pd.to_datetime(errors='coerce')`
3. Invalid dates become `pd.NaT`

**Performance:**
- Vectorized parsing: 10-50x faster than row-by-row
- 259,881 dates parsed in ~0.5 seconds

#### Numeric Cleaning

**Input Format:** Strings with commas (e.g., "8,148.51")  
**Output Format:** Float (e.g., 8148.51)

**Algorithm:**
```python
# Vectorized approach
df['balance'] = df['balance'].str.replace(',', '')
df['balance'] = pd.to_numeric(df['balance'], errors='coerce')
```

**Performance:** ~100x faster than `.apply(lambda x: ...)` approach

#### Activity Segmentation

**90-Day Threshold Logic:**
```python
from datetime import datetime, timedelta

cutoff_date = datetime.now() - timedelta(days=90)
active = df[df['ACNTS_LAST_TRAN_DATE'] >= cutoff_date]
inactive = df[df['ACNTS_LAST_TRAN_DATE'] < cutoff_date]
```

**Configurability:** Slider in UI adjusts threshold (30-180 days)

#### Churn Calculation

**Month-over-Month Logic:**
```python
for i in range(1, len(churn_df)):
    prev_customers = churn_df.iloc[i-1]['COMMON_CUSTOMERS']
    curr_customers = churn_df.iloc[i]['COMMON_CUSTOMERS']
    
    change = curr_customers - prev_customers
    
    if change < 0:
        churn_rate = abs(change / prev_customers * 100)
    else:
        churn_rate = 0.0  # Growth = no churn
```

**Key Rule:** Churn is non-negative (customer growth shows 0% churn)

### 3.5 Visualization Specifications

#### Plotly Chart Configuration

**Color Scheme:**
```python
PRIMARY_COLOR = '#003366'  # NMB Navy
ACCENT_COLOR = '#FFD700'   # NMB Gold
SECONDARY_COLORS = ['#004080', '#005599', '#0066AA']
```

**Chart Template:**
```python
fig.update_layout(
    font=dict(family="Arial, sans-serif", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='closest',
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02)
)
```

**Chart Types:**

1. **Line Chart** (Quarterly trends):
   - X-axis: Time periods
   - Y-axis: Metric values
   - Markers: Visible on data points
   - Hover: Show exact values

2. **Bar Chart** (Product distribution):
   - Orientation: Vertical or horizontal
   - Color: NMB Navy
   - Hover: Product name + count

3. **Pie Chart** (Active/Inactive distribution):
   - Colors: Navy (active), Light blue (inactive)
   - Labels: Percentage + count
   - Hole: 0.3 (donut chart)

4. **Grouped Bar** (Branch comparison):
   - Groups: Branches
   - Bars: Metrics (active, inactive)
   - Colors: Navy and Gold

### 3.6 Caching Specifications

**Resource-Level Cache:**
```python
@st.cache_resource
def load_data():
    """
    Cached for entire application lifecycle
    Shared across all users
    Cleared on code changes or manual clear
    """
    return DataLoader()
```

**Data-Level Cache:**
```python
@st.cache_data(ttl=3600)  # 1 hour TTL
def calculate_metrics(df):
    """
    Cached based on input data hash
    TTL: 3600 seconds (configurable)
    """
    return expensive_calculation(df)
```

**Cache Invalidation:**
- Automatic: Code changes, TTL expiration
- Manual: "Clear Cache" button in Streamlit sidebar

---

## 4. System Interfaces

### 4.1 User Interfaces

**Web Browser Requirements:**
- **Supported Browsers:** Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Screen Resolution:** Minimum 1366x768, Optimized for 1920x1080
- **JavaScript:** Required (enabled)
- **Cookies:** Required for session management (future)

**UI Components:**

1. **Navigation Sidebar:**
   - Width: 300px
   - Position: Left
   - Collapsible: Yes
   - Contents: Page links, filters, settings

2. **Main Content Area:**
   - Layout: Wide (full width)
   - Max width: 100%
   - Padding: 2rem
   - Background: White

3. **Header Section:**
   - Logo: Top-left, 180px width
   - Banner: Gradient background (Navy to lighter navy)
   - Title: Gold (#FFD700), 2.8rem
   - Subtitle: White, 1.2rem

4. **Footer Section:**
   - Position: Fixed bottom
   - Background: Navy gradient
   - Text: White with gold accent
   - Height: 60px

### 4.2 API Interfaces (Future)

**RESTful API Endpoints (Planned):**

```
GET  /api/v1/customers          # List customers
GET  /api/v1/customers/:id      # Get customer details
GET  /api/v1/accounts           # List accounts
GET  /api/v1/accounts/:id       # Get account details
GET  /api/v1/metrics/churn      # Get churn data
GET  /api/v1/metrics/quarterly  # Get quarterly performance
POST /api/v1/auth/login         # User login
POST /api/v1/auth/logout        # User logout
GET  /api/v1/bookmarks          # Get user bookmarks
POST /api/v1/bookmarks          # Create bookmark
```

**Authentication:**
```
Authorization: Bearer <JWT_TOKEN>
```

**Response Format:**
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2025-10-21T10:30:00Z"
}
```

### 4.3 Data Interfaces

**Input: CSV Files**
```
Location: data/ directory
Format: UTF-8 CSV
Headers: Required (first row)
Upload: Manual file replacement
Validation: On load (schema check)
```

**Output: Exported Data**
```
Format: CSV (Comma-separated values)
Encoding: UTF-8
Headers: Included
Filename: <dashboard>_export_<timestamp>.csv
```

---

## 5. Performance Specifications

### 5.1 Response Time Requirements

| Operation | Target | Maximum | Current |
|-----------|--------|---------|---------|
| Initial page load | 3s | 5s | 2-5s ✅ |
| Dashboard switch | 1s | 2s | <1s ✅ |
| Chart render | 1s | 2s | <2s ✅ |
| Data export | 2s | 5s | <3s ✅ |
| Search/filter | 0.5s | 1s | <0.5s ✅ |

### 5.2 Capacity Requirements

**Data Volume:**
- Current: 259,881 account records
- 1 Year: 350,000 records (projected)
- 3 Years: 500,000 records (projected)

**User Capacity:**
- Current: 1-5 concurrent users
- Phase 1 (with auth): 10-20 concurrent users
- Phase 2 (with database): 50-100 concurrent users

**Storage:**
- CSV files: 100MB current, 200MB projected
- PostgreSQL: 1GB initial, 5GB projected (3 years)

### 5.3 Scalability Targets

**Horizontal Scaling:**
- Replit deployment can scale cores automatically
- Target: Support 100 concurrent users without degradation

**Vertical Scaling:**
- Database: Neon supports vertical scaling on-demand
- Application: Streamlit can utilize multiple cores

---

## 6. Security Specifications

### 6.1 Authentication Specifications (Planned)

**Password Requirements:**
- Minimum length: 12 characters
- Must contain: Uppercase, lowercase, number, special char
- Hashing algorithm: bcrypt (cost factor 12)
- Password reset: Email link with 1-hour expiration

**Session Management:**
- Session token: 256-bit random (cryptographically secure)
- Storage: Streamlit session_state + PostgreSQL
- Expiration: 8 hours of inactivity
- Renewal: On each user interaction

### 6.2 Authorization Specifications (5-Level RBAC)

**Role Permissions Matrix:**

| Feature | Level 1 (Exec) | Level 2 (Mgr) | Level 3 (Analyst) | Level 4 (RO) | Level 5 (External) |
|---------|----------------|---------------|-------------------|--------------|-------------------|
| Executive Summary | ✅ Full | ✅ Full | ✅ View | ✅ View | ✅ Limited KPIs |
| Email Accounts | ✅ Full | ✅ Full | ✅ View | ❌ | ❌ |
| Account Activity | ✅ Full | ✅ Full | ✅ Full | ✅ View | ❌ |
| Customer Metrics | ✅ Full | ✅ Full | ✅ View | ❌ | ❌ |
| Quarterly Performance | ✅ Full | ✅ Full | ✅ View | ✅ View | ❌ |
| Campaign Analysis | ✅ Full | ✅ Full | ✅ Full | ❌ | ❌ |
| CSV Export | ✅ All | ✅ Limited | ❌ | ❌ | ❌ |
| Bookmarks | ✅ | ✅ | ✅ | ✅ | ❌ |
| Admin Functions | ✅ | ❌ | ❌ | ❌ | ❌ |

### 6.3 Data Protection

**Sensitive Data:**
- Customer names: PII (Personally Identifiable Information)
- Email addresses: PII
- Account numbers: Confidential
- Balances: Confidential

**Protection Measures:**
- Database: Encrypted at rest (Neon provides)
- Transit: TLS 1.2+ for all connections
- Application: No sensitive data in logs
- Exports: Access controlled by role

---

## 7. Quality Attributes

### 7.1 Availability
**Target:** 99.5% uptime  
**Measured:** Monthly  
**Dependency:** Replit platform SLA

### 7.2 Data Accuracy
**Target:** 100% calculation accuracy  
**Validation:** Automated tests on KPI logic  
**Source:** Core banking system (Intellect/IDC) - assumed accurate

### 7.3 User Satisfaction
**Target:** 90% user satisfaction (surveys)  
**Metrics:** Task completion rate, time-on-task  
**Feedback:** User interviews, support tickets

---

## 8. Constraints and Assumptions

### 8.1 Technical Constraints

1. **Platform Dependency:** Tied to Replit infrastructure
2. **Streamlit Limitations:** No native authentication (must build custom)
3. **Python-Only:** Cannot use other languages (JavaScript, etc.)
4. **CSV Performance:** Large files (>100MB) may slow down
5. **Single Server:** No multi-server deployment currently

### 8.2 Business Constraints

1. **Data Access:** Dependent on core banking data extracts
2. **Update Frequency:** Manual CSV uploads (no automated ETL)
3. **User Base:** Limited to NMB Bank employees
4. **Budget:** Development time (solo developer)

### 8.3 Assumptions

1. **Data Quality:** Core banking data is accurate and complete
2. **User Training:** Basic computer literacy assumed
3. **Internet Access:** Users have stable internet connection
4. **Browser Support:** Modern browsers (last 2 versions)
5. **Data Volume:** Growth rate ~35% per year

---

## 9. Testing Requirements

### 9.1 Unit Testing

**Scope:** utils/ modules (data_loader, data_processor, metrics_calculator)

**Framework:** pytest

**Coverage Target:** 80% code coverage

**Example Test:**
```python
def test_activity_segmentation():
    processor = DataProcessor(mock_loader)
    active, inactive = processor.get_account_activity_segments(90)
    
    assert len(active) + len(inactive) == total_accounts
    assert all(active['days_since_last_tran'] <= 90)
    assert all(inactive['days_since_last_tran'] > 90)
```

### 9.2 Integration Testing

**Scope:** Dashboard pages end-to-end

**Framework:** Playwright (via `run_test` tool)

**Test Cases:**
- Dashboard loads successfully
- Data displays correctly
- Filters apply as expected
- Export functionality works
- Navigation between pages

### 9.3 Performance Testing

**Tools:** Python profiling (cProfile), Streamlit performance monitor

**Metrics:**
- Page load time under load
- Memory usage with 259K records
- Chart rendering time
- Data cache effectiveness

### 9.4 User Acceptance Testing (UAT)

**Participants:** MBC department stakeholders  
**Scenarios:** Real-world use cases  
**Duration:** 2 weeks  
**Acceptance:** 90% task completion success rate  

---

## 10. Deployment Specifications

### 10.1 Deployment Environment

**Platform:** Replit Cloud  
**URL:** https://[project-slug].replit.app  
**Port:** 5000 (internal), 443 (external HTTPS)  
**SSL:** Automatic (Replit provides)

### 10.2 Deployment Process

**Current (Continuous Deployment):**
```
1. Code changes saved in Replit editor
2. Workflow auto-restarts
3. Application live in ~10 seconds
```

**Future (with Git workflow):**
```
1. Develop in feature branch
2. Merge to dev → Deploy to staging
3. Test in staging
4. Merge to main → Deploy to production
5. Rollback available if issues
```

### 10.3 Configuration

**Environment Variables (Required):**
```
DATABASE_URL=postgresql://...
SESSION_SECRET=...
ENVIRONMENT=production
```

**Streamlit Config (.streamlit/config.toml):**
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[browser]
gatherUsageStats = false
```

---

## 11. Maintenance Specifications

### 11.1 Backup and Recovery

**Data Backup:**
- CSV files: Versioned in Git (daily commits)
- Database: Neon automatic backups (point-in-time recovery)
- Code: Git repository (full history)

**Recovery Time Objective (RTO):** 1 hour  
**Recovery Point Objective (RPO):** 24 hours

### 11.2 Monitoring

**Application Monitoring:**
- Replit platform status
- Streamlit logs (errors, warnings)
- User session tracking (future)

**Database Monitoring:**
- Connection pool status
- Query performance
- Storage usage

**Alerting:**
- Email notifications for system errors (future)
- Dashboard admin panel for health status (future)

### 11.3 Support

**Support Levels:**
- **L1 (User Support):** Email/ticket system
- **L2 (Technical Support):** Developer investigation
- **L3 (Platform Support):** Replit support team

**SLA:**
- Critical issues: 4 hours response
- High issues: 1 business day
- Medium/Low: 3 business days

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **ACNTS** | Account field prefix in core banking system |
| **Churn** | Customer attrition rate (lost customers) |
| **CIF** | Customer Information File |
| **Funded Account** | Account with positive balance |
| **GL** | General Ledger |
| **IDC** | Core banking system component |
| **Intellect** | Core banking platform (Temenos) |
| **KPI** | Key Performance Indicator |
| **MBC** | Marketing & Brand Communications |
| **NMB** | NMB Bank Zimbabwe |
| **RBAC** | Role-Based Access Control |
| **RBZ** | Reserve Bank of Zimbabwe |

---

## 13. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-21 | Terence Tachiona | Initial technical specifications |

---

**Approval:**
- ☐ Technical Lead: Terence Tachiona
- ☐ Business Stakeholder: MBC Department Head
- ☐ IT Security: Security Team (for auth phase)

---

**Document Status:** Approved for Phase 1 (Core Dashboards)  
**Next Review:** After authentication implementation (Phase 2)  
**Owner:** Terence Tachiona, NMB Business Intelligence
