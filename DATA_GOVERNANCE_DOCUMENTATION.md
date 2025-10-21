# Data Governance & Management Documentation

## 📋 Overview

This document outlines the data governance framework, data management practices, and data quality standards for the Marketing & Brand Communications BI Portal.

---

## 🎯 Data Governance Framework

### 1. Data Ownership & Stewardship

**Data Owner:** Marketing & Brand Communications Department  
**Technical Steward:** IT/Data Team  
**Business Stewards:** Department Heads

**Responsibilities:**
- **Data Owner:** Defines business rules and data usage policies
- **Technical Steward:** Ensures data quality, security, and technical compliance
- **Business Stewards:** Validates data accuracy and business logic

### 2. Data Classification

| Classification | Description | Examples | Access Level |
|---|---|---|---|
| **Public** | Non-sensitive aggregated metrics | Total accounts, branch counts | All users |
| **Internal** | Business metrics | Product performance, activity rates | Department users |
| **Confidential** | Customer-related data | Account names, customer IDs | Authorized users only |
| **Restricted** | Sensitive financial data | Account balances, transactions | Executive/Finance only |

### 3. Data Access Policy

**Access Tiers:**
1. **Executive View:** Full access to all dashboards and data exports
2. **Operational View:** Access to operational dashboards (Activity, Accounts)
3. **Read-Only View:** View dashboards, no export capability

**Access Request Process:**
1. Submit access request to Data Owner
2. Justify business need
3. Approval by department head
4. Technical provisioning by IT

---

## 📊 Data Sources & Lineage

### Primary Data Sources

#### 1. Core Banking System (Intellect/IDC)

**System:** Intellect Core Banking Platform  
**Extract Frequency:** Daily (automated)  
**Extract Type:** Full snapshot for accounts, Incremental for transactions

**Tables:**
- **ACNTS (Accounts Master)**
  - Purpose: Account information, status, and attributes
  - Key Fields: ACNTS_INTERNAL_ACNUM, ACNTS_CLIENT_NUM, ACNTS_PROD_CODE
  - Update Frequency: Real-time in source, Daily extract
  
- **CLIENTS (Customer Master)**
  - Purpose: Customer demographics and classification
  - Key Fields: Clients Code, Clients Name, Clients Segment Code
  - Update Frequency: Real-time in source, Daily extract

- **TRANSACTIONS (Transaction Data)**
  - Purpose: Account transactions and GL postings
  - Key Fields: TRAN_INTERNAL_ACNUM, TRAN_DATE_OF_TRAN, TRAN_AMOUNT
  - Update Frequency: Continuous, Daily extract

#### 2. Reference Data

**GL Categories:**
- Source: Chart of Accounts
- Purpose: Income/expense classification
- Update Frequency: Monthly or as needed

**Product Types:**
- Source: Product Catalog
- Purpose: Product classification and attributes
- Update Frequency: Quarterly or as needed

**RBZ Sector Classification:**
- Source: Reserve Bank of Zimbabwe
- Purpose: Industry/sector segmentation
- Update Frequency: Annually or as regulatory requirements change

### Data Flow Diagram

```
┌─────────────────────────────────────────┐
│   Core Banking System (Intellect/IDC)  │
│                                         │
│  ┌─────────────┐  ┌──────────────┐    │
│  │  ACNTS      │  │   CLIENTS    │    │
│  │  (Accounts) │  │  (Customers) │    │
│  └──────┬──────┘  └──────┬───────┘    │
│         │                 │             │
│         │                 │             │
│  ┌──────┴─────────────────┴──────┐    │
│  │      TRANSACTIONS              │    │
│  │   (Daily GL Postings)          │    │
│  └──────┬─────────────────────────┘    │
└─────────┼─────────────────────────────┘
          │
          │ Daily Extract (CSV)
          │
          ▼
┌─────────────────────────────────────────┐
│      Data Staging Area                  │
│  (CSV Files in /data folder)            │
│                                         │
│  - accounts_data.csv                    │
│  - customers_data.csv                   │
│  - transactions_2025.csv                │
│  - revenue.csv                          │
└─────────┬───────────────────────────────┘
          │
          │ Data Loading & Validation
          │
          ▼
┌─────────────────────────────────────────┐
│   Data Processing Layer (Python)        │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Data Loader (data_loader.py)   │   │
│  │  - CSV parsing                   │   │
│  │  - Date formatting               │   │
│  │  - Column validation             │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│             ▼                           │
│  ┌─────────────────────────────────┐   │
│  │ Data Processor                   │   │
│  │ (data_processor.py)              │   │
│  │  - Activity segmentation         │   │
│  │  - Customer aggregation          │   │
│  │  - Churn calculation             │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│             ▼                           │
│  ┌─────────────────────────────────┐   │
│  │ Metrics Calculator               │   │
│  │ (metrics_calculator.py)          │   │
│  │  - KPIs                          │   │
│  │  - Growth rates                  │   │
│  │  - Penetration rates             │   │
│  └──────────┬──────────────────────┘   │
└─────────────┼───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      BI Portal Dashboards               │
│  (Streamlit Web Application)            │
│                                         │
│  - Executive Summary                    │
│  - Active Email Accounts                │
│  - Account Activity                     │
│  - Customer Metrics                     │
│  - Quarterly Performance                │
│  - Campaign Analysis                    │
└─────────────────────────────────────────┘
```

---

## 🔍 Data Quality Standards

### Data Quality Dimensions

#### 1. Completeness
**Definition:** Degree to which all required data is present

**Rules:**
- Account Number: 100% required
- Customer ID: 100% required
- Product Code: 100% required
- Opening Date: 100% required
- Currency Code: 100% required

**Validation:**
```python
# Check for missing critical fields
required_fields = ['ACNTS_ACCOUNT_NUMBER', 'ACNTS_CLIENT_NUM', 
                   'ACNTS_PROD_CODE', 'ACNTS_OPENING_DATE', 
                   'ACNTS_CURR_CODE']
completeness_rate = (df[required_fields].notna().sum() / len(df)) * 100
```

**Action:** Reject records with missing critical fields

#### 2. Accuracy
**Definition:** Degree to which data correctly represents reality

**Rules:**
- Account Status must be one of: ACTIVE, CLOSED, SUSPENDED
- Currency codes must be valid ISO codes (ZWL, USD, ZAR, etc.)
- Branch codes must exist in branch master
- Product codes must exist in product catalog

**Validation:**
```python
# Validate account status
valid_statuses = ['ACTIVE', 'CLOSED', 'SUSPENDED']
invalid_status = df[~df['ACNTS_CREATION_STATUS'].isin(valid_statuses)]

# Validate currency codes
valid_currencies = ['ZWL', 'USD', 'ZAR', 'GBP', 'EUR']
invalid_currency = df[~df['ACNTS_CURR_CODE'].isin(valid_currencies)]
```

**Action:** Flag and investigate invalid records

#### 3. Consistency
**Definition:** Data is consistent across systems and time

**Rules:**
- Account numbers unique across the system
- Customer IDs consistent between accounts and customer tables
- Transaction dates not in future
- Closure dates after opening dates

**Validation:**
```python
# Check date consistency
date_issues = df[df['ACNTS_CLOSURE_DATE'] < df['ACNTS_OPENING_DATE']]

# Check uniqueness
duplicate_accounts = df[df.duplicated(subset=['ACNTS_ACCOUNT_NUMBER'])]
```

**Action:** Investigate and resolve inconsistencies

#### 4. Timeliness
**Definition:** Data is up-to-date and available when needed

**Rules:**
- Account data refreshed daily
- Transaction data refreshed daily
- Reference data refreshed monthly
- Maximum lag: 24 hours for operational data

**Validation:**
```python
# Check data freshness
latest_transaction_date = df['ACNTS_LAST_TRAN_DATE'].max()
days_old = (datetime.now() - latest_transaction_date).days

if days_old > 1:
    alert_stakeholders("Data may be stale")
```

**Action:** Alert if data is not current

#### 5. Validity
**Definition:** Data conforms to defined formats and ranges

**Rules:**
- Dates in valid format (YYYY-MM-DD or DD/MM/YYYY)
- Numeric fields contain only numbers
- Text fields within character limits
- Branch codes are 1-2 digits
- Product codes are 4 digits

**Validation:**
```python
# Validate date formats
df['ACNTS_OPENING_DATE'] = pd.to_datetime(df['ACNTS_OPENING_DATE'], 
                                           errors='coerce')
invalid_dates = df[df['ACNTS_OPENING_DATE'].isna()]

# Validate numeric fields
df['ACNTS_BRN_CODE'] = pd.to_numeric(df['ACNTS_BRN_CODE'], 
                                      errors='coerce')
```

**Action:** Convert or flag invalid formats

### Data Quality Metrics

**Target Quality Scores:**
- Completeness: ≥ 99%
- Accuracy: ≥ 98%
- Consistency: ≥ 99%
- Timeliness: ≤ 24 hours
- Validity: ≥ 97%

**Overall Data Quality Score:**
```
DQ Score = (Completeness + Accuracy + Consistency + Validity) / 4
Target: ≥ 98%
```

---

## 🛡️ Data Security & Privacy

### Security Measures

#### 1. Data Encryption
- **At Rest:** CSV files stored with file system encryption
- **In Transit:** HTTPS for all web access
- **In Memory:** Session-based caching, cleared on logout

#### 2. Access Controls
- **Authentication:** Required for all users
- **Authorization:** Role-based access (Executive, Operational, Read-only)
- **Audit Logging:** All data access logged with user ID and timestamp

#### 3. Data Masking
For demonstration/testing purposes:
- **Account Numbers:** Mask middle digits (411012*****8901)
- **Customer Names:** Use initials or generic names
- **Balances:** Use percentages or ranges instead of actual amounts

#### 4. Data Retention
- **Active Data:** 24 months rolling
- **Archived Data:** 7 years (regulatory requirement)
- **Backup:** Daily incremental, Weekly full
- **Purge Schedule:** Automated after retention period

### Privacy Compliance

**GDPR/Data Protection Principles:**
1. **Lawful Basis:** Legitimate interest for business analytics
2. **Purpose Limitation:** Data used only for BI/analytics
3. **Data Minimization:** Only necessary fields collected
4. **Accuracy:** Data quality procedures in place
5. **Storage Limitation:** Defined retention periods
6. **Security:** Encryption and access controls
7. **Accountability:** This documentation serves as evidence

**Customer Rights:**
- Right to access their data
- Right to rectification
- Right to erasure (subject to regulatory requirements)
- Right to restrict processing

---

## 📏 Business Rules & Logic

### Account Activity Classification

**Active Account:**
```
IF ACNTS_LAST_TRAN_DATE >= (TODAY - 90 days)
   AND ACNTS_CLOSURE_DATE IS NULL
   AND ACNTS_CREATION_STATUS = 'ACTIVE'
THEN Account_Status = 'ACTIVE'
```

**Inactive Account:**
```
IF ACNTS_LAST_TRAN_DATE < (TODAY - 90 days)
   AND ACNTS_CLOSURE_DATE IS NULL
   AND ACNTS_CREATION_STATUS = 'ACTIVE'
THEN Account_Status = 'INACTIVE'
```

**Dormant Account:**
```
IF ACNTS_DORMANT_ACNT = 'Y'
   OR ACNTS_INOP_ACNT = 'Y'
THEN Account_Status = 'DORMANT'
```

### Customer Metrics

**Unique Customers:**
```python
unique_customers = accounts_df['ACNTS_CLIENT_NUM'].nunique()
```

**Average Products per Customer (excluding Account & Card):**
```python
# Exclude Account and Card product classes
filtered_df = accounts_df[
    ~accounts_df['Product Class'].isin(['Account', 'Card'])
]

# Calculate products per customer
products_per_customer = (
    filtered_df.groupby('ACNTS_CLIENT_NUM')['ACNTS_PROD_CODE']
    .nunique()
    .mean()
)
```

**Monthly Churn Rate:**
```python
# Customers who closed all accounts in a month
churned = accounts_df[
    accounts_df['ACNTS_CLOSURE_DATE'].dt.to_period('M') == period
]['ACNTS_CLIENT_NUM'].nunique()

# Total active customers at start of month
total_customers = accounts_df[
    (accounts_df['ACNTS_OPENING_DATE'] < period_start) &
    ((accounts_df['ACNTS_CLOSURE_DATE'].isna()) | 
     (accounts_df['ACNTS_CLOSURE_DATE'] >= period_start))
]['ACNTS_CLIENT_NUM'].nunique()

churn_rate = (churned / total_customers) * 100
```

### Quarterly Performance

**Funded Account:**
```
IF ACNTS_OPENING_DATE <= Quarter_End_Date
   AND ACNTS_LAST_TRAN_DATE >= Quarter_Start_Date
   AND ACNTS_CLOSURE_DATE IS NULL
THEN Account_Is_Funded = TRUE
```

**Quarter-on-Quarter Growth:**
```python
qoq_growth = ((Q2_accounts - Q1_accounts) / Q1_accounts) * 100
```

### Campaign Analysis

**Non-Funded Income Categories:**
- Commission Income (GL codes 3010101*)
- Fee Income (GL codes 3010102*)
- Service Charges (GL codes 3010103*)
- Other Non-Interest Income

**Month-on-Month Revenue Change:**
```python
mom_change_pct = ((current_month - previous_month) / previous_month) * 100
mom_change_abs = current_month - previous_month
```

---

## 📊 Data Dictionary

### Account Data (ACNTS)

Refer to `accounts_datadictionary_*.csv` for complete field definitions.

**Key Fields:**
- **ACNTS_INTERNAL_ACNUM:** System unique identifier (Primary Key)
- **ACNTS_ACCOUNT_NUMBER:** Customer-facing account number
- **ACNTS_CLIENT_NUM:** Customer identifier (Foreign Key to Clients)
- **ACNTS_PROD_CODE:** Product code (Foreign Key to Products)
- **ACNTS_BRN_CODE:** Branch code
- **ACNTS_CURR_CODE:** Currency code (ISO)
- **ACNTS_OPENING_DATE:** Account opening date
- **ACNTS_LAST_TRAN_DATE:** Last transaction date
- **ACNTS_CLOSURE_DATE:** Account closure date (NULL if active)
- **ACNTS_CREATION_STATUS:** Account status (ACTIVE/CLOSED/SUSPENDED)

### Product Data

See `PRODUCT TYPE LOOKUP TABLE_*.csv`

**Key Fields:**
- **Product Code:** Unique product identifier
- **Product Name:** Display name
- **Product Class:** Category (F=Funding, L=Lending)
- **Product Group Code:** Sub-category

### GL Categories

See `GL CATEGORY LOOKUP TABLE_*.csv`

**Key Fields:**
- **Gl Number:** GL account number
- **Gl Name:** Account description
- **Gl Type:** I=Income, E=Expense, A=Asset, L=Liability
- **Gl Catg Code:** Category code

### RBZ Sector Classification

See `RBZ SECTOR CLASSIFICATION LOOKUP TABLE_*.csv`

**Key Fields:**
- **Company Name:** Company/customer name
- **RBZ Sector Classification:** Industry sector

---

## 🔄 Data Refresh Process

### Daily Refresh Procedure

1. **Extract (Source System)**
   - Time: 01:00 AM daily
   - Method: Automated SQL query
   - Format: CSV export
   - Location: Staging server

2. **Transform (ETL Process)**
   - Validate data quality
   - Apply business rules
   - Format dates consistently
   - Remove duplicates

3. **Load (BI Portal)**
   - Upload to `/data` folder
   - Automatic detection and loading
   - Cache invalidation
   - User notification

4. **Validate (Post-Load)**
   - Record count verification
   - Data quality checks
   - Metric reconciliation
   - Alert on anomalies

### Manual Refresh (if needed)

1. Access core banking system
2. Run predefined extract queries
3. Export to CSV format
4. Upload to `/data` folder in Replit
5. Refresh browser
6. Verify data loading in dashboards

---

## 📈 Monitoring & Maintenance

### Data Quality Monitoring

**Daily Checks:**
- Record counts match expected volumes
- No duplicate account numbers
- All required fields populated
- Dates within valid ranges

**Weekly Checks:**
- Data quality score ≥ 98%
- Referential integrity maintained
- No orphaned records

**Monthly Checks:**
- Reference data updated
- Business rules still valid
- User feedback incorporated

### Issue Resolution

**Data Quality Issues:**
1. Log issue with details
2. Investigate root cause
3. Correct at source if possible
4. Apply transformation rule if systematic
5. Document resolution
6. Monitor recurrence

**Performance Issues:**
1. Check data volume
2. Optimize queries if needed
3. Consider data archiving
4. Review caching strategy

---

## 📝 Change Management

### Data Model Changes

All changes to data structure require:
1. Impact analysis
2. Testing in development environment
3. User acceptance testing
4. Documentation update
5. Deployment approval
6. User communication

### Business Rule Changes

1. Document proposed change
2. Get business approval
3. Update code and documentation
4. Test with historical data
5. Deploy and monitor

---

## 📞 Contacts & Escalation

**Data Governance Team:**
- Data Owner: Marketing Department Head
- Technical Lead: IT Manager
- Data Analyst: BI Team Lead

**Escalation Path:**
1. Data quality issues → Data Analyst
2. Access issues → Technical Lead
3. Business rule questions → Data Owner
4. System outages → IT Support

---

**Document Version:** 1.0  
**Last Updated:** October 21, 2025  
**Next Review Date:** January 21, 2026  
**Owner:** Marketing & Brand Communications Department
