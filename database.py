import pandas as pd
from pandasql import sqldf
import streamlit as st

class Database:
    """Handles all database operations"""
    
    @staticmethod
    @st.cache_data
    def load_data(file_path: str) -> pd.DataFrame:
        """Load data from Excel file"""
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            st.error(f"Error loading dataset: {str(e)}")
            return None
    
    @staticmethod
    def execute_query(sql_query: str, local_vars: dict) -> pd.DataFrame:
        """Execute SQL query using pandasql"""
        try:
            return sqldf(sql_query, local_vars)
        except Exception as e:
            st.error(f"Error executing SQL query: {str(e)}")
            return None
