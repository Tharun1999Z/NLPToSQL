#main.py
import streamlit as st
from config import Config
from database import Database
from ai_service import AIService
from ui_components import UIComponents
from voice_service import VoiceService


def main():
    st.set_page_config(page_title="ZionAI Chatbot", layout="wide")

    # Initialize AIService and UI Components
    ai_service = AIService(Config)
    ui = UIComponents()

    # Display header
    ui.display_header()

    # Load the dataset
    df = Database.load_data(Config.DATA_FILE)
    if df is not None:
        st.success(f"Dataset loaded successfully with {len(df):,} records")
    else:
        st.error("Failed to load the dataset. Please check the file path.")
        return

    if "transcribed_text" not in st.session_state:
        st.session_state["transcribed_text"] = ""



    # Input Section
    user_input = ui.display_input_section(value=st.session_state["transcribed_text"])

    # Initialize VoiceService
    voice_service = VoiceService()

    # Voice Button Section
    if st.button("🎙️ Speak"):
        # Capture voice input
        voice_text = voice_service.record_and_transcribe()
        if voice_text:
            st.write(f"**Transcribed Text:** {voice_text}")
            # Store the transcribed text in session state
            st.session_state["transcribed_text"] = voice_text
            # Update the input box with the transcribed text
            st.rerun()

    # SQL Generation and Execution
    if st.button("🚀 Submit"):
        if user_input.strip():
            with st.spinner("Converting text to SQL..."):
                sql_query = ai_service.generate_sql_query(user_input)

            if sql_query:
                #ui.display_generated_sql(sql_query)

                # Execute the SQL Query
                with st.spinner("Executing SQL Query..."):
                    result_df = Database.execute_query(sql_query, locals())

                # Store results in session state
                if result_df is not None and not result_df.empty:
                    st.session_state["query_results"] = result_df
                    st.session_state["sql_query"] = sql_query
                else:
                    st.warning("Query executed but returned no results.")
            else:
                ui.display_error_message("Failed to generate SQL query. Please try again.")
        else:
            st.warning("Please enter a valid query.")

# Display results if available
    if "query_results" in st.session_state:
        ui.display_results(st.session_state["query_results"])


if __name__ == "__main__":
    main()
