{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "47d13b9d-fe00-4e19-8d6e-1f81ef944288",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "from io import BytesIO\n",
    "\n",
    "st.set_page_config(page_title=\"Pivot Table Generator\", layout=\"wide\")\n",
    "st.title(\"🔁 Pivot Table Generator\")\n",
    "\n",
    "st.markdown(\"Upload a CSV or Excel file to generate a pivot table quickly and easily.\")\n",
    "\n",
    "# File uploader\n",
    "uploaded_file = st.file_uploader(\"Choose a file\", type=[\"csv\", \"xlsx\"])\n",
    "\n",
    "if uploaded_file:\n",
    "    try:\n",
    "        # Load file\n",
    "        if uploaded_file.name.endswith('.csv'):\n",
    "            df = pd.read_csv(uploaded_file)\n",
    "        else:\n",
    "            df = pd.read_excel(uploaded_file)\n",
    "\n",
    "        st.subheader(\"📋 Data Preview\")\n",
    "        st.dataframe(df.head(), use_container_width=True)\n",
    "\n",
    "        # Pivot table controls\n",
    "        st.markdown(\"### ➕ Pivot Table Options\")\n",
    "        with st.form(\"pivot_form\"):\n",
    "            rows = st.multiselect(\"Rows\", options=df.columns)\n",
    "            columns = st.multiselect(\"Columns\", options=df.columns)\n",
    "            values = st.multiselect(\"Values\", options=df.select_dtypes(include=['number']).columns)\n",
    "            aggfunc = st.selectbox(\"Aggregation Function\", ['sum', 'mean', 'count'])\n",
    "\n",
    "            submit = st.form_submit_button(\"Generate\")\n",
    "\n",
    "        if submit:\n",
    "            if not values:\n",
    "                st.warning(\"Select at least one column for 'Values'.\")\n",
    "            else:\n",
    "                pivot = pd.pivot_table(df, index=rows, columns=columns, values=values, aggfunc=aggfunc, fill_value=0)\n",
    "                st.success(\"✅ Pivot Table Created\")\n",
    "                st.dataframe(pivot, use_container_width=True)\n",
    "\n",
    "                # Download option\n",
    "                buffer = BytesIO()\n",
    "                pivot.to_excel(buffer)\n",
    "                buffer.seek(0)\n",
    "                st.download_button(\n",
    "                    label=\"📥 Download as Excel\",\n",
    "                    data=buffer,\n",
    "                    file_name=\"pivot_table.xlsx\",\n",
    "                    mime=\"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\"\n",
    "                )\n",
    "\n",
    "    except Exception as e:\n",
    "        st.error(f\"⚠️ Error: {e}\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
# Last updated: July 16, 2025
