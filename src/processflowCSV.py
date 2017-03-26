# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 20:46:08 2016

@author: othree
"""
#netflows are total count of occurence of a src_ip in a particular window
import pandas as pd
import numpy as np
#Edit path to the file for extracting features

def getFeatures(file_path):
    df=pd.read_csv(file_path)
    temp = pd.get_dummies(df.Tag)
    df['attack'] = temp.Attack
    df['normal'] = temp.Normal
    del temp, df['Tag']
    group = df.groupby(['bucket','source'])
    features = group.sourcePort.nunique()
    features = pd.DataFrame(features)
    features.rename(columns={'sourcePort':'usrc_port'},inplace=True)
    features['udest_ip'] = group.destination.nunique()
    features['udest_port'] = group.destinationPort.nunique()
    features['netflows'] = group.destination.count()
    features['bytes'] = group.totalSourceBytes.sum()
    features['packets'] = group.totalSourcePackets.sum()
    features['attack'] = group.attack.sum()
    features['normal'] = group.normal.sum()
    features.reset_index(inplace=True) 
    return features
    
def featurestoArray(features):
    #Converting DF to np array
    features_array = features.copy()
    del features_array['attack'],features_array['normal'],features_array['source'],features_array['bucket']
    features_array = np.array(features_array)
    return features_array

###############################################################################
def getLabeledFeaturesGMM(features_array):
    X_train = features_array
    from sklearn import mixture
    #Number of clusters = number of components
    # Four covariance Type ['spherical', 'diag', 'tied', 'full'] iterations can be changed
    clf = mixture.GMM(n_components=100, covariance_type='full', n_iter=100)
    label = clf.fit_predict(X_train)
    return label           

def addLabelTofeatures(features, label):
    labeled_features = features.copy()
    labeled_features['label'] = label
    return labeled_features
###############################################################################

###############################################################################
def getClusterFeatures(labeled_features):
    group = labeled_features.groupby(['label'])
    clusterfeatures = group.bucket.count()
    clusterfeatures = pd.DataFrame(clusterfeatures)
    clusterfeatures.rename(columns={'bucket':'instances'},inplace=True) 
    clusterfeatures['netflows']=group.netflows.sum()
    clusterfeatures['avgnetflows']=group.netflows.mean()
    clusterfeatures['stdnetflows']=group.netflows.std()
    clusterfeatures['usrc_ip']=group.source.nunique()
    clusterfeatures['avgsrc_port']=group.usrc_port.mean()
    clusterfeatures['stdsrc_port']=group.usrc_port.std()
    clusterfeatures['avgdest_ip']=group.udest_ip.mean()
    clusterfeatures['stddest_ip']=group.udest_ip.std()
    clusterfeatures['avgdest_port']=group.udest_port.mean()
    clusterfeatures['stddest_port']=group.udest_port.std()
    clusterfeatures['avgbytes']=group.bytes.mean()
    clusterfeatures['stdbytes']=group.bytes.std()
    clusterfeatures['avgpackets']=group.packets.mean()
    clusterfeatures['stdpackets']=group.packets.std()
    clusterfeatures['attack']=group.attack.sum()
    clusterfeatures['normal']=group.normal.sum()
    #True = Botnet    False = Normal
    clusterfeatures['label'] = (group.attack.sum()/group.normal.sum()>0.01)
    return clusterfeatures
###############################################################################

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import Imputer
file_path = "F:/MTP/Report/rep/labeled_flow_csv/ndf3.csv"
features = getFeatures(file_path=file_path)
X_train, X_test = train_test_split(features, test_size=0.4,random_state=0)

feature_array = featurestoArray(features=X_train)
label = getLabeledFeaturesGMM(features_array=feature_array)
X_train = addLabelTofeatures(features=X_train,label=label)
train_cluster_features = getClusterFeatures(labeled_features=X_train) 
train_labels = train_cluster_features['label']
del train_cluster_features['attack'],train_cluster_features['normal'],train_cluster_features['label']
train_cluster_features = Imputer.fit_transform(Imputer(strategy="most_frequent",axis=0),train_cluster_features)


feature_array = featurestoArray(features=X_test)
label = getLabeledFeaturesGMM(features_array=feature_array)
X_test = addLabelTofeatures(features=X_test,label=label)
test_cluster_features = getClusterFeatures(labeled_features=X_test)
test_labels = test_cluster_features['label']
del test_cluster_features['attack'],test_cluster_features['normal'],test_cluster_features['label'] 
test_cluster_features = Imputer.fit_transform(Imputer(strategy="most_frequent",axis=0),test_cluster_features)
del label, feature_array



train_cluster_features = train_cluster_features.astype(np.float32)
test_cluster_features = test_cluster_features.astype(np.float32)
train_labels = train_labels.astype(np.float32)
test_labels = test_labels.astype(np.float32)
###############################################################################
import sklearn.preprocessing
train_cluster_features= sklearn.preprocessing.normalize(train_cluster_features,axis=0)
test_cluster_features= sklearn.preprocessing.normalize(test_cluster_features,axis=0)

###############################################################################
#from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state=0)
clf.fit(train_cluster_features,train_labels)
label_predicted=clf.predict(test_cluster_features)
###############################################################################
from sklearn.metrics import confusion_matrix
confusion_matrix(test_labels, label_predicted)
print sum(abs(label_predicted-test_labels))
temp = X_test.groupby(['label'])
t = temp.packets.count()
label_predicted = [-1 if e == 0 else e for e in label_predicted]
test_labels = [-1 if e == 0 else e for e in test_labels]

pred = [a*b for a,b in zip(label_predicted,t)]
act =  [a*b for a,b in zip(test_labels,t)]
pp =0
pn = 0
nn = 0
np = 0
for a,b in zip(pred,act):
    if a>0 and b>0:
        pp +=a;
    elif a<0 and b<0:
        nn -= a;
    elif a>0 and b<0:
        pn += a;
    else :
        np += b;
print pp
print nn
print np
print pn
###############################################################################
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(train_cluster_features,train_labels)
label_predicted=gnb.predict(test_cluster_features)
gnb.score(test_cluster_features,test_labels)
###############################################################################