import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from sklearn.cluster import AffinityPropagation
from sklearn.metrics.cluster import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

# KMeans Model
def k_means_clustering(data, k, graph=False):
    km = KMeans(n_clusters=k)
    cluster_labels = km.fit_predict(data)

    inertia = km.inertia_

    # Plotting
    if graph:
        labels = km.labels_
        plt.figure(figsize=(8, 8))
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=labels.astype(np.float), marker='o', alpha=0.5)
        plt.xlabel('Principle component 1')
        plt.ylabel('Principle component 2')
        plt.title("K Means - k=" + str(k), fontsize=14)
        plt.show()

    return [[k, inertia], cluster_labels]


# DBSCAN Model
def db_scan(data, eps, min_samples):
    data = StandardScaler().fit_transform (data)
    # Compute DBSCAN
    db = DBSCAN(eps=eps, min_samples=min_samples).fit (data)
    core_samples_mask = np.zeros_like (db.labels_, dtype=bool)
    core_samples_mask[ db.core_sample_indices_ ] = True
    labels = db.labels_
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len (set (labels)) - (1 if -1 in labels else 0)
    n_noise_ = list (labels).count (-1)


# Gaussian Mixture Model
def gmm_clustering(data, k, graph=False):
    gmm = GaussianMixture(n_components=k)
    gmm.fit(data)

    posterior_probabilities = gmm.predict_proba(data)
    gmm_labels = gmm.predict(data)
    aic = gmm.aic(data)
    bic = gmm.bic(data)

    # Plotting
    if graph:
        colored_arrays = np.matrix(posterior_probabilities)
        colored_tuples = [tuple(i.tolist()[0]) for i in colored_arrays]
        plt.figure(figsize=(8, 8))
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=colored_tuples, marker='o', alpha=0.5)
        plt.title("Gaussian Mixture Model", fontsize=14)
        plt.show()

    return [k, aic, bic, gmm_labels, posterior_probabilities]

# KMedoids Model
def kMedoids(D, k, tmax=100):
    # determine dimensions of distance matrix D
    m, n = D.shape
    if k > n:
        raise Exception('too many medoids')
    # find a set of valid initial cluster medoid indices since we
    # can't seed different clusters with two points at the same location
    valid_medoid_inds = set(range(n))
    invalid_medoid_inds = set([])
    rs,cs = np.where(D==0)
    # the rows, cols must be shuffled because we will keep the first duplicate below
    index_shuf = list(range(len(rs)))
    np.random.shuffle(index_shuf)
    rs = rs[index_shuf]
    cs = cs[index_shuf]
    for r,c in zip(rs,cs):
        # if there are two points with a distance of 0...
        # keep the first one for cluster init
        if r < c and r not in invalid_medoid_inds:
            invalid_medoid_inds.add(c)
    valid_medoid_inds = list(valid_medoid_inds - invalid_medoid_inds)
    if k > len(valid_medoid_inds):
        raise Exception('too many medoids (after removing {} duplicate points)'.format(
            len(invalid_medoid_inds)))
    # randomly initialize an array of k medoid indices
    M = np.array(valid_medoid_inds)
    np.random.shuffle(M)
    M = np.sort(M[:k])
    # create a copy of the array of medoid indices
    Mnew = np.copy(M)
    # initialize a dictionary to represent clusters
    C = {}
    for t in range(tmax):
        # determine clusters, i. e. arrays of data indices
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]
        # update cluster medoids
        for kappa in range(k):
            J = np.mean(D[np.ix_(C[kappa],C[kappa])],axis=1)
            j = np.argmin(J)
            Mnew[kappa] = C[kappa][j]
        np.sort(Mnew)
        # check for convergence
        if np.array_equal(M, Mnew):
            break
        M = np.copy(Mnew)
    else:
        # final update of cluster memberships
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]
    # return results
    return M, C


def affinity_propagation(data):
    # Compute Affinity Propagation
    af = AffinityPropagation ()
    labels = af.fit_predict(data)
    sil_score = silhouette_score(data, labels)
    return sil_score


