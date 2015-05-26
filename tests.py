from glob import glob
from eclair.models import Email
from eclair.heuristics import guess_signatures
from flanker.mime.message.errors import DecodingError

files = glob('data/rubio_emails/*.eml')

emails = []
for file in files:
    with open(file, 'r') as f:
        data = f.read()

    try:
        emails.append( Email(data) )

    # Malformed email
    except DecodingError:
        continue

from eclair.network import build_network
build_network(emails)

foo

guess_signatures(emails)

import numpy as np
from eclair.text import clean_doc, Vectorizer
from scipy.spatial.distance import pdist, squareform
vectr = Vectorizer()
docs = [clean_doc(e.body) for e in emails]
vecs = vectr.vectorize(docs, train=True)

dists = pdist(vecs.todense(), metric='cosine')
print('Mean distance is: {0}'.format(np.nanmean(dists)))
print('Median distance is: {0}'.format(np.median(dists)))

# Set nans to a large distance
dists[np.isnan(dists)] = 99999.

dists = squareform(dists)

import os
import shutil
from sklearn.cluster import DBSCAN

outdir = 'debug'
if os.path.exists(outdir):
    shutil.rmtree(outdir)
os.makedirs(outdir)

for eps in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.]:
    print('EPS: {0}'.format(eps))
    m = DBSCAN(metric='precomputed', eps=eps, min_samples=3)
    print(dists.shape)
    y = m.fit_predict(dists)

    n = max(y) + 1

    if n == 0:
        print('NO CLUSTERS')

    else:
        clusters = [[] for _ in range(n)]
        for i, doc in enumerate(docs):
            clusters[y[i]].append(doc)

        print('num clusters:')
        print(len(clusters))
        print('total num emails:')
        print(sum([len(clus) for clus in clusters]))
        print('cluster sizes:')
        print([len(clus) for clus in clusters])


        eps_dir = os.path.join(outdir, 'eps_{0}'.format(eps))
        os.makedirs(eps_dir)
        for i, clus in enumerate(clusters):
            clus_dir = os.path.join(eps_dir, 'clus_{0}'.format(i))
            os.makedirs(clus_dir)
            for j, c in enumerate(clus):
                outfile = os.path.join(clus_dir, '{0}.txt'.format(j))
                with open(outfile, 'w') as f:
                    f.write(c.encode('utf-8'))

print('done')


