from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def bert_similarity(user_input, roles):
    model = load_model()

    embeddings = model.encode(roles + [user_input])

    user_vec = embeddings[-1]
    role_vecs = embeddings[:-1]

    scores = cosine_similarity([user_vec], role_vecs)

    return scores[0]