# pages/1_DataLayer_Checker.py

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json
import time

# Fetch dataLayer using Selenium
def get_data_layer(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)

    try:
        data_layer = driver.execute_script("return window.dataLayer;")
    except Exception:
        data_layer = None

    driver.quit()
    return data_layer

# Flatten list of objects in dataLayer
def flatten_data_layer(data_layer):
    flat_rows = []
    for obj in data_layer:
        if isinstance(obj, dict):
            flat_rows.append({k: str(v) for k, v in obj.items()})
        else:
            flat_rows.append({"non_dict_value": str(obj)})
    return pd.DataFrame(flat_rows)

# Streamlit UI
st.set_page_config(page_title="DataLayer Checker", page_icon="📦", layout="centered")
st.title("📦 DataLayer Checker (Google Analytics)")

with st.form(key="datalayer_form"):
    url = st.text_input("Enter a webpage URL")
    submitted = st.form_submit_button("Check dataLayer")

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
