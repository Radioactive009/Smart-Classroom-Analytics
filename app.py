import streamlit as st
import os
from analyzer.transcriber import transcribe_audio

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Smart Classroom Speech Analytics",
    layout="wide"
)

# -------------------------------
# Create Upload Folder
# -------------------------------
os.makedirs("uploads", exist_ok=True)

# -------------------------------
# Title
# -------------------------------
st.title("🎙 Smart Classroom Speech Analytics")

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader(
    "Upload Audio",
    type=["wav", "mp3", "m4a"]
)

if uploaded_file:

    file_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.audio(file_path)

    if st.button("Transcribe"):

        with st.spinner("Transcribing Audio..."):

            transcript = transcribe_audio(file_path)

        st.success("Transcription Complete!")

        st.subheader("Transcript")

        st.write(transcript)