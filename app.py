import streamlit as st
import os
import librosa

from analyzer.transcriber import transcribe_audio
from analyzer.metrics import (
    get_word_count,
    calculate_wpm,
    get_speed_category,
    detect_fillers
)

# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="Smart Classroom Speech Analytics",
    layout="wide"
)

os.makedirs("uploads", exist_ok=True)

st.title("🎙 Smart Classroom Speech Analytics")

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

    if st.button("Transcribe & Analyze"):

        with st.spinner("Analyzing Audio..."):

            transcript = transcribe_audio(file_path)

            duration_seconds = librosa.get_duration(
                path=file_path
            )

            word_count = get_word_count(
                transcript
            )

            wpm = calculate_wpm(
                word_count,
                duration_seconds
            )

            speed = get_speed_category(
                wpm
            )

            fillers = detect_fillers(
                transcript
            )

        st.success("Analysis Complete!")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Word Count",
            word_count
        )

        col2.metric(
            "WPM",
            wpm
        )

        col3.metric(
            "Speed",
            speed
        )

        st.subheader("Filler Words")

        st.json(fillers)

        st.subheader("Transcript")

        st.write(transcript)