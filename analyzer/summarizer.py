from transformers import pipeline

summarizer_pipeline = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

def generate_summary(transcript):

    if len(transcript.split()) < 20:
        return transcript

    result = summarizer_pipeline(
        transcript,
        max_length=50,
        min_length=10,
        do_sample=False
    )

    return result[0]["summary_text"]