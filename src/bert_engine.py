from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import numpy as np

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def bert_similarity(user_input: str, roles: list) -> np.ndarray:
    """Returns a 1D array of similarity scores, one per role."""
    if not user_input.strip() or not roles:
        return np.zeros(len(roles))

    model = load_model()
    embeddings = model.encode(roles + [user_input])
    user_vec = embeddings[-1]
    role_vecs = embeddings[:-1]
    scores = cosine_similarity([user_vec], role_vecs)
    return scores[0]  # ← was accidentally including career_path code in your message