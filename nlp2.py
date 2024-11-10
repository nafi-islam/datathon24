import spacy
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# spaCy's English model
nlp = spacy.load("en_core_web_lg")

# Define words
words = ["BENT", "OUNCE", "TWISTED", "ROOT", "LICK", "POWER", "SHRED", "WARPED", "BATH", 
         "POWDER", "REST", "TRACE", "EXPONENT", "GNARLY", "RADICAL", "THRONE"]

# embeddings using spaCy
word_vectors = [nlp(word).vector for word in words]

# similarity matrix using cosine similarity 
similarity_matrix = cosine_similarity(word_vectors)

# KMeans clustering
num_clusters = 4
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
labels = kmeans.fit_predict(word_vectors)

# group words by initial KMeans cluster assignment
clusters = {i: [] for i in range(num_clusters)}
for i, label in enumerate(labels):
    clusters[label].append(words[i])

# adjust clusters to ensure each has exactly four words
final_clusters = []
remaining_words = []

# get clusters with more or fewer than 4 words
for cluster_id, cluster_words in clusters.items():
    if len(cluster_words) == 4:
        final_clusters.append(cluster_words)
    else:
        remaining_words.extend(cluster_words)

# check clusters have exactly 4 words by adding remaining words
for cluster in final_clusters:
    if len(cluster) < 4:
        needed_words = 4 - len(cluster)
        cluster.extend(remaining_words[:needed_words])
        remaining_words = remaining_words[needed_words:]

# create new clusters for any remaining words in case of uneven distribution
while remaining_words:
    final_clusters.append(remaining_words[:4])
    remaining_words = remaining_words[4:]

# print the final clusters
for i, cluster_words in enumerate(final_clusters):
    print(f"Cluster {i + 1}: {cluster_words}")
