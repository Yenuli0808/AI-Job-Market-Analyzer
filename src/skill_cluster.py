from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from preprocess import get_processed_data

CLUSTER_LABELS = [
    "💻 Programming & Development",
    "📊 Management & Governance",
    "⚙️ Data Engineering & Pipelines",
    "📈 Reporting & Analytics",
    "🤖 Machine Learning & AI",
]

def cluster_skills(n_clusters: int = 5) -> dict:
    df = get_processed_data()
    skills = df["job_skills"].unique()

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(skills)

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    model.fit(X)

    raw_clusters: dict[int, list] = {}
    for skill, label in zip(skills, model.labels_):
        raw_clusters.setdefault(int(label), []).append(skill)

    # Sort clusters by size descending → assign fixed labels by size rank
    sorted_ids = sorted(raw_clusters, key=lambda k: len(raw_clusters[k]), reverse=True)
    named = {}
    for rank, cluster_id in enumerate(sorted_ids):
        label = CLUSTER_LABELS[rank] if rank < len(CLUSTER_LABELS) else f"Cluster {rank}"
        named[label] = raw_clusters[cluster_id]

    return named