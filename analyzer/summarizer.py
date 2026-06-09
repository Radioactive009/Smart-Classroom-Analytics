from transformers import pipeline

summarizer_pipeline = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def generate_summary(transcript):

    if len(transcript.split()) < 20:
        return transcript

    summary = summarizer_pipeline(
        transcript,
        max_length=50,
        min_length=10,
        do_sample=False
    )

    return summary[0]["summary_text"]