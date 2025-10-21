# Business Definitions & Metrics Dictionary
## NMB Bank Marketing & Brand Communications BI Portal

**Document Version:** 1.0  
**Last Updated:** October 21, 2025  
**Purpose:** Standard definitions for business terms and KPI calculations  

---

## Table of Contents

1. [Core Business Terms](#1-core-business-terms)
2. [Customer Metrics](#2-customer-metrics)
3. [Account Metrics](#3-account-metrics)
4. [Activity Metrics](#4-activity-metrics)
5. [Campaign Metrics](#5-campaign-metrics)
6. [Financial Metrics](#6-financial-metrics)
7. [Calculated KPIs](#7-calculated-kpis)
8. [Data Quality Indicators](#8-data-quality-indicators)

---

## 1. Core Business Terms

### 1.1 Customer

**Definition:** An individual or entity with a Customer Information File (CIF) record in the Intellect/IDC core banking system.

**Identifiers:**
- **CIF Number** (ACNTS_CLIENT_NUM): Unique customer identifier
- **Customer Type** (CLIENTS_TYPE_FLG): I=Individual, C=Corporate, S=SME

**Counting Rules:**
- One CIF = One customer, regardless of number of accounts
- Active customer: Has at least one account (any status)
- Unique customers counted by distinct CIF numbers

**Business Context:**
- Current customer base: **190,560 unique customers**
- Tracked via ACNTS_CLIENT_NUM field in accounts data

### 1.2 Account

**Definition:** A financial account linked to a customer, identified by a unique account number.

**Types:**
- **Product-based accounts:** Savings, Current, Fixed Deposit, Loans
- **Service accounts:** Card accounts, facility accounts
- **Exclusions for product holdings:** "Account" and "Card" types excluded from product count

**Identifiers:**
- **Account Number** (ACCOUNT_NUMBER): Unique 13-digit identifier
- **Product Code** (ACNTS_PROD_CODE): Product type classification
- **Branch Code** (ACNTS_BRN_CODE): Originating branch

**Total Accounts:** **259,881 records** as of October 2025

### 1.3 Product

**Definition:** A banking product or service offering that customers can hold.

**Classification:**
- **Savings Products:** Traditional savings, call accounts
- **Transactional Products:** Current accounts, cheque accounts
- **Investment Products:** Fixed deposits, term deposits
- **Lending Products:** Personal loans, mortgages, overdrafts
- **Card Products:** Debit cards, credit cards

**Exclusions:**
- Generic "Account" type (not a distinct product)
- Generic "Card" type (categorization, not product)

**Product Holdings per Customer:**
- Average: **1.36 products per customer** (excluding Account/Card types)
- Range: 1 to 7+ products

### 1.4 Branch

**Definition:** A physical or virtual NMB Bank location serving customers.

**Identifier:**
- **Branch Code** (ACNTS_BRN_CODE): 3-4 digit code

**Types:**
- **Full-service branches:** Complete banking services
- **Micro branches:** Limited service locations
- **Digital branch:** Online/mobile banking (coded as virtual branch)

---

## 2. Customer Metrics

### 2.1 Total Customers

**Definition:** Count of unique customers with at least one account in the system.

**Calculation:**
```python
total_customers = accounts_df['ACNTS_CLIENT_NUM'].nunique()
```

**Current Value:** 190,560

**Business Rule:** One CIF = One customer count

### 2.2 Active Customers

**Definition:** Customers with at least one account showing activity within the specified threshold period (default 90 days).

**Calculation:**
```python
cutoff_date = current_date - timedelta(days=90)
active_accounts = accounts_df[accounts_df['ACNTS_LAST_TRAN_DATE'] >= cutoff_date]
active_customers = active_accounts['ACNTS_CLIENT_NUM'].nunique()
```

**Threshold:** Configurable (30-180 days), default 90 days

**Current Value:** ~189,605 (99.5% of customer base)

### 2.3 Customer Churn

**Definition:** The rate at which customers leave the bank (close all accounts or become inactive).

**Calculation:**
```python
# Month-over-month method
previous_month_customers = 191,200  # Example
current_month_customers = 190,560
lost_customers = previous_month_customers - current_month_customers  # 640

if lost_customers > 0:
    churn_rate = (lost_customers / previous_month_customers) * 100  # 0.33%
else:
    churn_rate = 0  # Growth month, no churn
```

**Reporting Period:** Monthly

**Typical Range:** 0.2% to 1.8% per month

**Data Source:** churn_customers.csv (COMMON_CUSTOMERS field)

### 2.4 Customer Retention

**Definition:** Percentage of customers retained from one period to the next.

**Calculation:**
```python
retention_rate = 100 - churn_rate
```

**Target:** >98% monthly retention

### 2.5 New Customers

**Definition:** Customers acquired during a specific period.

**Calculation:**
```python
# Identified by first account opening date
new_customers_q3 = accounts_df[
    (accounts_df['ACNTS_OPENING_DATE'] >= '2025-07-01') &
    (accounts_df['ACNTS_OPENING_DATE'] <= '2025-09-30')
]['ACNTS_CLIENT_NUM'].nunique()
```

**Note:** Current data uses ACNTS_LAST_TRAN_DATE as proxy when ACNTS_OPENING_DATE unavailable

---

## 3. Account Metrics

### 3.1 Total Accounts

**Definition:** Count of all account records in the system.

**Calculation:**
```python
total_accounts = len(accounts_df)
```

**Current Value:** 259,881 accounts

**Includes:** All statuses (active, inactive, dormant)

### 3.2 Active Accounts

**Definition:** Accounts with at least one transaction within the activity threshold period.

**Calculation:**
```python
cutoff_date = current_date - timedelta(days=90)
active_accounts = accounts_df[accounts_df['ACNTS_LAST_TRAN_DATE'] >= cutoff_date]
active_count = len(active_accounts)
```

**Current Value:** 258,709 (99.5%)

**Threshold:** 90 days (configurable via UI slider)

### 3.3 Inactive Accounts

**Definition:** Accounts with no transactions within the activity threshold period.

**Calculation:**
```python
inactive_accounts = accounts_df[accounts_df['ACNTS_LAST_TRAN_DATE'] < cutoff_date]
inactive_count = len(inactive_accounts)
```

**Current Value:** 1,172 (0.5%)

**Reactivation Opportunity:** Target for marketing campaigns

### 3.4 Funded Accounts

**Definition:** Accounts with a positive balance and recent transaction activity, indicating customer engagement.

**Calculation:**
```python
# Quarterly funded accounts
funded_accounts_q3 = accounts_df[
    (accounts_df['ACNTS_LAST_TRAN_DATE'] >= '2025-07-01') &
    (accounts_df['ACNTS_LAST_TRAN_DATE'] <= '2025-09-30') &
    (accounts_df['BASE_CURR_BAL'] > 0)
]
```

**Business Context:** Key indicator of active, engaged customers

**Data Source:** ACNTS_LAST_TRAN_DATE + BASE_CURR_BAL fields

### 3.5 Dormant Accounts

**Definition:** Accounts with no activity for an extended period (typically >12 months).

**Regulatory Significance:** May require special handling per RBZ guidelines

---

## 4. Activity Metrics

### 4.1 Days Since Last Transaction

**Definition:** Number of calendar days between the last transaction date and the current date.

**Calculation:**
```python
days_since = (current_date - account['ACNTS_LAST_TRAN_DATE']).days
```

**Uses:**
- Activity segmentation
- Reactivation targeting
- Dormancy identification

### 4.2 Activity Threshold

**Definition:** Number of days used to classify accounts as active or inactive.

**Default Value:** 90 days

**Configurable Range:** 30-180 days

**Business Logic:**
- Accounts with transaction within threshold = Active
- Accounts with no transaction within threshold = Inactive

### 4.3 Transaction Frequency

**Definition:** Average number of transactions per account per period.

**Note:** Not currently calculated (requires transaction-level data integration)

**Future Enhancement:** Daily, weekly, monthly transaction counts

---

## 5. Campaign Metrics

### 5.1 Campaign Participant

**Definition:** Customer who engaged with a specific marketing campaign during the campaign period.

**Identification Methods:**
- Account activity during campaign window
- GL revenue attribution
- Product uptake during campaign

**Example:** Non-Funded Income Campaign (June-Sept 2025)
- **Participants:** Customers with fee-generating transactions
- **Period:** June 1 - September 30, 2025
- **Attribution:** GL account linkage to campaign products

### 5.2 Campaign Revenue

**Definition:** Total revenue generated from campaign participants during the campaign period.

**Calculation:**
```python
campaign_revenue = revenue_df[
    (revenue_df['period'] >= campaign_start) &
    (revenue_df['period'] <= campaign_end) &
    (revenue_df['gl_account'].isin(campaign_gl_list))
]['revenue_amount'].sum()
```

**Data Source:** revenue_gls.csv linked to campaign GL accounts

### 5.3 Campaign Conversion Rate

**Definition:** Percentage of targeted customers who became campaign participants.

**Calculation:**
```python
conversion_rate = (participants / targeted_customers) * 100
```

**Future Enhancement:** Requires campaign targeting data

### 5.4 Campaign ROI

**Definition:** Return on Investment for marketing campaign.

**Calculation:**
```python
roi = ((campaign_revenue - campaign_cost) / campaign_cost) * 100
```

**Note:** Requires campaign cost data (not currently tracked)

---

## 6. Financial Metrics

### 6.1 Account Balance

**Definition:** Current balance of an account in base currency (USD).

**Fields:**
- **BASE_CURR_BAL:** Balance in base currency (USD)
- **LOCAL_CURR_BAL:** Balance in local currency (ZWL)
- **ACNTBAL_CURR_CODE:** Currency code

**Business Rule:** Use BASE_CURR_BAL for standardized reporting

### 6.2 Average Balance per Customer

**Definition:** Mean account balance across all customer accounts.

**Calculation:**
```python
avg_balance = accounts_df.groupby('ACNTS_CLIENT_NUM')['BASE_CURR_BAL'].sum().mean()
```

**Note:** Not currently displayed (future enhancement)

### 6.3 Total Deposits

**Definition:** Sum of all positive account balances.

**Calculation:**
```python
total_deposits = accounts_df[accounts_df['BASE_CURR_BAL'] > 0]['BASE_CURR_BAL'].sum()
```

**Future Enhancement:** Segment by product type, branch

---

## 7. Calculated KPIs

### 7.1 Average Products per Customer

**Definition:** Mean number of distinct products held by each customer, excluding generic "Account" and "Card" types.

**Calculation:**
```python
# Exclude generic types
product_accounts = accounts_df[
    ~accounts_df['PRODUCT_NAME'].str.contains('Account|Card', case=False, na=False)
]

# Count distinct products per customer
products_per_customer = product_accounts.groupby('ACNTS_CLIENT_NUM')['ACNTS_PROD_CODE'].nunique()

# Calculate average
avg_products = products_per_customer.mean()
```

**Current Value:** ~1.36 products per customer

**Business Insight:** Cross-sell opportunity (target: 2+ products per customer)

### 7.2 Quarterly Growth Rate

**Definition:** Percentage change in funded accounts from one quarter to the next.

**Calculation:**
```python
growth_rate = ((Q2_funded - Q1_funded) / Q1_funded) * 100
```

**Example:**
- Q1 2025: 150,000 funded accounts
- Q2 2025: 158,000 funded accounts
- Growth: +5.3%

### 7.3 Contactable Customer Rate

**Definition:** Percentage of customers with valid email addresses for marketing outreach.

**Calculation:**
```python
# Exclude placeholders
valid_emails = accounts_df[
    ~accounts_df['INDCLIENT_EMAIL_ADDR1'].str.contains(
        'placeholder|none|test', case=False, na=False
    )
]['ACNTS_CLIENT_NUM'].nunique()

contactable_rate = (valid_emails / total_customers) * 100
```

**Current Value:** ~35.8% (68,118 contactable customers)

**Target:** Increase to 60%+ through data enrichment

### 7.4 Activity Distribution

**Definition:** Percentage breakdown of accounts by activity status.

**Calculation:**
```python
active_pct = (active_accounts / total_accounts) * 100
inactive_pct = (inactive_accounts / total_accounts) * 100
```

**Current Distribution:**
- Active: 99.5%
- Inactive: 0.5%

---

## 8. Data Quality Indicators

### 8.1 Data Completeness

**Definition:** Percentage of required fields populated with valid data.

**Key Fields Monitored:**
- Customer ID (ACNTS_CLIENT_NUM): 100% required
- Account Number (ACCOUNT_NUMBER): 100% required
- Last Transaction Date (ACNTS_LAST_TRAN_DATE): 100% required
- Product Code (ACNTS_PROD_CODE): 100% required
- Email Address (INDCLIENT_EMAIL_ADDR1): 35.8% valid

### 8.2 Data Freshness

**Definition:** Age of data since last update from core banking system.

**Current Status:** Data snapshot as of October 2025

**Update Frequency:** Daily (manual CSV upload)

**Future Target:** Real-time API integration

### 8.3 Data Accuracy

**Definition:** Alignment between BI portal data and core banking system.

**Validation Methods:**
- Cross-check total accounts with core system
- Verify customer counts with CIF database
- Reconcile balances with GL

**Responsibility:** BI team conducts monthly data quality audits

---

## 9. Glossary of Abbreviations

| Abbreviation | Full Term | Definition |
|--------------|-----------|------------|
| **ACNTS** | Accounts | Field prefix for account-related data |
| **CAGR** | Compound Annual Growth Rate | Annualized rate of growth |
| **CIF** | Customer Information File | Core customer master record |
| **CSAT** | Customer Satisfaction | Customer satisfaction score |
| **DAU** | Daily Active Users | App users per day |
| **GL** | General Ledger | Accounting classification |
| **IDC** | Intellect Data Component | Core banking module |
| **KPI** | Key Performance Indicator | Measurable business metric |
| **MAU** | Monthly Active Users | App users per month |
| **MBC** | Marketing & Brand Communications | Department name |
| **NMB** | NMB Bank Zimbabwe | Bank name |
| **NPS** | Net Promoter Score | Customer loyalty metric |
| **RBZ** | Reserve Bank of Zimbabwe | Central bank |
| **ROI** | Return on Investment | Campaign profitability |
| **SME** | Small & Medium Enterprises | Business customer segment |

---

## 10. Metric Ownership

| Metric Category | Primary Owner | Review Frequency |
|-----------------|---------------|------------------|
| Customer Metrics | MBC Manager | Monthly |
| Account Metrics | Operations Team | Weekly |
| Activity Metrics | BI Analyst | Daily |
| Campaign Metrics | Marketing Team | Per Campaign |
| Financial Metrics | Finance Team | Monthly |

---

## 11. Calculation Standards

### 11.1 Percentages

- Round to 1 decimal place (e.g., 99.5%)
- Always include % symbol
- Use consistent rounding (standard rounding, not truncation)

### 11.2 Currency

- Use BASE_CURR_BAL (USD) for all financial calculations
- Format: $1,234.56
- Round to 2 decimal places

### 11.3 Dates

- Format: Month DD, YYYY (e.g., October 21, 2025)
- Time periods: Use inclusive start and end dates
- Quarters: Q1=Jan-Mar, Q2=Apr-Jun, Q3=Jul-Sep, Q4=Oct-Dec

### 11.4 Counts

- Use comma separators for thousands (e.g., 259,881)
- No decimal places for counts
- Label as "count" or "#" to distinguish from amounts

---

**Document Status:** Approved  
**Next Review Date:** January 2026  
**Owner:** Terence Tachiona, NMB Business Intelligence  
**Approved By:** MBC Department Head  

---

*For questions or clarifications on business definitions, contact bi@nmbz.co.zw*
