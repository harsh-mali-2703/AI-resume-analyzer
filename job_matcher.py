import math
import re
from collections import Counter


def _tokenize(text):
    return re.findall(r"[a-z0-9+#.]+", text.lower())


def _tfidf_vectors(documents):
    tokenized_docs = [_tokenize(doc) for doc in documents]
    doc_count = len(tokenized_docs)
    vocabulary = sorted(set(token for doc in tokenized_docs for token in doc))

    # Document frequency is needed for the IDF part of TF-IDF.
    document_frequency = {}
    for token in vocabulary:
        document_frequency[token] = sum(1 for doc in tokenized_docs if token in doc)

    vectors = []
    for doc in tokenized_docs:
        counts = Counter(doc)
        total_words = len(doc) or 1
        vector = []
        for token in vocabulary:
            tf = counts[token] / total_words
            idf = math.log((doc_count + 1) / (document_frequency[token] + 1)) + 1
            vector.append(tf * idf)
        vectors.append(vector)

    return vectors


def _cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    length_a = math.sqrt(sum(a * a for a in vector_a))
    length_b = math.sqrt(sum(b * b for b in vector_b))

    if length_a == 0 or length_b == 0:
        return 0
    return dot_product / (length_a * length_b)


def build_role_text(role):
    return " ".join(
        [
            str(role["job_role"]),
            str(role["required_skills"]),
            str(role.get("description", "")),
        ]
    )


def calculate_role_matches(cleaned_resume_text, jobs_df):
    role_texts = [build_role_text(row) for row in jobs_df]
    documents = [cleaned_resume_text] + role_texts

    # The first vector is the resume; the remaining vectors represent the available job roles.
    tfidf_vectors = _tfidf_vectors(documents)
    resume_vector = tfidf_vectors[0]
    role_vectors = tfidf_vectors[1:]
    scores = [_cosine_similarity(resume_vector, role_vector) for role_vector in role_vectors]

    results = []
    for index, score in enumerate(scores):
        role = jobs_df[index]
        results.append(
            {
                "job_role": role["job_role"],
                "score": round(float(score) * 100, 2),
                "required_skills": role["required_skills"],
            }
        )

    return sorted(results, key=lambda item: item["score"], reverse=True)


def get_role_by_name(jobs_df, role_name):
    # Keep this lookup explicit so a missing role gives a clear error message.
    for role in jobs_df:
        if role["job_role"] == role_name:
            return role
    raise ValueError("Selected role was not found in dataset")
