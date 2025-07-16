import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Pivot Table Generator", layout="wide")
st.title("🔁 Pivot Table Generator")

st.markdown("Upload a CSV or Excel file to generate a pivot table quickly and easily.")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Load file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📋 Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        # Pivot table controls
        st.markdown("### ➕ Pivot Table Options")
        with st.form("pivot_form"):
            rows = st.multiselect("Rows", options=df.columns)
            columns = st.multiselect("Columns", options=df.columns)
            values = st.multiselect("Values", options=df.select_dtypes(include=['number']).columns)
            aggfunc = st.selectbox("Aggregation Function", ['sum', 'mean', 'count'])

            submit = st.form_submit_button("Generate")

        if submit:
            if not values:
                st.warning("Select at least one column for 'Values'.")
            else:
                pivot = pd.pivot_table(df, index=rows, columns=columns, values=values, aggfunc=aggfunc, fill_value=0)
                st.success("✅ Pivot Table Created")
                st.dataframe(pivot, use_container_width=True)

                # Download option
                buffer = BytesIO()
                pivot.to_excel(buffer)
                buffer.seek(0)
                st.download_button(
                    label="📥 Download as Excel",
                    data=buffer,
                    file_name="pivot_table.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"⚠️ Error: {e}")