#ui_componets.py
import streamlit as st
import pandas as pd
import plotly.express as px

class UIComponents:

    @staticmethod
    def display_header():
        """Display the application header."""
        st.title("📝 Zion AI Chatbot")

    @staticmethod
    def display_input_section(value=""):
        """Display the input section for user query."""
        st.header("Speak or Type your Query")
        return st.text_area("Enter your query here:", value=value, height=100)

    @staticmethod
    def display_generated_sql(sql_query: str):
        """Display the generated SQL query."""
        st.subheader("Generated SQL Query")
        st.code(sql_query, language="sql")

    @staticmethod
    def display_results(result_df: pd.DataFrame):
        """Display the query results as a DataFrame and the record count."""
        if result_df is not None and not result_df.empty:
            st.success(f"Query executed successfully! {len(result_df):,} records found.")

            # Display the DataFrame
            st.dataframe(result_df, use_container_width=True)

            # Button to show graph
            if st.button("Show Graph", key="show_graph_button"):
                st.session_state["graph_display"] = True



            # Check if "Show Graph" was clicked and display the graph
            if st.session_state.get("graph_display", False):
                UIComponents.show_graph(result_df)
        else:
            st.warning("Query executed but returned no results.")

    @staticmethod
    def show_graph(df: pd.DataFrame):
        """Generate and display a graph."""
        st.subheader("Data Visualization")
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()

        if not numeric_cols and not categorical_cols:
            st.warning("No suitable columns available for plotting.")
            return

        # Dropdown for selecting the plot type
        plot_type = st.selectbox("Select Plot Type", ["Bar", "Pie", "Scatter", "Line"], key="plot_type")

        # Generate plots based on selection
        if plot_type == "Bar":
            x_col = st.selectbox("Select X-axis Column", categorical_cols, key="x_col_bar")
            y_col = st.selectbox("Select Y-axis Column", numeric_cols, key="y_col_bar")
            fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Chart: {y_col} by {x_col}")

        elif plot_type == "Pie":
            category_col = st.selectbox("Select Category Column", categorical_cols, key="pie_col")
            fig = px.pie(df, names=category_col, title=f"Pie Chart: Distribution of {category_col}")

        elif plot_type == "Scatter":
            x_col = st.selectbox("Select X-axis Column", numeric_cols, key="x_col_scatter")
            y_col = st.selectbox("Select Y-axis Column", numeric_cols, key="y_col_scatter")
            fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot: {y_col} vs {x_col}")

        elif plot_type == "Line":
            x_col = st.selectbox("Select X-axis Column", categorical_cols + numeric_cols, key="x_col_line")
            y_col = st.selectbox("Select Y-axis Column", numeric_cols, key="y_col_line")
            fig = px.line(df, x=x_col, y=y_col, title=f"Line Chart: {y_col} vs {x_col}")

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)


    @staticmethod
    def display_error_message(message: str):
        """Display an error message."""
        st.error(message)
