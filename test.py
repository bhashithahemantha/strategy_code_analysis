# import numpy as np
# from kmodes.kmodes import KModes
from data_store_retrieve import DatabaseModel
import pandas as pd
from sklearn.metrics.cluster import silhouette_score
import matplotlib.pyplot as plt
# import progressbar
# from sklearn.preprocessing import normalize
# from sklearn.cluster import AffinityPropagation
# from sklearn import metrics
import encoding_data as ed
import clustering_analysis as ca
import progressbar

#
#
data_retrieved = DatabaseModel('CL_30').find_all({})

# drop _id from mongo
data = pd.DataFrame(data_retrieved).drop(['_id'], axis=1)

data = ed.data_encoding(data)


# coding: utf-8
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np

# 3 points in dataset
data = data.values

# distance matrix
D = pairwise_distances(data, metric='euclidean')

# split into  clusters
M, C = ca.kMedoids(D, 3)
labels = []
print('medoids:')
for point_idx in M:
    print( data[point_idx] )

print('')
print('clustering result:')
for label in C:
    for point_idx in C[label]:
        print('label {0}:　{1}'.format(label, data[point_idx]))
        labels.append(label)
sil_score = silhouette_score (D, labels)
print (sil_score)


# ---------------------------------------------------------------
# silhouette_avg_array = []
# labels = [ ]
# num_cluster = []
# min_number_of_clusters = 2
# max_number_of_clusters = 100
# step_size = 1
# # progress bar
# bar = progressbar.ProgressBar(maxval = max_number_of_clusters).start()
# # looping through the dataset
# for i in range(min_number_of_clusters, max_number_of_clusters):
#     # split into  clusters
#     M, C = ca.kMedoids (D, i)
#     num_cluster.append(len(M))
#     print ('medoids:')
#     for point_idx in M:
#         print (data[ point_idx ])
#
#     print ('')
#     print ('clustering result:')
#     for label in C:
#         for point_idx in C[ label ]:
#             print ('label {0}:　{1}'.format (label, data[ point_idx ]))
#             labels.append (label)
#         sil_score = silhouette_score (D, labels)
#         silhouette_avg_array.append(sil_score)

    # bar.update(i)

# plt.figure(figsize=(40, 30))
# plt.plot(num_cluster, silhouette_avg_array, linewidth=3, color='red')
# plt.title("silhouette_avg")
# plt.xlabel("number of clusters")
# plt.ylabel("silhouette_avg")
# plt.grid(linestyle='-', linewidth=1)
# plt.xticks(np.arange(min_number_of_clusters, max_number_of_clusters, step=step_size), rotation='vertical')
# # plt.savefig("/Users/bhashi/PycharmProjects/strategy_code_analysis/figures/k-means/silhouette_avg 2-100")
# plt.show()