#database.py

import pandas as pd
from pandasql import sqldf
import streamlit as st

class Database:
    @staticmethod
    @st.cache_data
    def load_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            st.error(f"Error loading dataset: {str(e)}")
            return None

    @staticmethod
    def execute_query(sql_query: str, local_vars: dict) -> pd.DataFrame:
        try:
            return sqldf(sql_query, local_vars)
        except Exception as e:
            st.error(f"Error executing SQL query: {str(e)}")
            return None
