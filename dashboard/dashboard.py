import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

# Set up the page layout
st.set_page_config(page_title="Phishing Logs Dashboard", layout="wide")
st.title("🔒 Phishing Logs Dashboard")

# Path to CSV file
csv_path = "backend/logs.csv"

# Load CSV with error handling
try:
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Sidebar filters
    with st.sidebar:
        st.header("🔎 Filters")
        unique_domains = df['url'].dropna().unique()
        selected_domains = st.multiselect("Filter by Domain", unique_domains)

        date_range = st.date_input("Filter by Date Range", [])

    # Apply domain filter
    if selected_domains:
        df = df[df['url'].isin(selected_domains)]

    # Apply date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

    # Categorize domains
    def categorize_domain(url):
        if pd.isna(url):
            return "Unknown"
        url = url.lower()
        if "bank" in url or "mada" in url:
            return "Banking"
        elif "gov" in url:
            return "Government"
        elif "pay" in url or "store" in url or "shop" in url:
            return "Ecommerce"
        else:
            return "Other"

    df["category"] = df["url"].apply(categorize_domain)

    # Show key metrics
    st.markdown("### 📊 Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Logs", len(df))
    col2.metric("Unique Domains", df['url'].nunique())
    col3.metric("Categories", df['category'].nunique())

    # Display filtered logs
    st.markdown("### 🧾 Raw Log Data")
    st.dataframe(df, use_container_width=True)

    # Line chart: Phishing attempts over time
    st.markdown("### 📈 Phishing Attempts Over Time")
    line_df = df.groupby(df['timestamp'].dt.date).size().reset_index(name='count')
    st.line_chart(line_df.set_index('timestamp'))

    # Bar chart: Domain categories
    st.markdown("### 📊 Domain Categories")
    category_counts = df['category'].value_counts()
    st.bar_chart(category_counts)

    # Export filtered CSV
    st.markdown("### 📥 Export Filtered Logs")
    csv_export = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv_export,
        file_name="filtered_logs.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error("❌ logs.csv not found in the backend folder.")
except Exception as e:
    st.error(f"⚠️ Something went wrong: {e}")