import re

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

    return round(word_count / (duration_seconds / 60), 2)


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

        pattern = r'\b' + re.escape(filler) + r'\b'

        count = len(re.findall(pattern, transcript))

        filler_counts[filler] = count

    return filler_counts