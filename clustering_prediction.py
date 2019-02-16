import pandas as pd
import pickle
from matplotlib import pyplot as plt
from clustering_analysis import k_means_clustering
from data_store_retrieve import DatabaseModel
from sklearn.cluster import KMeans
import encoding_data as ed


data_retrieved = DatabaseModel('CL_30').find_all({})
# drop _id from mongo
data_frame_toencode = pd.DataFrame(data_retrieved).drop(['_id', 'strategy_id'], axis=1)
# label encoding
data = ed.data_encoding(data_frame_toencode)

# calling kmeans
def kmeans_test(data, num_clusters):
    all_data = []
    model = KMeans(n_clusters=num_clusters)
    labels = model.fit_predict(data.values)
    filename = '/Users/bhashi/PycharmProjects/strategy_code_analysis/figures/k-means/trained_kmeans_model.sav'
    pickle.dump (model, open (filename, 'wb'))
    # for i in range(1,34):
    #     plt.figure(figsize=(8,6))
    #     plt.scatter(data[:,0],data[:,i],c=model.labels_.astype(float))
    #     plt.title("feature: "+data.columns[0]+" vs "+" feature: "+data.columns[i])
    #     plt.show()
    # print("error : ",model.inertia_)
    # print("centroids : ",model.cluster_centers_)
kmeans_test(data, 38)

# predicting the label of a given data point
# pred = model.predict(data.iloc[2:3,:])
# print("predicted label : ",pred)

# --------------------------------------------------------------------

# calling k medoids
# from data_extraction import get_data
# from sklearn.metrics.pairwise import pairwise_distances
# import pandas as pd
# import numpy as np
# from clustering_analysis import kMedoids
#
# # dataset
# data = pd.DataFrame(get_data())
# data = data.fillna(0).values
#
# # distance matrix
# D = pairwise_distances(data, metric='euclidean')
#
# # split into clusters
# M, C = kMedoids(D, 3)
#
# print('medoids:')
# for point_idx in M:
#     # print( data[point_idx] )
#     print(point_idx)
# print('')
# print('clustering result:')
# output =[]
# for label in C:
#     for point_idx in C[label]:
#         print('label {0}:　{1}'.format(label, data[point_idx]))
#         output.append([label,data[point_idx]])

# -------------------------------------------------------------

# save the model to disk
# filename = 'trained_kmeans_model.sav'
# pickle.dump (model, open (filename, 'wb'))

# some time later...
# load the model from disk
# loaded_model = pickle.load (open (filename, 'rb'))