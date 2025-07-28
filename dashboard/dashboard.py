import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

# Page config
st.set_page_config(page_title="Phishing Logs Dashboard", layout="wide")

st.title("🔒 Phishing Logs Dashboard")

csv_path = "backend/logs.csv"
st.write("📁 Looking for CSV at:", csv_path)

try:
    df = pd.read_csv(csv_path)

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Basic filters
    with st.sidebar:
        st.header("🔎 Filters")
        selected_domain = st.multiselect("Filter by domain (url)", df['url'].unique())
        date_range = st.date_input("Filter by date range", [])

    # Apply filters
    if selected_domain:
        df = df[df['url'].isin(selected_domain)]

    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

    # Optional domain categorization (Day 3)
    def categorize(url):
        if "bank" in url or "mada" in url:
            return "Banking"
        elif "pay" in url:
            return "E-commerce"
        elif ".gov" in url:
            return "Government"
        else:
            return "Other"

    df["category"] = df["url"].apply(categorize)

    # Success + shape
    st.success("✅ CSV Loaded Successfully")
    st.markdown(f"📊 **Data shape**: `{df.shape}`")

    # Main table
    st.dataframe(df)

    # Charts
    st.subheader("📈 Phishing Attempts Over Time")
    line_df = df.groupby(df['timestamp'].dt.date).size().reset_index(name='count')
    st.line_chart(line_df.set_index('timestamp'))

    st.subheader("🥧 Domain Categories")
    pie_df = df['category'].value_counts()
    st.bar_chart(pie_df)

    # CSV download
    def convert_df(data):
        return data.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Export CSV",
        data=convert_df(df),
        file_name='filtered_logs.csv',
        mime='text/csv'
    )

except FileNotFoundError:
    st.error("❌ logs.csv not found in the backend folder.")
except Exception as e:
    st.error(f"⚠️ Something went wrong: {e}")
