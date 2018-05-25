import sys
import zss
# 1

import matplotlib.pyplot as plt
import pickle as cPickle
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


pickle_followers = open("C://Users//BKUCINSK//Documents//Docker//Magister//kmeansTest.pickle", "rb")
df = cPickle.load(pickle_followers)
kmeans = KMeans(n_clusters=10)
colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'brown', 6: 'gold', 7: 'navy', 8: 'tan', 9: 'olive', 10: 'lightpink'}

kmeans.fit(df)
labels = kmeans.predict(df)
centroids = kmeans.cluster_centers_

head = kmeans.inertia_

closest, _ = pairwise_distances_argmin_min(centroids, df)
print(closest)

fig = plt.figure(figsize=(5, 5))

colors = map(lambda x: colmap[x+1], labels)

plt.scatter(df['y'], df['x'], color=list(colors), alpha=0.5, edgecolor='k')
for idx, centroid in enumerate(centroids):
    plt.scatter(*centroid, color=colmap[idx+1])
plt.xlim(0, 120)
plt.ylim(0, 2880)
plt.show()