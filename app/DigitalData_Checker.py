# DigitalData_Checker.py

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import pandas as pd
import time

# Set Streamlit config — MUST be first
st.set_page_config(page_title="DigitalData Checker", page_icon="🔎", layout="centered")


# Function to fetch digitalData using Selenium
def get_digital_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)

    try:
        digital_data = driver.execute_script("return window.digitalData;")
    except Exception:
        digital_data = None

    driver.quit()
    return digital_data

# Flatten nested JSON
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], f'{name}{a}_')
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, f'{name}{i}_')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Streamlit UI
st.title("🔎 DigitalData Checker (Adobe)")

with st.form(key="digitaldata_form"):
    url = st.text_input("Enter a webpage URL")
    submitted = st.form_submit_button("Find")

if submitted:
    if url:
        with st.spinner("Checking for digitalData..."):
            data = get_digital_data(url)

        if data:
            st.success("✅ digitalData found!")

            flat_data = flatten_json(data)
            df = pd.DataFrame(flat_data.items(), columns=["Key", "Value"])
            st.subheader("🔍 Flattened DigitalData")
            st.dataframe(df, use_container_width=True)

            st.subheader("🧾 Raw digitalData JSON")
            st.json(data)
        else:
            st.error("❌ digitalData not found on this page.")
    else:
        st.warning("⚠️ Please enter a valid URL.")
