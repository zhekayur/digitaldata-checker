# pages/1_DataLayer_Checker.py

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json
import time

# Function to fetch dataLayer using Selenium
def get_data_layer(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait for JavaScript to render
    time.sleep(3)

    try:
        data_layer = driver.execute_script("return window.dataLayer;")
    except Exception:
        data_layer = None

    driver.quit()
    return data_layer

# Helper to flatten dataLayer (list of dicts)
def flatten_data_layer(data_layer):
    flat_rows = []
    for obj in data_layer:
        flat_rows.append({k: str(v) for k, v in obj.items()})
    return pd.DataFrame(flat_rows)

# UI
st.set_page_config(page_title="DataLayer Checker", layout="centered")
st.title("📦 DataLayer Checker (for Google Analytics)")

with st.form(key="digitaldata_form"):
    url = st.text_input("Enter a webpage URL")
    submitted = st.form_submit_button("Find")

if submitted:
    if url:
        with st.spinner("Checking for dataLayer..."):
            data = get_data_layer(url)

        if data:
            st.success("✅ dataLayer found!")

            df = flatten_data_layer(data)
            st.subheader("📋 Flattened dataLayer Entries")
            st.dataframe(df, use_container_width=True)

            st.subheader("🧾 Raw dataLayer JSON")
            st.json(data)
        else:
            st.error("❌ dataLayer not found.")
    else:
        st.warning("⚠️ Please enter a valid URL.")
