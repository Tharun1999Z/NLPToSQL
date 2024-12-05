from openai import AzureOpenAI
import streamlit as st

class AIService:
    """Handles all AI-related operations"""
    
    def __init__(self, config):
        """Initialize AI service with configuration"""
        self.client = AzureOpenAI(
            api_key=config.AZURE_API_KEY,
            api_version=config.AZURE_API_VERSION,
            azure_endpoint=config.AZURE_ENDPOINT
        )
        self.schema = config.SCHEMA
    
    def generate_sql_query(self, user_input: str) -> str:
        """Generate SQL query from natural language input"""
        prompt = f"""Given the table schema:\n{self.schema}\n
Generate ONLY the SQL query without any explanation or additional text for this 
user input: '{user_input}'.
The query should:
1. Reference the table as 'df'
2. Account for potential spelling mistakes in column names
3. Ensure keyword matching is case-insensitive
4. Use partial matching where appropriate
5. Return only the SQL query, no explanations"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-35-turbo",
                messages=[
                    {"role": "system", "content": "You are an SQL generation assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0
            )
            
            sql_query = response.choices[0].message.content.strip()
            sql_query = sql_query.replace('ProgramData', 'df')
            if not sql_query.endswith(';'):
                sql_query += ';'
            return sql_query
            
        except Exception as e:
            st.error(f"Error generating SQL query: {str(e)}")
            return None
