import streamlit as st
import pandas as pd
from openai import AzureOpenAI
from pandasql import sqldf
import speech_recognition as sr

# Set page config
st.set_page_config(page_title="Zion AI's Chatbot", layout="wide")

# Add custom CSS for styling
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stAlert {
            margin-top: 1rem;
        }
        .voice-button {
            display: inline-flex;
            align-items: center;
            background-color: #f0f0f0;
            border: none;
            cursor: pointer;
            padding: 6px;
            margin-left: 5px;
            font-size: 16px;
            border-radius: 5px;
        }
        .voice-button:hover {
            background-color: #e0e0e0;
        }
    </style>
""", unsafe_allow_html=True)

# Load the company logo
company_logo = st.image("logo.jpg", width=200)

# Title and description
st.title("🔍 Welcome to Zion AI Chatbot for HCP Engagement")

# Speech-to-Text Function
def record_and_transcribe():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak into your microphone.")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.warning("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
        except sr.WaitTimeoutError:
            st.warning("Listening timed out. Please try again.")
    return ""

# Load the data
@st.cache_data
def load_data():
    file_path = 'dataset_meeting.xlsx'
    return pd.read_excel(file_path)

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key="",  # Replace with your valid API key
    api_version="",
    azure_endpoint="https://demo1nlp.openai.azure.com/"
)

# Load data
try:
    df = load_data()
    st.success(f"📊 Dataset loaded successfully with {len(df):,} records")
except Exception as e:
    st.error("Error loading dataset. Please check if the file exists and is accessible.")
    st.stop()

# Schema definition
schema = """
CREATE TABLE ProgramData (
    ProgramCode VARCHAR(20),
    Franchise VARCHAR(50),
    ClientEventType VARCHAR(100),
    LocationType VARCHAR(50),
    MeetingTopic VARCHAR(255),
    ProgramStatus VARCHAR(50),
    Month VARCHAR(20),
    ProgramDate DATE,
    ProgramTime TIME,
    SpeakerName VARCHAR(100),
    HostName VARCHAR(100),
    Territory VARCHAR(20),
    VenueName VARCHAR(100),
    VenueCity VARCHAR(100),
    VenueState VARCHAR(50),
    VenueZip VARCHAR(20),
    SurveyNeutralme VARCHAR(255),
    Question VARCHAR(500),
    Responses TEXT,
    LASTMODIFIEDDATE DATETIME,
    SurveyTaker_Rep VARCHAR(100),
    Admin Fee DECIMAL(10, 2)
);
"""

# Initialize user_input as a session state variable
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Search bar with Voice Button
st.write("💭 **Search Query with Voice Input**")

col1, col2 = st.columns([8, 1])
with col1:
    query_placeholder = st.empty()
    user_input = query_placeholder.text_input(
        "Enter your query here",
        placeholder="e.g., 'Show all completed programs' or 'Find programs in January'",
        value=st.session_state["user_input"]
    )
with col2:
    if st.button("🎙️ Speak"):
        voice_input = record_and_transcribe()
        if voice_input:
            st.session_state["user_input"] = voice_input  # Update session state with transcribed input

# Add a button to execute the query
if st.button("🚀 Submit", type="primary"):
    user_input = st.session_state["user_input"]  # Ensure user_input comes from the latest session state
    if user_input:
        with st.spinner("Generating and executing SQL query..."):
            try:
                # Generate SQL query
                prompt = f"""Given the table schema:\n{schema}\n
Generate ONLY the SQL query without any explanation or additional text for this 
user input: '{user_input}'.
The query should reference the table as 'df', account for potential spelling mistakes in column names by identifying and correcting them using the most similar column names based on the schema, and ensure that keyword matching for all columns is case-insensitive and uses partial matching.""" 
                response = client.chat.completions.create(
                    model="gpt-35-turbo",
                    messages=[
                        {"role": "system", "content": "You are an SQL generation assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                    temperature=0
                )
                
                generated_sql = response.choices[0].message.content.strip()
                generated_sql = generated_sql.replace('ProgramData', 'df')
                if not generated_sql.endswith(';'):
                    generated_sql += ';'
                
                # Display generated SQL
                with st.expander("🔍 View Generated SQL"):
                    st.code(generated_sql, language='sql')
                
                # Execute query
                result_df = sqldf(generated_sql, locals())
                
                # Display results
                record_count = len(result_df)
                
                st.metric("Number of Records", f"{record_count:,}")
                
                if len(result_df) > 0:
                    st.dataframe(result_df, use_container_width=True, height=400)
                else:
                    st.info("No records found matching your query.")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a query first.")

# Add helpful information at the bottom
with st.expander("ℹ️ Help"):
    st.markdown("""
    **Example Queries:**
    - Show all completed programs
    - Find programs in January
    - List all programs with more than 50 attendees
    - Show programs in New York state
    - Display programs by speaker John
    """)
