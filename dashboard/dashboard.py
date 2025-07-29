import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

# Set up layout
st.set_page_config(page_title="Phishing Logs Dashboard", layout="wide")
st.title("🔒 Saudi PhishGuard - Dashboard")

# Path to CSV
csv_path = "backend/logs.csv"

# Load and validate data
try:
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])  # Remove bad timestamps

    # Auto-categorize if category missing
    def auto_categorize(url):
        url = str(url).lower()
        if "bank" in url or "mada" in url or "samba" in url:
            return "Banking"
        elif "gov" in url or "absher" in url or "zakah" in url:
            return "Government"
        elif "moh" in url or "health" in url or "clinic" in url or "care" in url:
            return "Health"
        elif "noon" in url or "souq" in url or "store" in url:
            return "Ecommerce"
        elif "edu" in url or "tamkeen" in url:
            return "Education"
        else:
            return "Other"

    if "category" not in df.columns:
        df["category"] = df["url"].apply(auto_categorize)
    else:
        df["category"] = df["category"].fillna(df["url"].apply(auto_categorize))

    # Sidebar filters
    with st.sidebar:
        st.header("🔎 Filters")
        unique_domains = df['url'].dropna().unique()
        selected_domains = st.multiselect("Filter by Domain", unique_domains)

        date_range = st.date_input("Filter by Date Range", [])

    # Apply filters
    if selected_domains:
        df = df[df['url'].isin(selected_domains)]
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

    # Show metrics
    st.subheader("📊 Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Logs", len(df))
    col2.metric("Unique Domains", df['url'].nunique())
    col3.metric("Categories", df['category'].nunique())

    # Show raw data
    st.subheader("🧾 Raw Logs")
    df_reset = df.reset_index(drop=True)
    df_reset.index += 1  # start index from 1
    st.dataframe(df_reset, use_container_width=True)

    # Line chart
    st.subheader("📈 Phishing Attempts Over Time")
    line_df = df.groupby(df['timestamp'].dt.date).size().reset_index(name='Attempts')
    st.line_chart(line_df.set_index('timestamp'))

    # Category bar chart
    st.subheader("📊 Domain Categories")
    category_counts = df['category'].value_counts()
    st.bar_chart(category_counts)

    # Export
    st.subheader("📥 Export Filtered Logs")
    csv_export = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv_export,
        file_name="filtered_logs.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error("❌ logs.csv not found.")
except Exception as e:
    st.error(f"⚠️ Error: {e}")
