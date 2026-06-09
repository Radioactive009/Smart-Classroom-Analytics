import re
from pydub import AudioSegment
from pydub.silence import detect_silence

FILLER_WORDS = [
    "um",
    "uh",
    "like",
    "actually",
    "you know"
]


def get_word_count(transcript):
    return len(transcript.split())


def calculate_wpm(word_count, duration_seconds):

    if duration_seconds == 0:
        return 0

    return round(
        word_count / (duration_seconds / 60),
        2
    )


def get_speed_category(wpm):

    if wpm < 110:
        return "Slow"

    elif wpm <= 160:
        return "Good"

    return "Fast"


def detect_fillers(transcript):

    transcript = transcript.lower()

    filler_counts = {}

    for filler in FILLER_WORDS:

        pattern = r"\b" + re.escape(filler) + r"\b"

        count = len(
            re.findall(pattern, transcript)
        )

        filler_counts[filler] = count

    return filler_counts


def analyze_pauses(audio_path):

    audio = AudioSegment.from_file(audio_path)

    silence_segments = detect_silence(
        audio,
        min_silence_len=500,
        silence_thresh=audio.dBFS - 16
    )

    pause_count = len(silence_segments)

    total_pause_duration = sum(
        (end - start)
        for start, end in silence_segments
    ) / 1000

    return (
        pause_count,
        round(total_pause_duration, 2)
    )