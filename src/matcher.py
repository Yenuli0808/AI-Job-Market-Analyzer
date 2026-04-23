from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match(resume_text: str, job_desc: str) -> float:
    """Cosine similarity between resume and job description using TF-IDF."""
    if not resume_text.strip() or not job_desc.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf = vectorizer.fit_transform([resume_text.lower(), job_desc.lower()])
        score = cosine_similarity(tfidf[0], tfidf[1])[0][0]
        return round(float(score) * 100, 2)
    except Exception:
        return 0.0