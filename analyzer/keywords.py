from keybert import KeyBERT

kw_model = KeyBERT()


def extract_keywords(transcript):

    keywords = kw_model.extract_keywords(
        transcript,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=5
    )

    return [keyword[0] for keyword in keywords]
