# streamlit_app.py
import streamlit as st
import pandas as pd
import os
import json
import subprocess
from pathlib import Path

# --- AUTH ---
def authenticate(username, password):
    # Simple hardcoded credentials (you can connect to database later)
    return username == "admin" and password == "password123"

# --- MAIN ---
def main():
    st.title("🚗 RTO Scraper Dashboard")

    # --- Login Section ---
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success("Login successful")
            else:
                st.error("Invalid credentials")
        return  # stop here if not authenticated

    # --- Load States ---
    with open('jsons/states.json', 'r') as f:
        states = json.load(f)
    states_list = list(states.keys())

    # --- Select State ---
    state_selected = st.selectbox("Select State", states_list)

    # --- Load RTOs for that state ---
    rto_json_path = f"jsons/{state_selected}_rtos.json"
    if os.path.exists(rto_json_path):
        with open(rto_json_path, 'r') as f:
            rtos = json.load(f)
        rto_list = list(rtos.keys())
    else:
        rto_list = []

    rto_selected = st.selectbox("Select RTO", rto_list)

    # --- Select Year and Product ---
    years = ["2023", "2024", "2025"]
    products = ["L3P", "L3G", "L5P", "L5G"]

    year_selected = st.selectbox("Select Year", years)
    product_selected = st.selectbox("Select Product", products)

    # --- Button to Start Scraping ---
    if st.button("Start Scraping"):
        with st.spinner('Scraping in progress...'):

            cmd = [
                "python",
                "worker.py",
                state_selected,
                rto_selected,
                year_selected,
                product_selected,
                "True"  # trim option
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            st.text_area("Logs", result.stdout + "\n" + result.stderr, height=300)

            # Check if output file exists
            output_file = f"output/{state_selected}.{rto_selected}.{year_selected}.{product_selected}.csv"
            if os.path.exists(output_file):
                df = pd.read_csv(output_file)
                st.dataframe(df)

                # Download button
                st.download_button(
                    label="Download Data as CSV",
                    data=df.to_csv(index=False),
                    file_name=f"{state_selected}_{rto_selected}_{year_selected}_{product_selected}.csv",
                    mime='text/csv'
                )
            else:
                st.error("Output file not found!")

if __name__ == "__main__":
    main()
