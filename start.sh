#!/bin/bash

# Ensure Chrome is in the path
export PATH=$PATH:/usr/bin

# Run your Streamlit app
streamlit run app/DigitalData_Checker.py --server.port=8501 --server.enableCORS=false
