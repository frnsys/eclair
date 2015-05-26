import math
from sklearn.cluster import KMeans
from nytnlp.clean import clean_doc
from eclair.text import Vectorizer
from time import time


def cluster(emails, n_clusters=None):
    # Vector reps
    vectr = Vectorizer()
    docs = [clean_doc(e.body) for e in emails]
    vecs = vectr.vectorize(docs, train=True)

    # Default to rule-of-thumb
    if n_clusters is None:
        n_clusters = int(math.sqrt(len(emails)/2))
    print('Looking for {0} clusters'.format(n_clusters))

    s = time()
    m = KMeans(n_clusters=n_clusters)
    labels = m.fit_predict(vecs)
    print('Took {0:.2f} seconds'.format(time() - s))

    clusters = [[] for _ in range(n_clusters)]
    for i, label in enumerate(labels):
        clusters[label].append(emails[i])

    print('Found these clusters with these sizes:')
    print([len(clus) for clus in clusters])

    return clusters
