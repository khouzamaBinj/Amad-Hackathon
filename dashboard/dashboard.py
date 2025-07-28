import streamlit as st
import pandas as pd
import os

# Title
st.title("🔒 Phishing Logs Dashboard")

# Path to logs.csv
csv_path = "backend/logs.csv"
st.write("📁 Looking for CSV at:", csv_path)

try:
    df = pd.read_csv(csv_path)
    st.success("✅ CSV Loaded Successfully")
    st.write("📊 Data shape:", df.shape)
    st.dataframe(df)
except FileNotFoundError:
    st.error("❌ logs.csv not found in the backend folder.")
except Exception as e:
    st.error(f"⚠️ Something went wrong: {e}")
