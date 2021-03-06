# -*- coding: utf-8 -*-
"""DT-Counterfactual_Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nPn2586WCF6S3V9b9NLqX8ug5el2dwWW
"""

############# Initialise on Google Colab 
from google.colab import drive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
#from google.colab import auth
#from oauth2client.client import GoogleCredentials 
drive.mount('/content/gdrive', force_remount=True)
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
gdrive = GoogleDrive(gauth)
gdrive.CreateFile({"id": "1wwSN3AIl_dmayKENu5jnc1BRaNPe8BZc"}).GetContentFile("learning.py")

#### Installing Deps ####
#!pip3 install pyAgrum
#!pip3 install alibi



#### Removing str encoding error ####
# !python3 -m pip install 'h5py==2.10.0' --force-reinstall

!pip install alibi

!pip install pyAgrum

# Commented out IPython magic to ensure Python compatibility.
import os

import tensorflow as tf
tf.get_logger().setLevel(40) # suppress deprecation messages
tf.compat.v1.disable_v2_behavior() # disable TF2 behaviour as alibi code still relies on TF1 constructs

### Alibi lib.
from alibi.explainers import CounterFactualProto, CounterFactual

import numpy as np
import pandas as pd

from learning import *
from time import time

### Plotting
import matplotlib
import matplotlib.pyplot as plt
from IPython.display import display
from enum import Enum
# %matplotlib inline


## DT
from sklearn import tree
from sklearn import datasets
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
import pydotplus
from sklearn.model_selection import train_test_split

print('TF version: ', tf.__version__)
print('Eager execution enabled (DiCE should be True, Alibi should be False): ', tf.executing_eagerly()) # False
seed = 123
tf.random.set_seed(seed)
np.random.seed(seed)

data=pd.read_csv('gdrive/My Drive//Counterfactual-prototype-main/datasets/diabetes.csv')

# Giving current root path
PATH = "gdrive/My Drive//Counterfactual-prototype-main/"

# name of dataset
DATASET_NAME = "diabetes.csv"

# variable containing the class labels in this case the dataset contains:
# 0 - if not diabetes
# 1 - if diabetes
class_var = "Outcome"

# load dataset
dataset_path = PATH + "datasets/" + DATASET_NAME
data = pd.read_csv( dataset_path )

# features
feature_names = data.drop([class_var], axis=1).columns.to_list()

# balance dataset
sampled_data = data.sample(frac=1)
sampled_data = sampled_data[ sampled_data["Outcome"] == 0]

no_data = sampled_data.sample(frac=1)[0:268]
yes_data = data[ data["Outcome"] == 1]

balanced_data = [no_data,yes_data]
balanced_data = pd.concat(balanced_data)

#split dataset in features and target variable
feature_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
X = balanced_data[feature_names] # Features
y = balanced_data.Outcome # Target variable

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

feature_names

"""## Building Decision Tree Model

"""

# Create Decision Tree classifer object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

"""## Evaluating Model"""

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

"""## Visualizing Decision Trees"""

from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus

dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = feature_cols,class_names=['0','1'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('diabetes.png')
Image(graph.create_png())

"""## Optimizing Decision Tree Performance"""

# Create Decision Tree classifer object
clf = DecisionTreeClassifier(criterion="entropy", max_depth=3)

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

"""## Visualizing Decision Trees"""

from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus
dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True, feature_names = feature_cols,class_names=['0','1'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('diabetes.png')
Image(graph.create_png())

# Decision Tree Classification in Python
# https://www.datacamp.com/community/tutorials/decision-tree-classification-python

