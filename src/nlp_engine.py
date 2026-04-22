from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_similarity_scores(user_input, role_descriptions):
    vectorizer = TfidfVectorizer()

    texts = role_descriptions + [user_input]

    tfidf_matrix = vectorizer.fit_transform(texts)

    scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    return scores.flatten()