This repository contains my work on Botnet Detection.

During the work I have mainly worked on two dataset ISCX Botnet Dataset and CTU University Dataset.

Ipython notebook folder contains the implementation of different algorithms for botnet detection. 

During initial stages of my project I have implemented Botnet Clustering Algorithm based on Bclus method presented in thesis Identifying, Modeling and Detecting Botnet Behaviors in the Network by S. Gracia. The method uses combination of supervised and unsupervised learning for classification and shows encouraging results. The code can be found in Bclus.ipynb notebook.

The code is further modified to a realtime method in which instead of using Decision Tree over Cluster we trained a classifier to predict clusters to which incomming traffic will belong to. On the basis of their cluster labels we are prediciting the maliciousness of the flows.




