#!/usr/bin/env python

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Import all required packages
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

import sys

from tqdm import tqdm

import numpy as np
import MDAnalysis as md

import pandas

from collections import Counter

from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

import pickle

##-\-\-\-\-\-\-\-\-\-\
## Prepare the dataset
##-/-/-/-/-/-/-/-/-/-/

# Retrieve the dataset
dataset = pandas.read_csv('dataset_1.csv')

length = dataset.shape[1] - 1

array = dataset.values
X = array[:,0:length]
Y = array[:,length]

# Split the train and validation set into coordinates and distances
X_coord = X[:,0:100] # Coordinates
X_dist = X[:,100::] # Distances

##-\-\-\-\-\-\-\-\-\
## Prepare the models
##-/-/-/-/-/-/-/-/-/

# Get the algorithms
knn = KNeighborsClassifier()
svm_coord = SVC()
nb = GaussianNB()
svm_dist = SVC()

# Train the algorithms
knn.fit(X_coord,Y)
svm_coord.fit(X_coord,Y)
nb.fit(X_dist,Y)
svm_dist.fit(X_dist,Y)

##-\-\-\-\-\-\-\
## Save the model
##-/-/-/-/-/-/-/

models = [knn, svm_coord, nb, svm_dist]
pickle.dump(models, open('lipid_models.sav','wb'))
