import streamlit as st

st.set_page_config(
    page_title="Student Attention Monitoring System",
    layout="centered"
)

st.title("🎓 Student Attention Monitoring System")

st.write(
    "AI-powered assistive technology for visually impaired tutors."
)

# Webcam Input
camera = st.camera_input("Open Webcam")

if camera:
    st.success("Webcam Connected Successfully ✅")