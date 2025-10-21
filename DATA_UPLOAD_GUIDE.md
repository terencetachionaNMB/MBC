# Data Upload Guide for BI Portal

## 📁 Required Data Files

To fully populate your BI Portal with actual banking data, please upload the following CSV files to the `data/` folder:

### 1. Core Account Data (REQUIRED)
**File:** `accounts_data.csv`

This is your main account extract from the Intellect/IDC core banking system. It should contain all ACNTS_* columns from your accounts table.

**Required Columns:**
- ACNTS_ENTITY_NUM
- ACNTS_INTERNAL_ACNUM
- ACNTS_BRN_CODE
- ACNTS_CLIENT_NUM
- ACNTS_ACCOUNT_NUMBER
- ACNTS_PROD_CODE
- ACNTS_OPENING_DATE
- ACNTS_AC_NAME1
- ACNTS_CURR_CODE
- ACNTS_LAST_TRAN_DATE
- ACNTS_CLOSURE_DATE
- ACNTS_CREATION_STATUS
- And all other ACNTS_* fields from your system

**Sample data has been loaded** to demonstrate portal functionality. Replace it with your actual account extract.

### 2. Customer Master Data (OPTIONAL)
**File:** `customers_data.csv`

Customer/client information from your CIF (Customer Information File).

**Required Columns:**
- Clients Code (links to ACNTS_CLIENT_NUM)
- Clients Name
- Clients Type Flg
- Clients Home Brn Code
- Clients Segment Code
- Clients Opening Date
- And other Clients_* fields

### 3. Transaction Data (OPTIONAL - For Campaign Analysis)
**Files:** 
- `transactions_2024.csv`
- `transactions_2025.csv`
- `revenue.csv`

Transaction extracts for revenue analysis and campaign tracking.

**Required Columns:**
- TRAN_INTERNAL_ACNUM (links to ACNTS_INTERNAL_ACNUM)
- TRAN_DATE_OF_TRAN
- TRAN_VALUE_DATE
- TRAN_AMOUNT
- TRAN_GLACC_CODE
- TRAN_DB_CR_FLG
- TRAN_SERVICE_CODE
- TRAN_TRANSACTION_CODE

### 4. Lookup Tables (ALREADY LOADED ✓)
These files are already in place:
- ✓ `accounts_datadictionary_*.csv`
- ✓ `RBZ SECTOR CLASSIFICATION LOOKUP TABLE_*.csv`
- ✓ `GL CATEGORY LOOKUP TABLE_*.csv`
- ✓ `PRODUCT TYPE LOOKUP TABLE_*.csv`

---

## 📊 Current Status

**Currently Loaded:**
- ✓ Sample account data (50 accounts for demonstration)
- ✓ RBZ Sector Classification lookup (2,346 companies)
- ✓ GL Category lookup (3,583 GL accounts)
- ✓ Product Type lookup (192 products)
- ✓ Account data dictionary (93 field definitions)

**Missing (Upload to activate):**
- ⏳ Actual account data from your core banking system
- ⏳ Customer master data (CIF)
- ⏳ Transaction/revenue data for campaign analysis

---

## 🔄 How to Upload Your Data

### Option 1: Direct File Upload (Recommended)
1. Prepare your CSV exports from Intellect/IDC
2. Upload them to the `data/` folder in this Replit workspace
3. Ensure file names match the expected names above
4. Refresh the BI Portal - data will load automatically

### Option 2: Via Replit File Manager
1. Click on the "Files" icon in the left sidebar
2. Navigate to the `data/` folder
3. Click the "Upload file" button (or drag and drop)
4. Select your CSV files
5. Wait for upload to complete
6. Refresh your browser

---

## 📋 Data Quality Checklist

Before uploading, ensure:

- [ ] CSV files are properly formatted (comma-separated)
- [ ] Column names match exactly (case-sensitive)
- [ ] Date fields are in consistent format (YYYY-MM-DD or DD/MM/YYYY)
- [ ] No special characters in file names
- [ ] Files are UTF-8 encoded
- [ ] Numeric fields don't contain commas (use periods for decimals)
- [ ] Account numbers are unique
- [ ] Customer IDs link correctly between accounts and customers tables

---

## 🎯 Dashboard Data Requirements

### Executive Summary
- **Requires:** Account data, Product lookup
- **Optional:** Customer data for segmentation

### Active Email Accounts
- **Requires:** Account data with ACNTS_CREATION_STATUS
- **Optional:** Email field in account or customer data

### Account Activity
- **Requires:** Account data with ACNTS_LAST_TRAN_DATE
- **Uses:** 90-day activity threshold

### Customer Metrics
- **Requires:** Account data with ACNTS_CLIENT_NUM, ACNTS_PROD_CODE
- **Optional:** ACNTS_CLOSURE_DATE for churn calculation

### Quarterly Performance
- **Requires:** Account data with ACNTS_OPENING_DATE, ACNTS_LAST_TRAN_DATE
- **Filters:** Active accounts per quarter in 2025

### Campaign Analysis
- **Requires:** Transaction/Revenue data with TRAN_DATE_OF_TRAN, TRAN_AMOUNT
- **Period:** June - September 2025
- **Focus:** Non-funded income (fees, commissions)

---

## 🔐 Data Security

**Important Security Notes:**
1. This portal uses **development data only**
2. Do NOT upload production data containing:
   - Real customer PII (Personal Identifiable Information)
   - Actual account balances
   - Transaction details
   
3. For demonstration purposes:
   - Anonymize customer names
   - Mask account numbers
   - Use sample balances
   - Aggregate transaction data

4. For production use:
   - Implement proper access controls
   - Use database instead of CSV files
   - Enable authentication
   - Encrypt sensitive data

---

## 📞 Support

If you encounter issues:
1. Check that column names match exactly
2. Verify date formats are consistent
3. Ensure numeric fields don't have formatting
4. Review browser console for errors
5. Check the portal's data quality indicators

---

## 📈 Next Steps

1. **Review the portal** with sample data to understand functionality
2. **Prepare your data exports** from Intellect/IDC
3. **Upload actual data files** to replace sample data
4. **Verify data loading** in each dashboard
5. **Publish the portal** for internal use
6. **Schedule data refreshes** (daily/weekly)
7. **Train users** on dashboard features

---

## 🎨 Customization Options

After data is loaded, you can:
- Adjust activity thresholds (default: 90 days)
- Modify campaign periods
- Filter by branch, product, currency
- Export reports to CSV
- Drill down into specific segments
- Compare time periods

---

**Portal Version:** 1.0  
**Last Updated:** October 21, 2025  
**Data Sources:** Intellect/IDC Core Banking System
