from textblob import TextBlob
from collections import Counter


def extract_top_nouns(text: str, top_n: int = 3):
    blob = TextBlob(text)
    nouns = [word.lower() for word, tag in blob.tags if tag == "NN"]
    most_common = Counter(nouns).most_common(top_n)
    return [noun for noun, count in most_common]
