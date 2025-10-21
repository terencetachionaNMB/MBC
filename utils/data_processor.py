import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataProcessor:
    """
    Data processing utilities for transforming and preparing data for visualizations.
    """
    
    def __init__(self, data_loader):
        self.loader = data_loader
        self.accounts_df = data_loader.get_accounts_data()
        self.product_df = data_loader.get_product_data()
    
    def get_active_email_accounts(self):
        """
        Get accounts with email addresses that are currently active.
        Returns: DataFrame with account details and email addresses
        """
        if self.accounts_df is None:
            return pd.DataFrame()
        
        # Filter for active accounts (not closed)
        df = self.accounts_df.copy()
        
        # Check if closure date column exists and filter
        if 'ACNTS_CLOSURE_DATE' in df.columns:
            df = df[df['ACNTS_CLOSURE_DATE'].isna()]
        
        # Check if status column exists and filter for active
        if 'ACNTS_CREATION_STATUS' in df.columns:
            df = df[df['ACNTS_CREATION_STATUS'].str.upper() == 'ACTIVE']
        
        # For this example, we'll assume email is stored in a field
        # Since the data dictionary doesn't explicitly show email field,
        # we'd need the actual data structure
        
        return df
    
    def get_account_activity_segments(self, days_threshold=90):
        """
        Segment accounts by activity (last transaction date).
        
        Args:
            days_threshold: Number of days to consider account inactive
            
        Returns: DataFrame with activity segments
        """
        if self.accounts_df is None:
            return pd.DataFrame(), pd.DataFrame()
        
        df = self.accounts_df.copy()
        
        # Calculate days since last transaction
        if 'ACNTS_LAST_TRAN_DATE' in df.columns:
            today = pd.Timestamp.now()
            df['days_since_last_txn'] = (today - df['ACNTS_LAST_TRAN_DATE']).dt.days
            
            # Create activity segment
            df['activity_status'] = df['days_since_last_txn'].apply(
                lambda x: 'Active' if pd.notna(x) and x <= days_threshold else 'Inactive'
            )
            
            active_df = df[df['activity_status'] == 'Active']
            inactive_df = df[df['activity_status'] == 'Inactive']
            
            return active_df, inactive_df
        
        return pd.DataFrame(), pd.DataFrame()
    
    def get_unique_customer_count(self):
        """
        Get count of unique customers (not accounts).
        Returns: int - number of unique customers
        """
        if self.accounts_df is None:
            return 0
        
        if 'ACNTS_CLIENT_NUM' in self.accounts_df.columns:
            return self.accounts_df['ACNTS_CLIENT_NUM'].nunique()
        
        return 0
    
    def get_avg_products_per_customer(self):
        """
        Calculate average number of products per customer.
        Excludes Account and Card product types as specified.
        
        Returns: float - average products per customer
        """
        if self.accounts_df is None or self.product_df is None:
            return 0
        
        df = self.accounts_df.copy()
        
        # Filter out Account and Card product types
        if 'Product Class' in df.columns:
            df = df[~df['Product Class'].isin(['Account', 'Card', 'ACCOUNT', 'CARD'])]
        
        if 'ACNTS_CLIENT_NUM' in df.columns and 'ACNTS_PROD_CODE' in df.columns:
            # Count distinct products per customer
            products_per_customer = df.groupby('ACNTS_CLIENT_NUM')['ACNTS_PROD_CODE'].nunique()
            return products_per_customer.mean()
        
        return 0
    
    def calculate_monthly_churn_rate(self):
        """
        Calculate monthly churn rate (lost customers month-on-month).
        Uses actual churn data if available, otherwise calculates from closure dates.
        
        Returns: DataFrame with monthly churn rates
        """
        # Try to get actual churn data first
        churn_data = self.loader.get_churn_data()
        if churn_data is not None and len(churn_data) > 0:
            # Use actual churn data from the system
            result = churn_data.copy()
            
            # Ensure we have required columns
            if 'COMMON_CUSTOMERS' in result.columns and 'TRAN_MONTH' in result.columns:
                # Create month column if not exists
                if 'month' not in result.columns:
                    result['month'] = pd.to_datetime('2025-' + result['TRAN_MONTH'].astype(str) + '-01')
                
                # Sort by month to ensure proper sequence
                result = result.sort_values('month')
                
                # Calculate churned customers as the decrease from previous month
                # COMMON_CUSTOMERS shows active customers each month
                result['prev_month_customers'] = result['COMMON_CUSTOMERS'].shift(1)
                result['customer_change'] = result['prev_month_customers'] - result['COMMON_CUSTOMERS']
                
                # Churn is only when customers decrease (positive change = lost customers)
                # If customers grow (negative change), set churn to 0
                result['churned_customers'] = result['customer_change'].apply(lambda x: max(0, x) if pd.notna(x) else 0)
                
                # Calculate churn rate as percentage of previous month's base
                # Only calculate when we have previous month data
                result['churn_rate'] = result.apply(
                    lambda row: (row['churned_customers'] / row['prev_month_customers']) * 100 
                    if pd.notna(row['prev_month_customers']) and row['prev_month_customers'] > 0 
                    else 0, 
                    axis=1
                )
                
                # Track growth separately for visibility
                result['customer_growth'] = result['customer_change'].apply(lambda x: max(0, -x) if pd.notna(x) else 0)
                
                return result[['month', 'churned_customers', 'churn_rate', 'COMMON_CUSTOMERS']].rename(
                    columns={'COMMON_CUSTOMERS': 'active_customers'}
                )
        
        # Fallback: Calculate from account closure dates
        if self.accounts_df is None:
            return pd.DataFrame()
        
        df = self.accounts_df.copy()
        
        if 'ACNTS_CLOSURE_DATE' in df.columns and 'ACNTS_CLIENT_NUM' in df.columns:
            # Filter closed accounts
            closed = df[df['ACNTS_CLOSURE_DATE'].notna()].copy()
            
            # Extract month from closure date
            closed['closure_month'] = closed['ACNTS_CLOSURE_DATE'].dt.to_period('M')
            
            # Count unique customers who closed accounts each month
            churned_customers = closed.groupby('closure_month')['ACNTS_CLIENT_NUM'].nunique().reset_index()
            churned_customers.columns = ['month', 'churned_customers']
            
            # Get total active customers at start of each month
            total_customers = self.get_unique_customer_count()
            
            # Calculate churn rate
            churned_customers['churn_rate'] = (churned_customers['churned_customers'] / total_customers) * 100
            
            return churned_customers
        
        return pd.DataFrame()
    
    def get_quarterly_funded_accounts(self, year=2025):
        """
        Get funded (active) accounts count by quarter for specified year.
        
        Args:
            year: Year to analyze (default 2025)
            
        Returns: DataFrame with quarterly counts
        """
        if self.accounts_df is None:
            return pd.DataFrame()
        
        df = self.accounts_df.copy()
        
        # Filter for active/funded accounts (has transactions)
        if 'ACNTS_LAST_TRAN_DATE' not in df.columns:
            return pd.DataFrame()
        
        df = df[df['ACNTS_LAST_TRAN_DATE'].notna()].copy()
        
        # Create quarter periods for the year
        quarters = []
        for q in range(1, 4):  # Q1, Q2, Q3
            q_start = pd.Timestamp(f'{year}-{(q-1)*3+1:02d}-01')
            q_end = pd.Timestamp(f'{year}-{q*3:02d}-01') + pd.offsets.MonthEnd(0)
            
            # Count accounts with transactions in this quarter
            # An account is "funded" if it had any transaction during the quarter
            active_in_q = df[
                (df['ACNTS_LAST_TRAN_DATE'] >= q_start) &
                (df['ACNTS_LAST_TRAN_DATE'] <= q_end)
            ]
            
            quarters.append({
                'quarter': f'Q{q} {year}',
                'funded_accounts': len(active_in_q),
                'period_start': q_start,
                'period_end': q_end
            })
        
        return pd.DataFrame(quarters)
    
    def get_campaign_revenue_analysis(self, campaign_start='2025-06-01', campaign_end='2025-09-30'):
        """
        Analyze revenue trends during campaign period.
        Focus on non-funded income campaign (June-September 2025).
        
        Args:
            campaign_start: Campaign start date
            campaign_end: Campaign end date
            
        Returns: DataFrame with monthly revenue trends
        """
        # This would require transaction/revenue data which isn't in the provided schema
        # We'll create a structure that can be populated when transaction data is available
        
        campaign_start = pd.Timestamp(campaign_start)
        campaign_end = pd.Timestamp(campaign_end)
        
        # Generate monthly periods
        months = pd.period_range(start=campaign_start, end=campaign_end, freq='M')
        
        # Placeholder structure - would be populated with actual GL transaction data
        revenue_data = []
        for month in months:
            revenue_data.append({
                'month': month.to_timestamp(),
                'month_name': month.strftime('%B %Y'),
                'revenue': 0,  # Would be calculated from GL transactions
                'non_funded_income': 0  # Commission, fees, etc.
            })
        
        df = pd.DataFrame(revenue_data)
        
        # Calculate month-on-month change
        if len(df) > 0:
            df['mom_change'] = df['revenue'].pct_change() * 100
            df['mom_change_abs'] = df['revenue'].diff()
        
        return df
    
    def get_account_balances_summary(self):
        """
        Get summary of account balances by product type and currency.
        Note: Actual balance data not in provided schema, structure for future use.
        
        Returns: DataFrame with balance summaries
        """
        if self.accounts_df is None:
            return pd.DataFrame()
        
        df = self.accounts_df.copy()
        
        # Group by product and currency
        if 'ACNTS_PROD_CODE' in df.columns and 'ACNTS_CURR_CODE' in df.columns:
            summary = df.groupby(['ACNTS_PROD_CODE', 'ACNTS_CURR_CODE']).agg({
                'ACNTS_ACCOUNT_NUMBER': 'count'
            }).reset_index()
            summary.columns = ['product_code', 'currency', 'account_count']
            
            # Merge with product names
            if self.product_df is not None and 'Product Code' in self.product_df.columns:
                summary = summary.merge(
                    self.product_df[['Product Code', 'Product Name']],
                    left_on='product_code',
                    right_on='Product Code',
                    how='left'
                )
            
            return summary
        
        return pd.DataFrame()
    
    def get_branch_performance(self):
        """
        Get account statistics by branch.
        
        Returns: DataFrame with branch-level metrics
        """
        if self.accounts_df is None:
            return pd.DataFrame()
        
        df = self.accounts_df.copy()
        
        if 'ACNTS_BRN_CODE' in df.columns:
            branch_stats = df.groupby('ACNTS_BRN_CODE').agg({
                'ACNTS_ACCOUNT_NUMBER': 'count',
                'ACNTS_CLIENT_NUM': 'nunique'
            }).reset_index()
            
            branch_stats.columns = ['branch_code', 'total_accounts', 'unique_customers']
            
            return branch_stats
        
        return pd.DataFrame()
