# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 15:14:00 2016

@author: othree
"""
import pandas as pd
import numpy as np

######################################################################################
def getLabeledFeaturesGMM(features_array):
    X_train = features_array
    from sklearn import mixture
    #Number of clusters = number of components
    # Four covariance Type ['spherical', 'diag', 'tied', 'full'] iterations can be changed
    clf = mixture.GMM(n_components=15, covariance_type='full', n_iter=20)
    label = clf.fit_predict(X_train)
    label =  pd.DataFrame(label)
    label = label.rename(columns={0:'label'})
    return label           

def addLabelTofeatures(features, label):
    labeled_features = features.copy()
    labeled_features['label'] = label
    return labeled_features
##################################################################################### 


###############################################################################
def meanShift(features_array):
    X = features_array
    #Applying GMM for clustering
    from sklearn.cluster import MeanShift, estimate_bandwidth
    # Compute clustering with MeanShift

    # The following bandwidth can be automatically detected using
    bandwidth = estimate_bandwidth(X, quantile=0.2)
    
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    
    print("number of estimated clusters : %d" % n_clusters_)
    # Plot result
    import matplotlib.pyplot as plt
    from itertools import cycle
    
    plt.figure(1)
    plt.clf()
    
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
    labels = pd.DataFrame(labels)
    return labels
###############################################################################
    
###############################################################################
def kproto(features_array):
    from kmodes import kprototypes
    kproto = kprototypes.KPrototypes(n_clusters=20, init='Cao', verbose=2)
    clusters = kproto.fit_predict(features_array, categorical= [])
    centroids = kproto.cluster_centroids_
    labels = kproto.labels_
    return labels
###############################################################################
