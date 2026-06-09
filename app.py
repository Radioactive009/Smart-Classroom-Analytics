import streamlit as st
import os
import librosa

from analyzer.transcriber import transcribe_audio

from analyzer.metrics import (
    get_word_count,
    calculate_wpm,
    get_speed_category,
    detect_fillers,
    analyze_pauses
)

from analyzer.sentiment import (
    analyze_sentiment
)

from analyzer.keywords import (
    extract_keywords
)

# ------------------------------------
# Page Configuration
# ------------------------------------

st.set_page_config(
    page_title="Smart Classroom Speech Analytics",
    layout="wide"
)

# ------------------------------------
# Create Upload Folder
# ------------------------------------

os.makedirs("uploads", exist_ok=True)

# ------------------------------------
# Title
# ------------------------------------

st.title("🎙 Smart Classroom Speech Analytics")

st.markdown(
    "Upload classroom audio and receive AI-powered speech analytics."
)

# ------------------------------------
# File Upload
# ------------------------------------

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

            transcript = transcribe_audio(
                file_path
            )

            duration_seconds = round(
                librosa.get_duration(
                    path=file_path
                ),
                2
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

            keywords = extract_keywords(
                transcript
            )

            sentiment = analyze_sentiment(
                transcript
            )

            pause_count, pause_duration = (
                analyze_pauses(
                    file_path
                )
            )

        st.success(
            "Analysis Complete!"
        )

        # ------------------------------------
        # Main Metrics Row
        # ------------------------------------

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Words",
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

        col4.metric(
            "Pauses",
            pause_count
        )

        col5.metric(
            "Duration (sec)",
            duration_seconds
        )

        # ------------------------------------
        # Sentiment Section
        # ------------------------------------

        st.subheader("😊 Sentiment")

        sent1, sent2 = st.columns(2)

        sent1.metric(
            "Label",
            sentiment["label"]
        )

        sent2.metric(
            "Confidence %",
            sentiment["score"]
        )

        # ------------------------------------
        # Keywords
        # ------------------------------------

        st.subheader("🔑 Keywords")

        if keywords:

            keyword_cols = st.columns(
                min(len(keywords), 5)
            )

            for i, keyword in enumerate(
                keywords[:5]
            ):
                keyword_cols[i].info(
                    keyword.title()
                )

        # ------------------------------------
        # Pause Analytics
        # ------------------------------------

        st.subheader("⏸ Pause Analytics")

        st.info(
            f"Detected {pause_count} pauses with a total duration of {pause_duration} seconds."
        )

        # ------------------------------------
        # Filler Words
        # ------------------------------------

        st.subheader("🗣 Filler Words")

        st.json(
            fillers
        )

        # ------------------------------------
        # Transcript
        # ------------------------------------

        st.subheader("📝 Transcript")

        st.write(
            transcript
        )