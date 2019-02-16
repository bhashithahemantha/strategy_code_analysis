import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from data_store_retrieve import DatabaseModel
import encoding_data as ed
from sklearn.cluster import MeanShift, estimate_bandwidth



# #############################################################################
data_retrieved = DatabaseModel('CL_30').find_all({})
# drop _id from mongo
data = pd.DataFrame(data_retrieved).drop(['_id'], axis=1)
data = ed.data_encoding(data)
# data = StandardScaler().fit_transform(data)


# #############################################################################
# Compute DBSCAN
# db = DBSCAN(eps=0.3, min_samples=10).fit(data)
# core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
# core_samples_mask[db.core_sample_indices_] = True
# labels = db.labels_
# # Number of clusters in labels, ignoring noise if present.
# n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
# n_noise_ = list(labels).count(-1)

# #############################################################################
# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
bandwidth = estimate_bandwidth(data)

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(data)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

# #############################################################################
