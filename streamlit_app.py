# streamlit_app.py

import streamlit as st
import requests
import json

st.set_page_config(page_title="Blockchain UI", layout="wide")

# Sidebar input
st.sidebar.title(" Blockchain Node Settings")
base_url = st.sidebar.text_input("Base URL of Node", "http://127.0.0.1:5000")

st.title("Blockchain Frontend Interface")

tabs = st.tabs(["Chain", "New Tx", "Mine", "Register Nodes", "Consensus"])

# Tab: View Chain
with tabs[0]:
    st.subheader("View Full Blockchain")
    if st.button("Fetch Chain"):
        try:
            response = requests.get(f"{base_url}/chain")
            chain_data = response.json()
            st.json(chain_data)
        except:
            st.error("Could not fetch chain. Check URL.")

# Tab: New Transaction
with tabs[1]:
    st.subheader("New Transaction")
    sender = st.text_input("Sender")
    recipient = st.text_input("Recipient")
    amount = st.number_input("Amount", min_value=0.0, step=0.1)
    if st.button("Submit Transaction"):
        data = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }
        try:
            r = requests.post(f"{base_url}/transactions/new", json=data)
            st.success(r.json()["message"])
        except:
            st.error("Failed to create transaction.")

# Tab: Mine Block
with tabs[2]:
    st.subheader("Mine a New Block")
    if st.button("Start Mining"):
        try:
            r = requests.get(f"{base_url}/mine")
            st.success("Block mined successfully!")
            st.json(r.json())
        except:
            st.error("Mining failed.")

# Tab: Register Nodes
with tabs[3]:
    st.subheader("Register New Nodes")
    node_list = st.text_area("Enter node URLs (comma-separated)", "http://127.0.0.1:5001")
    if st.button("Register Nodes"):
        nodes = [n.strip() for n in node_list.split(",")]
        try:
            r = requests.post(f"{base_url}/nodes/register", json={"nodes": nodes})
            st.success("Nodes registered.")
            st.json(r.json())
        except:
            st.error("Failed to register nodes.")

# Tab: Consensus
with tabs[4]:
    st.subheader("Resolve Conflicts (Consensus)")
    if st.button("Run Consensus"):
        try:
            r = requests.get(f"{base_url}/nodes/resolve")
            st.success(r.json()["message"])
            st.json(r.json())
        except:
            st.error("Consensus failed.")
