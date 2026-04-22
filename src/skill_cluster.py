from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from preprocess import get_processed_data

def cluster_skills(n_clusters=5):
    df = get_processed_data()

    skills = df["job_skills"].unique()

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(skills)

    model = KMeans(n_clusters=n_clusters, random_state=42)
    model.fit(X)

    clusters = {}

    for skill, label in zip(skills, model.labels_):
        clusters.setdefault(label, []).append(skill)

    return clusters