from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis"
)

def analyze_sentiment(transcript):

    result = sentiment_pipeline(
        transcript
    )[0]

    return {
        "label": result["label"],
        "score": round(
            result["score"] * 100,
            2
        )
    }