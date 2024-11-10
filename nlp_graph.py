import numpy as np
import networkx as nx
import community.community_louvain as community_louvain 
from scipy.special import expit
from itertools import combinations

# input
words = ["EXPONENT", "POWER", "RADICAL", "ROOT",
         "BENT", "GNARLY", "TWISTED", "WARPED",
         "LICK", "OUNCE", "SHRED", "TRACE",
         "BATH", "POWDER", "REST", "THRONE"]

# Generate synthetic embeddings for each word (placeholder) -- ??
# In a real implementation, replace this with embeddings from a pre-trained language model -- Insert Word2Vec Here?
rng = np.random.default_rng(seed=42)
word_embeddings = rng.normal(size=(len(words), 50))  # Assume 50-dimensional embeddings

# Build the graph with weighted edges
G = nx.Graph()
for i, word in enumerate(words):
    G.add_node(i, label=word)

for i, j in combinations(range(len(words)), 2):
    # Directly calculate the belief score
    similarity_score = np.dot(word_embeddings[i], word_embeddings[j]) / (
        np.linalg.norm(word_embeddings[i]) * np.linalg.norm(word_embeddings[j])
    )
    belief_score = expit(similarity_score)  # [0, 1] range
    G.add_edge(i, j, weight=belief_score)

# Use the Louvain algorithm with a resolution parameter to perform community detection
partition = community_louvain.best_partition(G, weight='weight', resolution=1.0)

# Organize nodes by community
clusters = {}
for node, community_id in partition.items():
    clusters.setdefault(community_id, []).append(words[node])

# Ensure we have exactly four clusters of four words
def refine_clusters(clusters):
    # Flatten clusters into individual lists
    flat_clusters = [c for c in clusters.values()]
    
    # Split clusters larger than 4 words
    refined_clusters = []
    for cluster in flat_clusters:
        while len(cluster) > 4:
            refined_clusters.append(cluster[:4])
            cluster = cluster[4:]
        if cluster:
            refined_clusters.append(cluster)

    # Merge small clusters until exactly four remain
    while len(refined_clusters) > 4:
        smallest = min(refined_clusters, key=len)
        refined_clusters.remove(smallest)
        refined_clusters[0].extend(smallest)

    return refined_clusters[:4]  # Return only the first four clusters

# Refine clusters to get exactly four groups of four
final_clusters = refine_clusters(clusters)

# Print the final four clusters
for i, cluster in enumerate(final_clusters, 1):
    print(f"Cluster {i}: {', '.join(cluster)}")
