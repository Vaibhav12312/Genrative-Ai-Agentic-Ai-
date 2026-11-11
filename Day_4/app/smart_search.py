
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "records.json"


def load_records():
    """Load EPFO FAQ records from JSON."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_records(query, limit=5):
    """Rank FAQ records using TF-IDF and cosine similarity."""

    if not query or not query.strip():
        return []

    records = load_records()

    documents = [
        f"{record['category']} {record['question']} {record['answer']}"
        for record in records
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

    ranked_indices = scores.argsort()[::-1][:limit]

    results = []

    for index in ranked_indices:
        if scores[index] <= 0:
            continue

        record = records[index].copy()
        record["similarity_score"] = round(float(scores[index]), 4)
        results.append(record)

    return results
