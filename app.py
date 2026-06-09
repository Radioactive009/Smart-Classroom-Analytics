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

from analyzer.summarizer import (
    generate_summary
)

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Smart Classroom Speech Analytics",
    page_icon="🎙",
    layout="wide"
)

# ==================================
# FOLDER SETUP
# ==================================

os.makedirs("uploads", exist_ok=True)

# ==================================
# HEADER
# ==================================

st.title("🎙 Smart Classroom Speech Analytics")

st.markdown(
    """
    Upload classroom recordings and receive AI-powered insights including:
    
    - Speech-to-Text
    - Speaking Rate Analysis
    - Pause Detection
    - Filler Word Analysis
    - Sentiment Analysis
    - Keyword Extraction
    - AI Generated Summary
    """
)

st.divider()

# ==================================
# FILE UPLOAD
# ==================================

uploaded_file = st.file_uploader(
    "Upload Audio File",
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

    if st.button("🚀 Analyze Audio"):

        with st.spinner("Running AI Analysis..."):

            # ---------------------------
            # Speech Recognition
            # ---------------------------

            transcript = transcribe_audio(
                file_path
            )

            # ---------------------------
            # Audio Metrics
            # ---------------------------

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

            pause_count, pause_duration = (
                analyze_pauses(
                    file_path
                )
            )

            # ---------------------------
            # NLP Features
            # ---------------------------

            keywords = extract_keywords(
                transcript
            )

            sentiment = analyze_sentiment(
                transcript
            )

            summary = generate_summary(
                transcript
            )

        st.success(
            "✅ Analysis Complete"
        )

        # ==================================
        # MAIN METRICS
        # ==================================

        st.subheader("📊 Speech Metrics")

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
            "Duration",
            f"{duration_seconds}s"
        )

        st.divider()

        # ==================================
        # SUMMARY
        # ==================================

        st.subheader("📄 AI Summary")

        st.info(summary)

        # ==================================
        # SENTIMENT
        # ==================================

        st.subheader("😊 Sentiment Analysis")

        sent1, sent2 = st.columns(2)

        sent1.metric(
            "Sentiment",
            sentiment["label"]
        )

        sent2.metric(
            "Confidence %",
            sentiment["score"]
        )

        st.divider()

        # ==================================
        # KEYWORDS
        # ==================================

        st.subheader("🔑 Keywords")

        if keywords:

            keyword_cols = st.columns(
                min(len(keywords), 5)
            )

            for i, keyword in enumerate(
                keywords[:5]
            ):
                keyword_cols[i].success(
                    keyword.title()
                )

        st.divider()

        # ==================================
        # PAUSE ANALYTICS
        # ==================================

        st.subheader("⏸ Pause Analytics")

        st.info(
            f"""
            Total Pauses Detected: {pause_count}
            
            Total Pause Duration: {pause_duration} seconds
            """
        )

        st.divider()

        # ==================================
        # FILLER WORDS
        # ==================================

        st.subheader("🗣 Filler Words")

        filler_cols = st.columns(
            len(fillers)
        )

        for idx, (word, count) in enumerate(
            fillers.items()
        ):
            filler_cols[idx].metric(
                word,
                count
            )

        st.divider()

        # ==================================
        # TRANSCRIPT
        # ==================================

        st.subheader("📝 Transcript")

        with st.expander(
            "View Full Transcript",
            expanded=True
        ):
            st.write(
                transcript
            )