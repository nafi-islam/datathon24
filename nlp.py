import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

embedding_model = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")

words = ["EXPONENT", "POWER", "RADICAL", "ROOT",
         "BENT", "GNARLY", "TWISTED", "WARPED",
         "LICK", "OUNCE", "SHRED", "TRACE",
         "BATH", "POWDER", "REST", "THRONE"]

# Step 1
embeddings = [np.mean(embedding_model(word)[0], axis=0) for word in words]

# Step 2
kmeans = KMeans(n_clusters=4, random_state=0, n_init=10).fit(embeddings)
labels = kmeans.labels_

# Step 3
clusters = {i: [] for i in range(4)}
for idx, label in enumerate(labels):
    clusters[label].append((words[idx], embeddings[idx]))

# Step 4: 4 words and cosine similarity
refined_clusters = {}
for cluster_id, word_embeddings in clusters.items():
    if len(word_embeddings) > 4:
        # cosine similarities within a cluster
        cluster_embeddings = np.array([embedding for _, embedding in word_embeddings])
        similarity_matrix = cosine_similarity(cluster_embeddings)

        # choose 4 words with highest average similarity in each cluster
        avg_similarities = similarity_matrix.mean(axis=1)
        top_indices = np.argsort(avg_similarities)[-4:]

        refined_clusters[cluster_id] = [word_embeddings[i][0] for i in top_indices]
    else:
        # if the cluster has 4 or fewer words, keep all of them
        refined_clusters[cluster_id] = [word for word, _ in word_embeddings]

# check exactly 4 words per cluster 
for cluster_id in refined_clusters:
    if len(refined_clusters[cluster_id]) < 4:
        remaining_words = [word for word in words if word not in sum(refined_clusters.values(), [])]
        remaining_embeddings = [embedding_model(word)[0] for word in remaining_words]
        
        # calculate cosine similarity to the cluster center
        cluster_center = kmeans.cluster_centers_[cluster_id]
        distances = [(remaining_words[i], np.linalg.norm(embedding - cluster_center)) for i, embedding in enumerate(remaining_embeddings)]
        distances.sort(key=lambda x: x[1])
        
        # add the closest words until cluster has 4
        refined_clusters[cluster_id].extend([word for word, _ in distances[:4 - len(refined_clusters[cluster_id])]])

for cluster_id, words_in_cluster in refined_clusters.items():
    print(f"Cluster {cluster_id + 1}: {words_in_cluster}")
