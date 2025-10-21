import pandas as pd
import streamlit as st
from pathlib import Path
import glob
from datetime import datetime

class DataLoader:
    """
    Centralized data loading utility for the BI Portal.
    Loads all CSV files and creates the data model.
    """
    
    def __init__(self):
        self.data_folder = Path("data")
        self.accounts_df = None
        self.sector_df = None
        self.gl_df = None
        self.product_df = None
        self.product_volume_df = None
        self.revenue_df = None
        self.churn_df = None
        self.transactions_df = None
        
        self._load_all_data()
        self._create_data_model()
    
    def _find_csv_file(self, pattern):
        """Find CSV file matching pattern in data folder"""
        files = glob.glob(str(self.data_folder / pattern))
        if files:
            return files[0]
        return None
    
    def _parse_date(self, date_str):
        """Parse dates in various formats"""
        if pd.isna(date_str) or date_str == '':
            return None
        
        # Try different date formats
        formats = [
            '%B %d, %Y',  # October 17, 2025
            '%d/%m/%Y',
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d-%m-%Y',
            '%Y/%m/%d'
        ]
        
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        
        # If all formats fail, try pandas auto-parsing
        try:
            return pd.to_datetime(date_str)
        except:
            return None
    
    def _clean_numeric(self, value_str):
        """Clean numeric values that may have commas"""
        if pd.isna(value_str) or value_str == '':
            return None
        try:
            # Remove commas and convert to float
            if isinstance(value_str, str):
                return float(value_str.replace(',', ''))
            return float(value_str)
        except:
            return None
    
    def _load_accounts_data(self):
        """Load accounts data from actual banking system extract"""
        # Load data dictionary for reference
        dict_path = self._find_csv_file("*accounts_datadictionary*.csv")
        if dict_path:
            self.accounts_schema = pd.read_csv(dict_path)
            st.session_state['accounts_schema'] = self.accounts_schema
        
        # Load actual accounts data
        accounts_data_path = self._find_csv_file("accounts_data.csv")
        if accounts_data_path:
            # Read CSV - use low_memory=False to avoid dtype warnings
            df = pd.read_csv(accounts_data_path, low_memory=False)
            
            # Parse date columns using vectorized operations (MUCH faster than apply)
            date_columns = [
                'ACNTS_LAST_TRAN_DATE', 'ACNTS_NONSYS_LAST_DATE', 
                'INDCLIENT_BIRTH_DATE', 'ACNTS_OPENING_DATE',
                'ACNTS_CLOSURE_DATE'
            ]
            
            for col in date_columns:
                if col in df.columns:
                    # Save original before parsing
                    original = df[col].copy()
                    # Try common format first (fastest path)
                    df[col] = pd.to_datetime(df[col], format='%B %d, %Y', errors='coerce')
                    # Fallback: for NaT values, try general parsing on original data
                    nat_mask = df[col].isna() & original.notna()
                    if nat_mask.any():
                        df.loc[nat_mask, col] = pd.to_datetime(original[nat_mask], errors='coerce')
            
            # Clean numeric columns - vectorized (MUCH faster than apply)
            numeric_columns = [
                'BASE_CURR_BAL', 'LOCAL_CURR_BAL'
            ]
            
            for col in numeric_columns:
                if col in df.columns:
                    # Remove commas and convert to numeric
                    if df[col].dtype == 'object':
                        df[col] = df[col].str.replace(',', '')
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # ACNTS_CLIENT_NUM should stay as-is (it's already numeric in the data)
            if 'ACNTS_CLIENT_NUM' in df.columns:
                df['ACNTS_CLIENT_NUM'] = pd.to_numeric(df['ACNTS_CLIENT_NUM'], errors='coerce')
            
            # Map column names to standardized names for compatibility
            column_mapping = {
                'ACCOUNT_NUMBER': 'ACNTS_ACCOUNT_NUMBER',
                'ACNTBAL_CURR_CODE': 'ACNTS_CURR_CODE',
                'PRODUCT_NAME': 'Product Name',
                'ACCOUNT_NAME': 'ACNTS_AC_NAME1',
                'CLIENTS_TYPE_FLG': 'ACNTS_CLIENT_TYPE',
                'INDCLIENT_EMAIL_ADDR1': 'ACNTS_EMAIL'
            }
            
            # Rename columns if they exist
            df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
            
            # Add derived columns
            df['ACNTS_CREATION_STATUS'] = 'ACTIVE'  # All records are active accounts
            
            # Add digital channel flags based on activity
            df['ACNTS_INET_OPERN'] = 'Y'  # Assume all have internet banking
            df['ACNTS_ATM_OPERN'] = 'Y'
            df['ACNTS_SMS_OPERN'] = 'Y'
            df['ACNTS_CALL_CENTER_OPERN'] = 'Y'
            df['ACNTS_TELLER_OPERN'] = 'Y'
            
            self.accounts_df = df
        else:
            st.warning("⚠️ Accounts data file not found. Please ensure accounts_data.csv is in the data folder.")
            self.accounts_df = None
    
    def _load_sector_classification(self):
        """Load RBZ Sector Classification lookup"""
        file_path = self._find_csv_file("*RBZ SECTOR CLASSIFICATION*.csv")
        
        if file_path:
            self.sector_df = pd.read_csv(file_path)
            # Clean column names
            self.sector_df.columns = self.sector_df.columns.str.strip()
        else:
            st.warning("⚠️ RBZ Sector Classification file not found.")
            self.sector_df = None
    
    def _load_gl_categories(self):
        """Load GL Category lookup table"""
        file_path = self._find_csv_file("*GL CATEGORY LOOKUP*.csv")
        
        if file_path:
            self.gl_df = pd.read_csv(file_path)
            # Clean column names
            self.gl_df.columns = self.gl_df.columns.str.strip()
            
            # Parse date columns using vectorized operations
            date_cols = ['Gl Date Of Opening', 'Gl Closure Date', 'Gl Entd On', 
                        'Gl Last Mod On', 'Gl Auth On']
            for col in date_cols:
                if col in self.gl_df.columns:
                    self.gl_df[col] = pd.to_datetime(self.gl_df[col], errors='coerce')
        else:
            st.warning("⚠️ GL Category lookup file not found.")
            self.gl_df = None
    
    def _load_product_types(self):
        """Load Product Type lookup table"""
        file_path = self._find_csv_file("*PRODUCT TYPE LOOKUP*.csv")
        
        if file_path:
            self.product_df = pd.read_csv(file_path)
            # Clean column names
            self.product_df.columns = self.product_df.columns.str.strip()
        else:
            st.warning("⚠️ Product Type lookup file not found.")
            self.product_df = None
    
    def _load_product_volume(self):
        """Load product volume summary data"""
        file_path = self._find_csv_file("product_volume.csv")
        if file_path:
            df = pd.read_csv(file_path)
            # Clean numeric columns using vectorized operations
            for col in ['TOTAL_ACCOUNTS', 'TOTAL_BASE_CURR_BAL', 'TOTAL_LOCAL_CURR_BAL']:
                if col in df.columns:
                    if df[col].dtype == 'object':
                        df[col] = df[col].str.replace(',', '')
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            self.product_volume_df = df
        else:
            self.product_volume_df = None
    
    def _load_revenue_data(self):
        """Load GL revenue data"""
        file_path = self._find_csv_file("revenue_gls.csv")
        if file_path:
            df = pd.read_csv(file_path)
            # Clean numeric columns using vectorized operations
            if 'SUM(GLBALH_AC_BAL)' in df.columns:
                if df['SUM(GLBALH_AC_BAL)'].dtype == 'object':
                    df['SUM(GLBALH_AC_BAL)'] = df['SUM(GLBALH_AC_BAL)'].str.replace(',', '')
                df['SUM(GLBALH_AC_BAL)'] = pd.to_numeric(df['SUM(GLBALH_AC_BAL)'], errors='coerce')
            self.revenue_df = df
        else:
            self.revenue_df = None
    
    def _load_churn_data(self):
        """Load customer churn data"""
        file_path = self._find_csv_file("churn_customers.csv")
        if file_path:
            df = pd.read_csv(file_path)
            # Clean numeric columns using vectorized operations
            if 'COMMON_CUSTOMERS' in df.columns:
                if df['COMMON_CUSTOMERS'].dtype == 'object':
                    df['COMMON_CUSTOMERS'] = df['COMMON_CUSTOMERS'].str.replace(',', '')
                df['COMMON_CUSTOMERS'] = pd.to_numeric(df['COMMON_CUSTOMERS'], errors='coerce')
            # Parse month if needed
            if 'TRAN_MONTH' in df.columns:
                df['month'] = pd.to_datetime('2025-' + df['TRAN_MONTH'].astype(str) + '-01')
            self.churn_df = df
        else:
            self.churn_df = None
    
    def _load_transactions(self):
        """Load transaction data"""
        file_path = self._find_csv_file("transactions.csv")
        if file_path:
            # Only load if file size is manageable
            import os
            file_size = os.path.getsize(file_path)
            if file_size < 100 * 1024 * 1024:  # Less than 100MB
                df = pd.read_csv(file_path, thousands=',')
                self.transactions_df = df
            else:
                # File too large, skip for now
                self.transactions_df = None
        else:
            self.transactions_df = None
    
    def _load_all_data(self):
        """Load all data sources"""
        self._load_accounts_data()
        self._load_sector_classification()
        self._load_gl_categories()
        self._load_product_types()
        self._load_product_volume()
        self._load_revenue_data()
        self._load_churn_data()
        self._load_transactions()
    
    def _create_data_model(self):
        """Create relationships between tables"""
        if self.accounts_df is not None and self.product_df is not None:
            # Merge accounts with product information if not already present
            if 'Product Name' not in self.accounts_df.columns and 'ACNTS_PROD_CODE' in self.accounts_df.columns:
                # Clean product codes - remove commas
                self.accounts_df['ACNTS_PROD_CODE'] = self.accounts_df['ACNTS_PROD_CODE'].apply(self._clean_numeric)
                self.product_df['Product Code'] = self.product_df['Product Code'].apply(self._clean_numeric)
                
                # Merge with product information
                self.accounts_df = self.accounts_df.merge(
                    self.product_df[['Product Code', 'Product Name', 'Product Class', 'Product Group Code']],
                    left_on='ACNTS_PROD_CODE',
                    right_on='Product Code',
                    how='left',
                    suffixes=('', '_product')
                )
        
        if self.accounts_df is not None and self.sector_df is not None:
            # Add sector classification based on account name
            # This is a simplified approach - actual matching would require customer master data
            pass
    
    def get_accounts_data(self):
        """Get accounts dataframe"""
        return self.accounts_df
    
    def get_sector_data(self):
        """Get sector classification dataframe"""
        return self.sector_df
    
    def get_gl_data(self):
        """Get GL categories dataframe - returns revenue GL data if available"""
        return self.revenue_df if self.revenue_df is not None else self.gl_df
    
    def get_product_data(self):
        """Get product types dataframe"""
        return self.product_df
    
    def get_product_volume(self):
        """Get product volume summary"""
        return self.product_volume_df
    
    def get_revenue_data(self):
        """Get revenue GL data"""
        return self.revenue_df
    
    def get_churn_data(self):
        """Get churn customer data"""
        return self.churn_df
    
    def get_transactions(self):
        """Get transactions dataframe"""
        return self.transactions_df
    
    def get_data_summary(self):
        """Get summary statistics of loaded data"""
        summary = {
            'accounts_loaded': self.accounts_df is not None,
            'accounts_count': len(self.accounts_df) if self.accounts_df is not None else 0,
            'sector_loaded': self.sector_df is not None,
            'sector_count': len(self.sector_df) if self.sector_df is not None else 0,
            'gl_loaded': self.gl_df is not None,
            'gl_count': len(self.gl_df) if self.gl_df is not None else 0,
            'product_loaded': self.product_df is not None,
            'product_count': len(self.product_df) if self.product_df is not None else 0,
            'product_volume_loaded': self.product_volume_df is not None,
            'product_volume_count': len(self.product_volume_df) if self.product_volume_df is not None else 0,
            'revenue_loaded': self.revenue_df is not None,
            'revenue_count': len(self.revenue_df) if self.revenue_df is not None else 0,
            'churn_loaded': self.churn_df is not None,
            'churn_count': len(self.churn_df) if self.churn_df is not None else 0,
        }
        return summary
