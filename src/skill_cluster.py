from preprocess import get_processed_data

# Keyword rules for each cluster — order matters (first match wins)
CLUSTER_RULES = [
    ("🤖 Machine Learning & AI", [
        "machine learning", "deep learning", "nlp", "natural language",
        "computer vision", "tensorflow", "pytorch", "keras", "scikit",
        "artificial intelligence", "neural", "llm", "bert", "gpt",
        "xgboost", "reinforcement", "classification", "regression",
        "clustering", "hugging", "transformer", "model", "prediction",
    ]),
    ("💻 Programming & Development", [
        "python", "java", "scala", "r", "c++", "javascript", "typescript",
        "sql", "bash", "shell", "go", "rust", "ruby", "php", "matlab",
        "programming", "software", "development", "coding", "algorithm",
        "data structures", "oop", "api", "microservices", "rest",
    ]),
    ("⚙️ Data Engineering & Pipelines", [
        "kafka", "spark", "hadoop", "airflow", "etl", "pipeline",
        "data engineering", "data lake", "data warehouse", "flink",
        "hive", "presto", "nifi", "dbt", "ingestion", "streaming",
        "batch", "databricks", "glue", "data integration",
    ]),
    ("☁️ Cloud & Databases", [
        "aws", "azure", "gcp", "cloud", "s3", "ec2", "redshift",
        "bigquery", "snowflake", "mysql", "postgresql", "mongodb",
        "cassandra", "redis", "dynamodb", "oracle", "database",
        "nosql", "storage", "kubernetes", "docker", "terraform",
    ]),
    ("📊 Analytics & Reporting", [
        "tableau", "power bi", "looker", "excel", "data analysis",
        "data visualization", "analytics", "reporting", "dashboard",
        "statistics", "business intelligence", "insight", "kpi",
        "metrics", "qlik", "data science", "pandas", "numpy",
    ]),
    ("📋 Management & Soft Skills", [
        "communication", "leadership", "project management", "agile",
        "scrum", "teamwork", "collaboration", "problem solving",
        "stakeholder", "mentoring", "presentation", "analytical",
        "time management", "adaptability", "critical thinking",
    ]),
]

def cluster_skills(n_clusters: int = 6) -> dict:
    """Group skills by semantic category using keyword rules."""
    df = get_processed_data()
    skills = df["job_skills"].dropna().unique().tolist()

    clusters: dict[str, list] = {label: [] for label, _ in CLUSTER_RULES}
    clusters["🔧 Other Technical"] = []

    for skill in skills:
        skill_lower = skill.lower().strip()
        assigned = False
        for label, keywords in CLUSTER_RULES:
            if any(kw in skill_lower for kw in keywords):
                clusters[label].append(skill)
                assigned = True
                break
        if not assigned:
            clusters["🔧 Other Technical"].append(skill)

    # Remove empty clusters
    clusters = {k: v for k, v in clusters.items() if v}
    return clusters