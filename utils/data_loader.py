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
    
    def _load_accounts_data(self):
        """Load accounts data dictionary"""
        file_path = self._find_csv_file("*accounts_datadictionary*.csv")
        
        if file_path:
            # Since the actual accounts data is not provided, we create a data dictionary
            # The user needs to upload the actual accounts extract
            self.accounts_schema = pd.read_csv(file_path)
            st.session_state['accounts_schema'] = self.accounts_schema
            
            # Check if actual accounts data exists
            accounts_data_path = self._find_csv_file("*accounts_data*.csv")
            if accounts_data_path:
                df = pd.read_csv(accounts_data_path)
                
                # Parse date columns based on schema
                date_columns = [
                    'ACNTS_OPENING_DATE', 'ACNTS_LAST_TRAN_DATE', 
                    'ACNTS_CLOSURE_DATE', 'ACNTS_MATURITY_DATE',
                    'ACNTS_NONSYS_LAST_DATE', 'ACNTS_BASE_DATE'
                ]
                
                for col in date_columns:
                    if col in df.columns:
                        df[col] = df[col].apply(self._parse_date)
                
                self.accounts_df = df
            else:
                st.warning("⚠️ Accounts data file not found. Please upload 'accounts_data.csv' to the data folder.")
                self.accounts_df = None
        else:
            st.error("❌ Accounts data dictionary file not found.")
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
            
            # Parse date columns
            date_cols = ['Gl Date Of Opening', 'Gl Closure Date', 'Gl Entd On', 
                        'Gl Last Mod On', 'Gl Auth On']
            for col in date_cols:
                if col in self.gl_df.columns:
                    self.gl_df[col] = self.gl_df[col].apply(self._parse_date)
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
    
    def _load_all_data(self):
        """Load all data sources"""
        self._load_accounts_data()
        self._load_sector_classification()
        self._load_gl_categories()
        self._load_product_types()
    
    def _create_data_model(self):
        """Create relationships between tables"""
        if self.accounts_df is not None and self.product_df is not None:
            # Merge accounts with product information
            if 'ACNTS_PROD_CODE' in self.accounts_df.columns and 'Product Code' in self.product_df.columns:
                self.accounts_df = self.accounts_df.merge(
                    self.product_df[['Product Code', 'Product Name', 'Product Class', 'Product Group Code']],
                    left_on='ACNTS_PROD_CODE',
                    right_on='Product Code',
                    how='left'
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
        """Get GL categories dataframe"""
        return self.gl_df
    
    def get_product_data(self):
        """Get product types dataframe"""
        return self.product_df
    
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
        }
        return summary
