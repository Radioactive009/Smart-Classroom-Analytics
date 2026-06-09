from transformers import pipeline

print("Testing sentiment...")
sentiment = pipeline("sentiment-analysis")
print("Sentiment OK")

print("Testing summarization...")
summarizer = pipeline("summarization")
print("Summarization OK")