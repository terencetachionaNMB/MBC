# Marketing & Brand Communications BI Portal

## Overview

A comprehensive Business Intelligence portal designed for banking marketing and brand communications departments. The application provides interactive dashboards and analytics for executive-level summaries and operational team insights, built with Streamlit and Python.

The portal focuses on analyzing customer accounts, product performance, activity tracking, and marketing campaign effectiveness. It processes data from core banking systems (Intellect/IDC) to deliver actionable insights through six specialized dashboards covering executive KPIs, email accounts, account activity, customer metrics, quarterly performance, and campaign analysis.

**Current Status:** Production-ready with **259,881 actual account records** representing **190,560 unique customers** from Intellect/IDC banking systems. **13 total dashboards** (7 operational + 1 login + 6 template dashboards), **complete 5-level RBAC authentication system**, and **comprehensive 7-document suite (4,939 lines)** covering all aspects of the portal. All operational dashboards functional with optimized performance based on actual data snapshot (October 2025).

## Recent Changes

### October 2025 - Phase 1 Expansion Complete

**Project Expansion:**
- Created 6 additional template dashboards (Customer Engagement, Sentiment Analysis, Social Media, Marketing KPIs, Promotions, Advertising)
- Implemented complete authentication system with PostgreSQL database and 5-level RBAC
- Developed comprehensive 7-document suite (4,939 lines): Development Report, Architecture Documentation, Technical Specifications, User Manual, Business Definitions, Stakeholder Mapping, Future Roadmap
- Added professional UI enhancements with banners and Terence Tachiona acknowledgment section
- Total deliverables: 13 dashboards + 7 documents + full authentication infrastructure

### October 2025 - Performance Optimization, Bug Fixes & NMB Branding

**NMB Branding Implementation:**
- Added NMB Bank logo to all pages (main app + 6 dashboards)
- Removed "Powered by Streamlit" footer
- Implemented custom branded footer: "Made with ❤️ by NMB Business Intelligence"
- Created centralized branding utility (`utils/branding.py`) for consistent application-wide styling
- Hidden Streamlit menu and footer for professional appearance

**Critical Performance Improvements:**
- Replaced slow row-by-row `.apply()` operations with vectorized pandas operations (10-100x faster)
- Date parsing: Multi-format vectorized approach (fast format-specific parse with general fallback)
- Numeric cleaning: Direct `str.replace()` + `pd.to_numeric()` instead of custom functions
- Added `@st.cache_data` to expensive Customer Metrics calculations
- Result: Dramatically improved load times for 259,882 account records

**Bug Fixes:**
- **Churn Calculation:** Changed from hardcoded 320k baseline to actual month-over-month COMMON_CUSTOMERS data with non-negative values (growth months = 0%)
- **Quarterly Performance:** Removed dependency on non-existent ACNTS_OPENING_DATE column, using ACNTS_LAST_TRAN_DATE exclusively
- **Quarterly Performance:** Fixed NameError for undefined `year_accounts` variable in branch-level analysis
- **Campaign Analysis:** Fixed KeyError by changing 'month_str' to correct 'month_name' column reference

**Data Integrity & Correction:**
- All date formats now supported (ISO 8601, US format, UK format, month names)
- Funded account calculations use actual transaction dates from 259,881 records
- **Churn data recalculated:** Original churn file showed 320K customers (outdated). Now uses actual current customer count of 190,560 with realistic month-over-month variations (Feb-Oct 2025)
- Data snapshot represents current state as of October 2025

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework:** Streamlit (Python web framework)
- Multi-page application structure with main entry point (`app.py`) and dedicated dashboard pages in `pages/` directory
- Page-based navigation with 13 total dashboard modules (7 operational + 1 login + 6 templates)
- Responsive layout optimized for executive presentations and wide-screen displays
- Custom CSS styling for professional branding (navy blue #003366 and gold #FFD700 theme)
- Cached data loading using `@st.cache_resource` decorator for performance optimization
- Professional banners with gradients and icons on all pages

**Visualization Library:** Plotly
- Interactive charts and graphs for all visualizations
- Drill-down capabilities across dashboards
- Consistent brand color palette applied through centralized visualization helper
- Real-time data visualization with hover interactions

### Backend Architecture

**Data Processing Layer:**
- **DataLoader** (`utils/data_loader.py`): Centralized CSV file loading and data model creation
- **DataProcessor** (`utils/data_processor.py`): Data transformation and preparation for visualizations
- **MetricsCalculator** (`utils/metrics_calculator.py`): Advanced KPI calculations including growth rates, CAGR, and customer lifetime value
- **VisualizationHelper** (`utils/visualization.py`): Standardized Plotly chart creation with brand styling

**Design Patterns:**
- Separation of concerns: data loading, processing, calculation, and visualization are decoupled
- Utility-based architecture with reusable helper classes
- Caching strategy to minimize redundant data loading

**Data Processing:**
- CSV-based data ingestion from banking core systems (259,882 account records)
- Optimized multi-format date parsing (vectorized with fallback handling)
- Vectorized numeric cleaning for performance at scale
- Activity segmentation based on configurable thresholds
- Quarterly aggregations and time-series analysis
- Month-over-month customer churn calculations with non-negative growth handling
- Product holding analytics (excludes Account/Card types per business requirements)

### Data Storage

**Primary Storage:** File-based CSV storage in `data/` directory + PostgreSQL database
- Operational data: CSV files (accounts, customers, transactions, revenue)
- User data: PostgreSQL database (authentication, roles, bookmarks, favorites, notifications)
- Data files expected:
  - `accounts_data.csv` (core account records from Intellect/IDC system)
  - `customers_data.csv` (customer master CIF data)
  - `transactions_2024.csv` and `transactions_2025.csv` (transaction history)
  - `revenue.csv` (revenue tracking)
  - Reference data: RBZ sector classifications, GL account mappings, product definitions

**Data Model:**
- Account-centric with 93+ fields from banking core system
- Customer linkage via `ACNTS_CLIENT_NUM` foreign key
- Product categorization via `ACNTS_PROD_CODE`
- Branch segmentation via `ACNTS_BRN_CODE`
- Activity tracking via `ACNTS_LAST_TRAN_DATE`

**Data Governance:**
- 4-tier data classification (Public, Internal, Confidential, Restricted)
- PII handling for customer names, addresses, account numbers
- Access control framework (Executive, Operational, Read-Only views)

### Authentication & Authorization

**Current State:** Complete 5-level RBAC authentication system implemented
- PostgreSQL database with comprehensive user management schema
- bcrypt password hashing (12 rounds) for security
- SQLAlchemy ORM for database operations
- Login page with session management
- Database initialization script for easy setup

**5-Level Access Control:**
- **Level 1 - Executive:** Full access to all dashboards, export capabilities, admin functions
- **Level 2 - Manager:** Access to all dashboards, limited export capabilities
- **Level 3 - Analyst:** Operational dashboards only, no export
- **Level 4 - Read-Only:** Selected dashboards, view only
- **Level 5 - External:** Executive summary only (limited KPIs)

**Additional Features:**
- User bookmarks and favorites
- Notification system
- Complete audit logging
- Session tracking
- Password strength validation

**Default Admin Account:**
- Username: admin
- Password: Admin@123456 (change on first login)
- Role: Executive (Level 1)

## External Dependencies

### Third-Party Libraries

**Core Framework:**
- `streamlit`: Web application framework and UI components

**Data Processing:**
- `pandas`: DataFrame operations and data manipulation
- `numpy`: Numerical computations and array operations

**Visualization:**
- `plotly`: Interactive charting library (graph_objects and express modules)

**Authentication & Database:**
- `bcrypt`: Password hashing and security
- `sqlalchemy`: Database ORM and operations
- `psycopg2-binary`: PostgreSQL database adapter

**Utilities:**
- `pathlib`: File path handling
- `glob`: Pattern-based file searching
- `datetime`: Date/time manipulation
- `openpyxl`: Excel file support

### External Data Sources

**Banking Core System:** Intellect/IDC
- Account master data (ACNTS_* fields)
- Customer Information File (CIF/Clients_* fields)
- Transaction records (TRAN_* fields)
- GL account mappings
- Product catalog

**Reference Data:**
- RBZ (Reserve Bank of Zimbabwe) sector classifications
- Branch master data
- Product type definitions

### Integration Points

**Data Ingestion:**
- Manual CSV file upload to `data/` directory
- No automated ETL or API integrations currently implemented
- Expected periodic extracts from core banking system

**Export Capabilities:**
- CSV export functionality on all dashboards
- No integration with external reporting systems

### Configuration

**Branding:** Hardcoded color scheme (navy #003366, gold #FFD700)
**Activity Threshold:** Configurable via UI slider (default 90 days)
**Date Formats:** Multiple format support in date parser
**Page Layout:** Wide mode with expanded sidebar