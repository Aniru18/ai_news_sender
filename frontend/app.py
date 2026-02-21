import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI News Summary", layout="centered")

st.title("📰 AI News Summary Generator")

topic = st.text_input("Enter Topic")
email = st.text_input("Enter Email ID (Optional)")

if "summary" not in st.session_state:
    st.session_state.summary = ""

# -------------------------
# Generate Summary Button
# -------------------------
if st.button("Generate Summary"):
    if topic:
        response = requests.post(
            f"{BACKEND_URL}/generate",
            json={"topic": topic}
        )

        if response.status_code == 200:
            st.session_state.summary = response.json()["summary"]
        else:
            st.error("Failed to generate summary.")
    else:
        st.warning("Please enter a topic.")

# -------------------------
# Display Summary
# -------------------------
if st.session_state.summary:
    st.subheader("Generated Summary")
    st.write(st.session_state.summary)

# -------------------------
# Send Mail Button
# -------------------------
if st.button("Send Mail"):
    if not email:
        st.warning("Please enter an email address.")
    else:
        response = requests.post(
            f"{BACKEND_URL}/send-mail",
            json={
                "topic": topic,
                "email": email,
                "summary": st.session_state.summary
            }
        )

        if response.status_code == 200:
            st.success("Email sent successfully!")
        else:
            st.error("Failed to send email.")