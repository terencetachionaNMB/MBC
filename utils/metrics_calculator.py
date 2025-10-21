import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MetricsCalculator:
    """
    Advanced metrics and KPI calculations for the BI Portal.
    """
    
    def __init__(self, data_processor):
        self.processor = data_processor
        self.accounts_df = data_processor.accounts_df
    
    def calculate_growth_rate(self, current_value, previous_value):
        """Calculate growth rate percentage"""
        if previous_value == 0 or pd.isna(previous_value):
            return 0
        return ((current_value - previous_value) / previous_value) * 100
    
    def calculate_compound_growth_rate(self, values, periods):
        """Calculate CAGR (Compound Annual Growth Rate)"""
        if len(values) < 2 or periods == 0:
            return 0
        
        start_value = values[0]
        end_value = values[-1]
        
        if start_value <= 0:
            return 0
        
        return (((end_value / start_value) ** (1 / periods)) - 1) * 100
    
    def calculate_customer_lifetime_value(self):
        """
        Calculate estimated customer lifetime value.
        This is a simplified calculation based on account tenure.
        """
        if self.accounts_df is None:
            return 0
        
        df = self.accounts_df.copy()
        
        if 'ACNTS_OPENING_DATE' in df.columns and 'ACNTS_CLIENT_NUM' in df.columns:
            today = pd.Timestamp.now()
            
            # Calculate account age in days
            df['account_age_days'] = (today - df['ACNTS_OPENING_DATE']).dt.days
            
            # Average account age per customer
            avg_age = df.groupby('ACNTS_CLIENT_NUM')['account_age_days'].mean().mean()
            
            return avg_age / 365.25  # Convert to years
        
        return 0
    
    def calculate_retention_rate(self, period_start, period_end):
        """
        Calculate customer retention rate for a period.
        
        Args:
            period_start: Start of period (datetime)
            period_end: End of period (datetime)
            
        Returns: float - retention rate percentage
        """
        if self.accounts_df is None:
            return 0
        
        df = self.accounts_df.copy()
        
        if 'ACNTS_OPENING_DATE' not in df.columns or 'ACNTS_CLOSURE_DATE' not in df.columns:
            return 0
        
        # Customers at start of period
        customers_start = df[
            (df['ACNTS_OPENING_DATE'] < period_start) &
            ((df['ACNTS_CLOSURE_DATE'].isna()) | (df['ACNTS_CLOSURE_DATE'] >= period_start))
        ]['ACNTS_CLIENT_NUM'].nunique()
        
        # Customers retained at end of period
        customers_retained = df[
            (df['ACNTS_OPENING_DATE'] < period_start) &
            ((df['ACNTS_CLOSURE_DATE'].isna()) | (df['ACNTS_CLOSURE_DATE'] >= period_end))
        ]['ACNTS_CLIENT_NUM'].nunique()
        
        if customers_start == 0:
            return 0
        
        return (customers_retained / customers_start) * 100
    
    def calculate_product_penetration(self):
        """
        Calculate product penetration rates.
        Returns: DataFrame with penetration rates per product
        """
        if self.accounts_df is None:
            return pd.DataFrame()
        
        df = self.accounts_df.copy()
        
        total_customers = df['ACNTS_CLIENT_NUM'].nunique() if 'ACNTS_CLIENT_NUM' in df.columns else 0
        
        if total_customers == 0:
            return pd.DataFrame()
        
        if 'ACNTS_PROD_CODE' in df.columns and 'ACNTS_CLIENT_NUM' in df.columns:
            product_penetration = df.groupby('ACNTS_PROD_CODE').agg({
                'ACNTS_CLIENT_NUM': 'nunique',
                'ACNTS_ACCOUNT_NUMBER': 'count'
            }).reset_index()
            
            product_penetration.columns = ['product_code', 'unique_customers', 'total_accounts']
            product_penetration['penetration_rate'] = (product_penetration['unique_customers'] / total_customers) * 100
            
            # Merge with product names
            if self.processor.product_df is not None:
                product_penetration = product_penetration.merge(
                    self.processor.product_df[['Product Code', 'Product Name', 'Product Class']],
                    left_on='product_code',
                    right_on='Product Code',
                    how='left'
                )
            
            return product_penetration.sort_values('penetration_rate', ascending=False)
        
        return pd.DataFrame()
    
    def calculate_account_concentration(self):
        """
        Calculate concentration metrics (e.g., top 10% customers' share).
        Returns: dict with concentration metrics
        """
        if self.accounts_df is None:
            return {}
        
        df = self.accounts_df.copy()
        
        if 'ACNTS_CLIENT_NUM' not in df.columns:
            return {}
        
        # Count accounts per customer
        accounts_per_customer = df.groupby('ACNTS_CLIENT_NUM').size().reset_index(name='account_count')
        accounts_per_customer = accounts_per_customer.sort_values('account_count', ascending=False)
        
        total_accounts = len(df)
        total_customers = len(accounts_per_customer)
        
        # Top 10% customers
        top_10_pct_count = int(total_customers * 0.1)
        top_10_pct_accounts = accounts_per_customer.head(top_10_pct_count)['account_count'].sum()
        
        # Top 20% customers
        top_20_pct_count = int(total_customers * 0.2)
        top_20_pct_accounts = accounts_per_customer.head(top_20_pct_count)['account_count'].sum()
        
        return {
            'total_customers': total_customers,
            'total_accounts': total_accounts,
            'top_10_pct_customers': top_10_pct_count,
            'top_10_pct_accounts': top_10_pct_accounts,
            'top_10_pct_share': (top_10_pct_accounts / total_accounts) * 100,
            'top_20_pct_customers': top_20_pct_count,
            'top_20_pct_accounts': top_20_pct_accounts,
            'top_20_pct_share': (top_20_pct_accounts / total_accounts) * 100
        }
    
    def calculate_channel_adoption(self):
        """
        Calculate channel adoption rates (Internet Banking, Mobile, ATM, etc.).
        Returns: DataFrame with channel metrics
        """
        if self.accounts_df is None:
            return pd.DataFrame()
        
        df = self.accounts_df.copy()
        
        total_accounts = len(df)
        
        channel_columns = {
            'ACNTS_INET_OPERN': 'Internet Banking',
            'ACNTS_MBLBNK_OPERN': 'Mobile Banking',
            'ACNTS_ATM_OPERN': 'ATM',
            'ACNTS_SMS_OPERN': 'SMS Banking',
            'ACNTS_CALL_CENTER_OPERN': 'Call Center',
            'ACNTS_TELLER_OPERN': 'Teller/Branch'
        }
        
        channel_stats = []
        
        for col, channel_name in channel_columns.items():
            if col in df.columns:
                enabled_count = df[df[col] == 'Y'].shape[0]
                adoption_rate = (enabled_count / total_accounts) * 100 if total_accounts > 0 else 0
                
                channel_stats.append({
                    'channel': channel_name,
                    'enabled_accounts': enabled_count,
                    'adoption_rate': adoption_rate
                })
        
        return pd.DataFrame(channel_stats).sort_values('adoption_rate', ascending=False)
    
    def calculate_dormancy_metrics(self):
        """
        Calculate dormancy and inoperative account metrics.
        Returns: dict with dormancy statistics
        """
        if self.accounts_df is None:
            return {}
        
        df = self.accounts_df.copy()
        
        total_accounts = len(df)
        
        metrics = {
            'total_accounts': total_accounts
        }
        
        if 'ACNTS_DORMANT_ACNT' in df.columns:
            dormant_count = df[df['ACNTS_DORMANT_ACNT'] == 'Y'].shape[0]
            metrics['dormant_accounts'] = dormant_count
            metrics['dormant_rate'] = (dormant_count / total_accounts) * 100 if total_accounts > 0 else 0
        
        if 'ACNTS_INOP_ACNT' in df.columns:
            inop_count = df[df['ACNTS_INOP_ACNT'] == 'Y'].shape[0]
            metrics['inoperative_accounts'] = inop_count
            metrics['inoperative_rate'] = (inop_count / total_accounts) * 100 if total_accounts > 0 else 0
        
        return metrics
