from config import Config
from database import Database
from ai_service import AIService
from ui_components import UIComponents
import streamlit as st
from voice_service import VoiceService

def main():
    ui = UIComponents()
    ui.setup_page(Config)
    ui.display_header()
    
    ai_service = AIService(Config)
    voice_service = VoiceService()
    
    df = Database.load_data(Config.DATA_FILE)
    if df is not None:
        st.success(f"Dataset loaded successfully with {len(df):,} records")
        
        user_input = ui.get_user_input(voice_service)
        ui.display_example_queries()
        
        if st.button("Convert to SQL and Execute"):
            if user_input:
                with st.spinner("Converting text to SQL..."):
                    sql_query = ai_service.generate_sql_query(user_input)
                    
                    if sql_query:
                        st.subheader("Generated SQL Query")
                        st.code(sql_query, language='sql')
                        
                        result_df = Database.execute_query(sql_query, locals())
                        st.subheader("Query Results")
                        ui.display_results(result_df)
            else:
                st.warning("Please enter a query first.")

if __name__ == "__main__":
    main()