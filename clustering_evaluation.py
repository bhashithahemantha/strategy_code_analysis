import encoding_data as ed
import pandas as pd
import numpy as np
import csv
import category_encoders as ce
from sklearn import metrics
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics.cluster import silhouette_score
import progressbar
from sklearn.metrics import davies_bouldin_score
from clustering_analysis import k_means_clustering
from data_store_retrieve import DatabaseModel

np.seterr(divide='ignore', invalid='ignore')

data_retrieved = DatabaseModel('CL_30').find_all({})
# drop _id from mongo
data_frame_toencode = pd.DataFrame(data_retrieved).drop(['_id', 'strategy_id'], axis=1)
# label encoding
data = ed.data_encoding(data_frame_toencode)



# Elbow method
# def elbow_method_plot(cluster_data):
#     fig, curve = plt.subplots()
#     plt.xticks (np.arange (0, 256, step=10))
#     curve.plot(cluster_data.num_clusters, cluster_data.cluster_errors)
#     curve.set(xlabel='Number of clusters', ylabel='Cluster error', title='Elbow Method Analysis')
#     curve.grid()
#     plt.show()


# calling elbow method and silhouette method
# method inputs
num_cluster = []
elbow_cluster_error = []
calinski_harabaz_score_array = []
davies_bouldin_index_array = []
silhouette_avg_array = []
# for hold kmeans values
k_value_error = []
labels = 0
values = 0

min_number_of_clusters = 2
max_number_of_clusters = 50
step_size = 1
# progress bar
bar = progressbar.ProgressBar(maxval = max_number_of_clusters).start()
# looping through the dataset
for i in range(min_number_of_clusters, max_number_of_clusters):
    kmeans = KMeans(i)
    labels =kmeans.fit_predict(data)
    values = kmeans.fit_transform(data)
    k_value_error.append([i,kmeans.inertia_])

    # inputs for elbow method
    clustered_data = k_means_clustering(data, i)
    num_cluster.append(clustered_data[0][0])
    elbow_cluster_error.append(clustered_data[0][1])

    # # cluster evaluation
    # calinski_harabaz_score = metrics.calinski_harabaz_score(data, labels)
    # calinski_harabaz_score_array.append(calinski_harabaz_score)
    #
    # davies_bouldin_index = davies_bouldin_score(data, labels)
    # davies_bouldin_index_array.append(davies_bouldin_index)
    #
    # silhouette_avg = silhouette_score(data, labels)
    # silhouette_avg_array.append(silhouette_avg)

    bar.update(i)

# plt.figure(figsize=(80, 60))
# plt.plot(num_cluster, calinski_harabaz_score_array, linewidth=3, color='red')
# plt.title("calinski_harabaz_score")
# plt.xlabel("number of clusters")
# plt.ylabel("calinski_harabaz_score")
# plt.grid(linestyle='-', linewidth=1)
# plt.xticks(np.arange(min_number_of_clusters, max_number_of_clusters, step=step_size), rotation='vertical')
# plt.savefig("/Users/bhashi/PycharmProjects/strategy_code_analysis/figures/k-means/calinski_harabaz_score")
# # # plt.show()
# #
# plt.figure(figsize=(80, 60))
# plt.plot(num_cluster, davies_bouldin_index_array, linewidth=2, color='red')
# plt.title("davies_bouldin_index")
# plt.xlabel("number of clusters")
# plt.ylabel("davies_bouldin_index")
# plt.grid(linestyle='-', linewidth=1)
# plt.xticks(np.arange(min_number_of_clusters, max_number_of_clusters, step=step_size), rotation='vertical')
# plt.savefig("/Users/bhashi/PycharmProjects/strategy_code_analysis/figures/k-means/davies_bouldin_index")
# # # plt.show()
#
# plt.figure(figsize=(80, 60))
# plt.plot(num_cluster, silhouette_avg_array, linewidth=1, color='red')
# plt.title("silhouette_avg")
# plt.xlabel("number of clusters")
# plt.ylabel("silhouette_avg")
# plt.grid(linestyle='-', linewidth=1)
# plt.xticks(np.arange(min_number_of_clusters, max_number_of_clusters, step=step_size), rotation='vertical')
# plt.savefig("/Users/bhashi/PycharmProjects/strategy_code_analysis/figures/k-means/silhouette_avg")
# # plt.show()

# plt.figure(figsize=(80, 60))
# plt.plot(num_cluster, elbow_cluster_error, linewidth=3, color='red')
# plt.title("elbow_method")
# plt.xlabel("number of clusters")
# plt.ylabel("error")
# plt.grid(linestyle='-', linewidth=1)
# plt.xticks(np.arange(min_number_of_clusters, max_number_of_clusters, step=step_size), rotation='vertical')
# plt.savefig("/Users/bhashi/PycharmProjects/strategy_code_analysis/figures/k-means/elbow_method 2-50")
# plt.show()