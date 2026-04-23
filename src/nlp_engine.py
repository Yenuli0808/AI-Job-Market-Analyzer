import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_similarity_scores(user_input: str, role_descriptions: list) -> np.ndarray:
    if not user_input.strip() or not role_descriptions:
        return np.zeros(len(role_descriptions))

    try:
        vectorizer = TfidfVectorizer()
        texts = role_descriptions + [user_input]
        tfidf_matrix = vectorizer.fit_transform(texts)
        scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        return scores.flatten()
    except Exception:
        return np.zeros(len(role_descriptions))