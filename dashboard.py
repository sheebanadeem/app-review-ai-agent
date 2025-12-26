import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="App Review Trend Analyzer", layout="wide")

st.title("📊 App Review Trend Analyzer")
st.caption("Semantic topic normalization & trend aggregation")

OUTPUT_DIR = "output"

# List available reports
files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".csv")]

if not files:
    st.warning("No trend reports found. Run main.py first.")
    st.stop()

selected_file = st.selectbox("Select a trend report", files)

df = pd.read_csv(os.path.join(OUTPUT_DIR, selected_file))

st.subheader("📌 Trend Summary")
st.dataframe(df, use_container_width=True)

if "count" in df.columns:
    st.subheader("📈 Topic Frequency")
    st.bar_chart(df.set_index("topic")["count"])

st.subheader("🔍 Raw Data")
st.expander("View raw CSV").write(df)
