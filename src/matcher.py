from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def extract_keywords(text: str) -> set:
    """Extract meaningful words, remove stopwords."""
    stopwords = {"a","an","the","and","or","of","to","in","for","with",
                 "is","are","be","have","has","that","this","it","on","at"}
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.]*\b', text.lower())
    return {w for w in words if w not in stopwords and len(w) > 1}

def calculate_match(resume_text: str, job_desc: str) -> float:
    if not resume_text.strip() or not job_desc.strip():
        return 0.0
    try:
        # TF-IDF cosine similarity (base score)
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf = vectorizer.fit_transform([resume_text.lower(), job_desc.lower()])
        cosine_score = cosine_similarity(tfidf[0], tfidf[1])[0][0] * 100

        # Keyword overlap bonus (skill keywords matter more than generic words)
        resume_kw = extract_keywords(resume_text)
        job_kw = extract_keywords(job_desc)
        if job_kw:
            overlap = len(resume_kw & job_kw) / len(job_kw)
            overlap_score = overlap * 100
        else:
            overlap_score = 0

        # Weighted blend: 50% TF-IDF + 50% keyword overlap
        final = (cosine_score * 0.5) + (overlap_score * 0.5)
        return round(min(final, 100.0), 2)
    except Exception:
        return 0.0