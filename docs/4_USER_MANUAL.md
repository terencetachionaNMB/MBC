# User Manual
## NMB Bank Marketing & Brand Communications BI Portal

**Version:** 1.0  
**Last Updated:** October 21, 2025  
**Intended Audience:** All Portal Users (Executive, Managers, Analysts)  

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Getting Started](#2-getting-started)
3. [Dashboard Guide](#3-dashboard-guide)
4. [Features and Functions](#4-features-and-functions)
5. [Authentication and Access](#5-authentication-and-access)
6. [Troubleshooting](#6-troubleshooting)
7. [FAQ](#7-faq)
8. [Support](#8-support)

---

## 1. Introduction

### 1.1 What is the BI Portal?

The NMB Bank Marketing & Brand Communications BI Portal is a web-based business intelligence application that transforms raw banking data into actionable insights. It provides interactive dashboards for analyzing customer accounts, tracking marketing campaigns, monitoring quarterly performance, and identifying business trends.

### 1.2 Who Should Use This Portal?

**Target Users:**
- **Executives:** C-suite and VPs needing high-level KPIs for strategic decisions
- **Managers:** Department heads tracking team performance and campaign results
- **Analysts:** Marketing analysts conducting detailed data analysis
- **Stakeholders:** Board members and consultants viewing summary metrics

### 1.3 What You Can Do

✅ **View Real-Time Data:** Access up-to-date account and customer information  
✅ **Analyze Trends:** Track quarterly performance, churn rates, and activity patterns  
✅ **Monitor Campaigns:** Measure marketing campaign effectiveness  
✅ **Export Reports:** Download data for presentations and further analysis  
✅ **Save Preferences:** Bookmark favorite views and configurations  

### 1.4 System Requirements

**Web Browser:**
- Google Chrome (version 90 or later) - Recommended
- Mozilla Firefox (version 88 or later)
- Microsoft Edge (version 90 or later)
- Safari (version 14 or later)

**Internet Connection:**
- Stable broadband connection (minimum 2 Mbps)
- Corporate VPN if accessing remotely

**Screen Resolution:**
- Minimum: 1366 x 768
- Recommended: 1920 x 1080 or higher

---

## 2. Getting Started

### 2.1 Accessing the Portal

**Step 1: Open Your Web Browser**
- Launch your preferred browser (Chrome recommended)

**Step 2: Navigate to Portal URL**
```
https://[your-portal-url].replit.app
```
- Bookmark this URL for quick access

**Step 3: Log In (Future - Currently No Authentication)**
- Enter your NMB email address
- Enter your password
- Click "Log In"

**First-Time Login:**
- You will be prompted to change your temporary password
- Create a strong password (minimum 12 characters, mix of uppercase, lowercase, numbers, special characters)

### 2.2 Understanding the Interface

**Main Components:**

```
┌────────────────────────────────────────────────────────┐
│ [NMB Logo]                                             │
│────────────────────────────────────────────────────────│
│ [Header Banner with Dashboard Title]                   │
│────────────────────────────────────────────────────────│
│ ┌──────────┐ ┌───────────────────────────────────────┐│
│ │          │ │                                       ││
│ │ Sidebar  │ │   Main Content Area                  ││
│ │ Nav      │ │   (Charts, Tables, Metrics)          ││
│ │          │ │                                       ││
│ │ Pages:   │ │                                       ││
│ │ • Home   │ │                                       ││
│ │ • Exec   │ │                                       ││
│ │ • Email  │ │                                       ││
│ │ • Activity│ │                                       ││
│ │ • Metrics│ │                                       ││
│ │ • Quarter│ │                                       ││
│ │ • Campaign│ │                                       ││
│ └──────────┘ └───────────────────────────────────────┘│
│────────────────────────────────────────────────────────│
│ [Footer: Made with ❤️ by NMB Business Intelligence]   │
└────────────────────────────────────────────────────────┘
```

**1. NMB Logo:** Company branding (top-left)  
**2. Header Banner:** Current dashboard name and description  
**3. Sidebar Navigation:** Quick links to all dashboards  
**4. Main Content:** Interactive charts, tables, and metrics  
**5. Footer:** Portal information and credits  

### 2.3 Navigation Basics

**Switching Dashboards:**
1. Click on sidebar link (e.g., "Executive Summary")
2. Dashboard loads with relevant data
3. Breadcrumb shows current location

**Using Filters:**
1. Locate filter controls (usually at top of page)
2. Select desired criteria (date range, branch, product)
3. Data updates automatically
4. Reset filters using "Clear" or "Reset" button

**Scrolling and Zooming:**
- Scroll down for more content
- Charts support zoom (click and drag)
- Hover over chart elements for details

---

## 3. Dashboard Guide

### 3.1 Home Dashboard

**Purpose:** Portal overview and quick access to all features

**What You See:**
- Welcome message
- Quick statistics (6 dashboards, 4 data sources)
- Dashboard navigation guide
- Data governance information
- Project acknowledgment

**How to Use:**
1. Review dashboard categories (Executive vs Operational)
2. Click "View Data Quality Indicators" to see data freshness
3. Navigate to specific dashboard using sidebar or description links

### 3.2 Executive Summary Dashboard

**Purpose:** High-level KPIs for executive presentations

**Key Metrics:**
- **Total Customers:** 190,560
- **Active Accounts:** 258,709 (99.5% in 90-day window)
- **Avg Products/Customer:** ~1.36 (excluding Account/Card types)
- **Q3 2025 Funded Accounts:** Quarterly performance

**Charts:**
1. **Quarterly Performance Trend:** Line chart showing funded accounts by quarter
2. **Activity Distribution:** Pie chart of active vs inactive accounts
3. **Product Distribution:** Bar chart of top products by volume
4. **Top 10 Products:** Horizontal bar chart

**How to Use:**
- **For Presentations:** Export charts (right-click → Save image)
- **For Analysis:** Hover over data points for exact values
- **For Reports:** Click "Download CSV" button to export data
- **For Drill-Down:** Click on chart segments to filter (where supported)

**Export Options:**
- CSV export (all data)
- Chart images (PNG)

### 3.3 Active Email Accounts Dashboard

**Purpose:** Identify contactable customers for email campaigns

**Key Information:**
- Total accounts with email addresses
- Valid vs placeholder email counts
- Searchable account listings
- Branch and product breakdowns

**How to Use:**

**Step 1: View Email Statistics**
- Review total email counts at top of page
- Note valid vs placeholder distinction

**Step 2: Search for Specific Accounts**
1. Type in search box (account number, name, or email)
2. Results filter as you type
3. Clear search to reset

**Step 3: Filter by Segment**
- Select branch from dropdown
- Select product type from dropdown
- Multiple filters combine (AND logic)

**Step 4: Export Results**
- Click "Download Email List (CSV)"
- Opens/saves file with filtered results
- Use for mail merge or CRM import

**Tips:**
- **Valid Emails:** Excludes "placeholder@nmbz.co.zw" and "none@nmbz.co.zw"
- **Real Contact Count:** ~68,118 customers with actual email addresses
- **Campaign Planning:** Use product/branch filters to target specific segments

### 3.4 Account Activity Dashboard

**Purpose:** Segment accounts by recent transaction activity

**Key Features:**
- **90-Day Threshold:** Configurable activity window (default 90 days)
- **Active Accounts:** 258,709 (99.5%)
- **Inactive Accounts:** 1,172 (0.5%)
- **Drill-Down:** Branch, product, and individual account details

**How to Use:**

**Step 1: Set Activity Threshold**
1. Locate slider at top of page
2. Drag to adjust days (30-180)
3. Data updates automatically
4. Default: 90 days

**Step 2: View Active vs Inactive**
- Review pie chart for overall distribution
- Check metrics for exact counts

**Step 3: Drill Down to Details**

**By Branch:**
1. Scroll to "Branch Breakdown" section
2. Review bar chart
3. Identify branches with high inactive rates

**By Product:**
1. Scroll to "Product Analysis" section
2. See which products have low activity
3. Plan reactivation campaigns

**By Individual Account:**
1. Switch to "Active Accounts" or "Inactive Accounts" tab
2. Search by account number or name
3. View last transaction date
4. Export list for follow-up

**Tips:**
- **Reactivation Campaigns:** Focus on inactive accounts (1,172 opportunities)
- **Activity Patterns:** Most accounts very active (99.5%)
- **Seasonal Trends:** Adjust threshold for seasonal analysis

### 3.5 Customer Metrics Dashboard

**Purpose:** Track customer churn and product holdings

**Key Metrics:**
- **Current Customers:** 190,560
- **Monthly Churn:** Tracked Feb-Oct 2025
- **Retention Trends:** Month-over-month changes
- **Product Holdings:** Distribution across customer base

**How to Use:**

**Step 1: Review Churn Trends**
1. View line chart for monthly customer counts
2. Identify months with highest churn (April, May, June)
3. Note growth months (March, August, September)

**Step 2: Analyze Churn Rates**
- Churn calculated only for customer decreases
- Growth months show 0% churn
- Typical range: 0.2% to 1.8%

**Step 3: Product Holdings Analysis**
- Review "Products per Customer" distribution
- Identify cross-sell opportunities (customers with only 1 product)
- See top product combinations

**Tips:**
- **High Churn Months:** April (-1.83%), May (-1.53%) - investigate causes
- **Retention Success:** Recent months show growth
- **Cross-Sell:** Many customers have only 1-2 products

### 3.6 Quarterly Performance Dashboard

**Purpose:** Track funded accounts Q1-Q3 2025

**Key Metrics:**
- Q1 funded accounts
- Q2 funded accounts
- Q3 funded accounts
- Quarter-over-quarter growth rates

**How to Use:**

**Step 1: View Quarterly Trend**
- Line chart shows funded account growth
- Compare Q1 → Q2 → Q3 performance

**Step 2: Calculate Growth**
- Percentage change displayed for each quarter
- Identify acceleration or deceleration

**Step 3: Branch Comparison**
- Bar chart compares branch performance
- Identify top-performing and underperforming branches

**Step 4: Product Contribution**
- See which products drive funded account growth
- Plan product promotions accordingly

**Export:**
- Download quarterly data for executive presentations
- Use in budget planning and forecasting

### 3.7 Campaign Analysis Dashboard

**Purpose:** Measure non-funded income campaign performance (June-Sept 2025)

**Key Metrics:**
- Campaign participants (accounts and customers)
- Revenue generated (GL-based)
- Branch and product attribution
- Campaign timeline trends

**How to Use:**

**Step 1: Campaign Overview**
- Review total participants
- See revenue contribution
- Check campaign success indicators

**Step 2: Timeline Analysis**
- Monthly trend chart shows campaign momentum
- Identify peak months
- Plan future campaign timing

**Step 3: Geographic Performance**
- Branch-level revenue comparison
- Identify high-performing locations
- Replicate success factors

**Step 4: Product Performance**
- See which products generated most revenue
- Focus marketing on high-performing products

**Tips:**
- **Revenue Attribution:** Links GL accounts to campaign activity
- **Duration:** June-September 2025 (4 months)
- **ROI:** Calculate by comparing revenue to campaign costs

---

## 4. Features and Functions

### 4.1 Interactive Charts

**Hover for Details:**
- Move mouse over chart elements
- Tooltip shows exact values
- Works on all charts

**Zoom and Pan:**
1. Click and drag on chart area to zoom
2. Double-click to reset view
3. Use scroll wheel (on some charts)

**Legend Interaction:**
- Click legend items to toggle visibility
- Useful for comparing specific segments

### 4.2 Data Export

**CSV Export:**
1. Locate "Download CSV" button (usually top-right)
2. Click button
3. File downloads to your browser's default location
4. Open in Excel or other spreadsheet software

**What Gets Exported:**
- Filtered data (if filters applied)
- All columns visible in current view
- Timestamp in filename

**Chart Export:**
1. Right-click on chart
2. Select "Save image as..."
3. Choose location and save as PNG

### 4.3 Search and Filter

**Search Box:**
- Type to filter instantly
- Searches across multiple fields (account number, name, email)
- Case-insensitive
- Clear with "X" button

**Dropdown Filters:**
- Select from available options
- Multiple filters combine (AND logic)
- "All" option to clear filter

**Date Range:**
- Calendar picker for start/end dates
- Apply to specific date fields
- Reset to default range

### 4.4 Bookmarks (Future Feature)

**Save Current View:**
1. Configure dashboard with desired filters
2. Click "Bookmark This View"
3. Enter bookmark name
4. Save

**Load Bookmark:**
1. Click "My Bookmarks" dropdown
2. Select saved bookmark
3. Dashboard loads with saved configuration

### 4.5 Favorites (Future Feature)

**Mark as Favorite:**
1. Find account/customer/product of interest
2. Click star icon
3. Access later from "My Favorites"

**View Favorites:**
1. Click "Favorites" in navigation
2. See all favorited items
3. Quick access to important data

### 4.6 Notifications (Future Feature)

**Bell Icon:**
- Shows unread notification count
- Click to view notifications

**Notification Types:**
- System updates
- Data refresh alerts
- Important KPI changes
- Scheduled reports

---

## 5. Authentication and Access

### 5.1 User Roles and Permissions

**Level 1: Executive**
- **Access:** All dashboards
- **Permissions:** View, Export (full), Admin functions
- **Users:** C-suite, VPs

**Level 2: Manager**
- **Access:** All dashboards
- **Permissions:** View, Limited export
- **Users:** Department heads, Senior managers

**Level 3: Analyst**
- **Access:** Operational dashboards
- **Permissions:** View only (no export)
- **Users:** Marketing analysts, BI team

**Level 4: Read-Only**
- **Access:** Selected dashboards
- **Permissions:** View only (no drill-down)
- **Users:** Junior staff, Contractors

**Level 5: External Stakeholder**
- **Access:** Executive Summary (limited KPIs)
- **Permissions:** View high-level metrics only
- **Users:** Board members, External consultants

### 5.2 Password Management (Future)

**Password Requirements:**
- Minimum 12 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character (!@#$%^&*)

**Change Password:**
1. Click profile icon → "Settings"
2. Select "Change Password"
3. Enter current password
4. Enter new password (twice)
5. Click "Update Password"

**Forgot Password:**
1. Click "Forgot Password" on login page
2. Enter your email address
3. Check email for reset link
4. Click link (valid for 1 hour)
5. Set new password

### 5.3 Session Management (Future)

**Session Duration:**
- 8 hours of inactivity
- Auto-logout for security

**Active Session:**
- Renewed on each interaction
- Warning before timeout

**Logout:**
1. Click profile icon
2. Select "Logout"
3. Redirected to login page

---

## 6. Troubleshooting

### 6.1 Common Issues

**Issue: Page Won't Load**
- **Solution:**
  1. Check internet connection
  2. Refresh browser (Ctrl+R or Cmd+R)
  3. Clear browser cache
  4. Try different browser

**Issue: Data Looks Incorrect**
- **Solution:**
  1. Check date range filters
  2. Verify branch/product filters
  3. Refresh page
  4. Contact support if persists

**Issue: Charts Not Displaying**
- **Solution:**
  1. Enable JavaScript in browser
  2. Disable ad blockers for this site
  3. Update browser to latest version
  4. Clear browser cache

**Issue: Export Not Working**
- **Solution:**
  1. Check browser pop-up blocker
  2. Verify download folder permissions
  3. Try right-click → "Save Link As"
  4. Contact support if persists

**Issue: Slow Performance**
- **Solution:**
  1. Close unused browser tabs
  2. Check internet speed (minimum 2 Mbps)
  3. Use Chrome browser (best performance)
  4. Reduce number of active filters

**Issue: Can't Access Certain Dashboards**
- **Solution:**
  1. Verify your user role/permissions
  2. Contact your manager for access request
  3. Contact support if access should be granted

### 6.2 Browser-Specific Tips

**Chrome:**
- Clear cache: Settings → Privacy → Clear browsing data
- Disable extensions: Menu → More tools → Extensions

**Firefox:**
- Clear cache: Options → Privacy → Clear Data
- Disable extensions: Menu → Add-ons → Extensions

**Safari:**
- Clear cache: Safari → Clear History
- Enable JavaScript: Preferences → Security

**Edge:**
- Clear cache: Settings → Privacy → Choose what to clear
- Disable extensions: Menu → Extensions

---

## 7. FAQ

**Q: How often is data updated?**  
A: Currently, data is updated when CSV files are uploaded (daily). Future versions will have automated real-time updates.

**Q: Can I access this portal from my phone?**  
A: The portal is optimized for desktop/laptop screens. Mobile access is possible but not recommended for full functionality.

**Q: How do I request access to additional dashboards?**  
A: Contact your department head or the BI team at bi@nmbz.co.zw with your request.

**Q: Can I customize the dashboards?**  
A: Currently, dashboards are standardized. User customization (bookmarks, favorites) will be available in future versions.

**Q: What does "90-day activity" mean?**  
A: It means accounts that have had at least one transaction in the last 90 days. You can adjust this threshold using the slider.

**Q: Why are some email addresses marked as "placeholder"?**  
A: These are system-generated placeholder emails (e.g., "placeholder@nmbz.co.zw") that don't represent real customer contact information.

**Q: How is churn calculated?**  
A: Churn is the month-over-month decrease in customer count. Growth months show 0% churn.

**Q: What's the difference between funded and non-funded accounts?**  
A: Funded accounts have positive balances and recent transactions. Non-funded accounts may be inactive or have zero balance.

**Q: Can I share dashboard links with colleagues?**  
A: Yes, you can share the portal URL. In future versions with authentication, users will need their own login credentials.

**Q: How do I report a bug or suggest a feature?**  
A: Contact the BI team at bi@nmbz.co.zw or use the feedback form (future feature).

---

## 8. Support

### 8.1 Contact Information

**BI Team:**
- **Email:** bi@nmbz.co.zw
- **Phone:** [Internal Extension]
- **Office:** IT Department, NMB Head Office

**Support Hours:**
- Monday - Friday: 8:00 AM - 5:00 PM CAT
- Response Time: Within 1 business day

### 8.2 Support Levels

**Level 1: User Support**
- Login issues
- Navigation questions
- Basic troubleshooting
- Feature questions

**Level 2: Technical Support**
- Data discrepancies
- Export issues
- Performance problems
- Browser compatibility

**Level 3: Development Support**
- Bug fixes
- Feature enhancements
- System improvements
- Integration requests

### 8.3 Getting Help

**Self-Service:**
1. Check this user manual
2. Review FAQ section
3. Try troubleshooting steps

**Email Support:**
1. Send detailed description to bi@nmbz.co.zw
2. Include screenshots if applicable
3. Mention your browser and OS
4. Await response (1 business day)

**Training Sessions:**
- Group training available on request
- Contact BI team to schedule
- Customized to department needs

---

## Appendix A: Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+R / Cmd+R | Refresh page |
| Ctrl+F / Cmd+F | Find on page |
| Ctrl+P / Cmd+P | Print page |
| Esc | Clear search/close dialog |
| Tab | Navigate between form fields |

---

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| **Active Account** | Account with transaction in last 90 days (configurable) |
| **Churn** | Customer attrition (lost customers) |
| **CIF** | Customer Information File |
| **Funded Account** | Account with positive balance |
| **GL** | General Ledger |
| **KPI** | Key Performance Indicator |
| **Placeholder Email** | System-generated email (not real contact) |
| **Product Holdings** | Number of different products a customer owns |
| **Quarter** | 3-month period (Q1=Jan-Mar, Q2=Apr-Jun, Q3=Jul-Sep, Q4=Oct-Dec) |

---

**Document Version:** 1.0  
**Publication Date:** October 21, 2025  
**Prepared By:** Terence Tachiona, NMB Business Intelligence  
**Review Schedule:** Quarterly  

---

*For the latest version of this manual, contact bi@nmbz.co.zw*
