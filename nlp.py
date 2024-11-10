import random
import spacy
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# spaCy's English model
nlp = spacy.load("en_core_web_lg")

# Define words
# words = ["BENT", "OUNCE", "TWISTED", "ROOT", "LICK", "POWER", "SHRED", "WARPED", "BATH", 
#          "POWDER", "REST", "TRACE", "EXPONENT", "GNARLY", "RADICAL", "THRONE"]

# Output:
# Cluster 1: ['EXPONENT', 'RADICAL', 'POWDER', 'SHRED']
# Cluster 2: ['POWER', 'REST', 'TRACE', 'ROOT']
# Cluster 3: ['LICK', 'BATH', 'TWISTED', 'THRONE']
# Cluster 4: ['BENT', 'GNARLY', 'WARPED', 'OUNCE']

# words = ["JAGUAR", "TIGER", "LION", "CHEETAH", "BLUE", "PINK", "RED", "YELLOW",
#          "BEST BOY", "KRONER", "IDEA", "STABLES", "STEER", "DIRECT", "GUIDE", "LEAD"]

# Output: 
# Cluster 1: ['BLUE', 'RED', 'PINK', 'YELLOW']
# Cluster 2: ['JAGUAR', 'LION', 'CHEETAH', 'TIGER']
# Cluster 3: ['GUIDE', 'STABLES', 'BEST BOY', 'DIRECT']
# Cluster 4: ['IDEA', 'LEAD', 'STEER', 'KRONER']

# words = ["apple", "banana", "car", "truck", "strawberry", "peach", "engine", "tire", 
#          "phone", "laptop", "monitor", "keyboard","guitar", "drum", "piano", "flute"]

# Output:
# Cluster 1: ['peach', 'banana', 'apple', 'strawberry']
# Cluster 2: ['laptop', 'phone', 'monitor', 'keyboard']
# Cluster 3: ['truck', 'car', 'tire', 'engine']
# Cluster 4: ['drum', 'piano', 'flute', 'guitar']

# words = ['Tizzy', 'Rapid', 'Wave', 'Normal', 'Rinse', 'Quick', 'Shape', 'Sweat',
#          'Sanitize', 'Health', 'Lather', 'Cascade', 'Stew', 'Current', 'Form', 'Condition']

# words = ["BUNS", "BUNK", "CANOPY","SEAT", "LIFESAVER", "DONUT", "BOTTOM", "FEZ",
#          "BOWLER", "CHEERIO", "FEDORA", "TRUNDLE", "MURPHY", "BAGEL", "TAIL", "BERET"]

# Output:
# Cluster 1: ['Tizzy', 'Sweat', 'Lather', 'Form']
# Cluster 2: ['Normal', 'Cascade', 'Rapid', 'Quick']
# Cluster 3: ['Wave', 'Shape', 'Condition', 'Health']
# Cluster 4: ['Current', 'Stew', 'Sanitize', 'Rinse']

# words = ['link', 'horseshoe', 'pencil', 'walrus', 'toward', 'date', 'bond', 'relation',
#         'concerning', 'space', 'tie', 'handlebar', 'about', 'on', 'dutch', 'jeopardy']

# Output:
# Cluster 1: ['date', 'horseshoe', 'walrus', 'tie']
# Cluster 2: ['about', 'relation', 'toward', 'concerning']
# Cluster 3: ['handlebar', 'jeopardy', 'bond', 'space']
# Cluster 4: ['dutch', 'on', 'link', 'pencil']

# words = ["biotin", "sepak", "twister", "sorry", "finland", "riboflavin", "niacin","boccia", 
#          "kabaddi", "risk", "chess", "sweden", "iceland", "folate", "denmark", "jai-alai"]

# Output:
# Cluster 1: ['finland', 'denmark', 'sweden', 'iceland']
# Cluster 2: ['biotin', 'niacin', 'folate', 'riboflavin']
# Cluster 3: ['risk', 'sorry', 'jai-alai', 'chess']
# Cluster 4: ['twister', 'kabaddi', 'boccia', 'sepak']

words = ["cask", "cylinder", "drum", "tank", "pilot", "shepard", "steer", "usher",
         "cowboy", "jet", "ram", "raven", "golfer", "pendulum", "saloon doors", "swing"]

# Output:
# Cluster 1: ['shepard', 'raven', 'cylinder', 'tank']
# Cluster 2: ['pendulum', 'swing', 'drum', 'golfer']
# Cluster 3: ['steer', 'cask', 'jet', 'cowboy']
# Cluster 4: ['saloon doors', 'pilot', 'usher', 'ram']

random.shuffle(words)

print("Shuffled words:", words)

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
