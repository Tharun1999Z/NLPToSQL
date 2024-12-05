import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class UIComponents:
    @staticmethod
    def create_sql_visualization(df: pd.DataFrame):
        """Create appropriate visualization for SQL query results"""
        if len(df) == 1 and len(df.columns) == 1:
            value = df.iloc[0, 0]
            fig = go.Figure()
            fig.add_trace(go.Indicator(
                mode="number",
                value=value,
                title={"text": df.columns[0]},
                number={"font": {"size": 50}}
            ))
            fig.update_layout(height=300)
            return fig
            
        # Handle time series or categorical data
        elif len(df) > 1:
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_cols) > 0:
                y_col = numeric_cols[0]
                x_col = [col for col in df.columns if col != y_col][0] if len(df.columns) > 1 else df.index
                
                fig = px.bar(df, x=x_col, y=y_col,
                           title=f"{y_col} Distribution",
                           labels={y_col: y_col.replace('_', ' ').title(),
                                  x_col: x_col.replace('_', ' ').title()})
                fig.update_layout(height=500)
                return fig
        
        return None

    @staticmethod
    def display_results(result_df: pd.DataFrame):
        if result_df is not None and len(result_df) > 0:
            st.metric("Number of Records", f"{len(result_df):,}")
            
            # Display data
            st.dataframe(result_df, use_container_width=True)
            
            st.subheader("Query Visualization")
            fig = UIComponents.create_sql_visualization(result_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            if len(result_df) > 1 and len(result_df.columns) > 1:
                plot_type = st.selectbox(
                    "Change visualization type",
                    ["bar", "line", "scatter", "pie"],
                    key="plot_type"
                )
                if plot_type != "bar":
                    numeric_cols = result_df.select_dtypes(include=['float64', 'int64']).columns
                    if len(numeric_cols) > 0:
                        y_col = numeric_cols[0]
                        x_col = [col for col in result_df.columns if col != y_col][0]
                        
                        if plot_type == "line":
                            fig = px.line(result_df, x=x_col, y=y_col)
                        elif plot_type == "scatter":
                            fig = px.scatter(result_df, x=x_col, y=y_col)
                        elif plot_type == "pie":
                            fig = px.pie(result_df, values=y_col, names=x_col)
                        
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No records found matching your query.")

    @staticmethod
    def setup_page(config):
        st.set_page_config(page_title=config.PAGE_TITLE, layout=config.LAYOUT)
        if 'input_text' not in st.session_state:
            st.session_state.input_text = ""
    
    @staticmethod
    def display_header():
        st.title("📝 Text to SQL Converter")
    
    @staticmethod
    def display_example_queries():
        with st.expander("See example queries"):
            st.markdown("""
            Try these example queries:
            - Show all completed programs
            - Find programs in January
            - List all programs with more than 50 attendees
            - Show programs in New York state
            - Display programs by speaker John
            """)
    
    @staticmethod
    def get_user_input(voice_service) -> str:
        st.write("💭 **Enter Query (Text or Voice)**")
        col1, col2 = st.columns([6, 1])
        
        with col1:
            input_text = st.text_input(
                "Enter your query:",
                value=st.session_state.input_text,
                placeholder="e.g., 'Show all completed programs' or 'Find programs in January'",
                key="query_input"
            )
        
        with col2:
            if st.button("🎙️ Speak", help="Click to speak your query"):
                voice_text = voice_service.record_and_transcribe()
                if voice_text:
                    st.session_state.input_text = voice_text
                    st.rerun()
        
        return st.session_state.input_text or input_text