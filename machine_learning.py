# -*- coding: utf-8 -*-
"""Machine Learning

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ebo0g2Qx2wFVVu6wbxVaS0LRx7iwkrvn
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score , f1_score
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import  GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import scale
# %matplotlib inline

from google.colab import files
upload = files.upload()

data = pd.read_csv('data_minicurso.csv', delimiter=",")
data.head()

matches = data.shape [0]

features = data.shape [1] - 1

home_win = len(data[data.Res==1])
away_win = len(data[data.Res==2])
draw = len(data[data.Res==0])

win_rate = (float(home_win)/(matches)) * 100

print(matches)
print(features)
print(home_win)
print(away_win)
print(draw)
print(win_rate)

x = np.arange(3)

val = [home_win, away_win, draw]
plt.bar(x, val)
plt.xticks(x, ('Home', 'Away', 'Draw'))
plt.show()

num_data = data.drop(['Country', 'League', 'Season', 'Date', 'Time', 'Home', 'Away'], 1)
num_data.head()

features = num_data.drop(['Res'], 1)

labels = num_data['Res']

print(features)
print(labels)

features_list = ('HG','AG','PH','PD','PA','MaxH','MaxD','MaxA','AvgH','AvgD','AvgA')

k_best_features = SelectKBest(k='all')
k_best_features.fit_transform(features, labels)
k_best_features_scores = k_best_features.scores_
raw_pairs = zip(features_list[1:], k_best_features_scores)
ordered_pairs = list(reversed(sorted(raw_pairs, key=lambda x: x[1])))

k_best_features_final = dict(ordered_pairs[:15])
best_features = k_best_features_final.keys()
print ('')
print ("Melhores features:")
print (k_best_features_final)

features = num_data.drop(['Res', 'game_id', 'home_id', 'Away_id', 'AG', 'PD', 'PH'], 1)

labels = num_data['Res']
print(features.head())

print(labels.head())

scaler = MinMaxScaler().fit(features)
features_scale = scaler.transform(features)

print(features_scale.shape)
print(features_scale)

X_train = features_scale[:1932]
X_test = features_scale[1932:2155]
y_train = labels[:1932]
y_test = labels[1932:2155]

print(len(X_train), len(y_train))

print(len(X_test), len(y_test))

clf_LR = LogisticRegression(multi_class='multinomial', max_iter=2000)

clf_LR.fit(X_train, y_train)
pred = clf_LR.predict(X_test)

lg_acc = accuracy_score(y_test, pred)

print(lg_acc)

clf = SVC()
clf.fit(X_train, y_train)
pred = clf.predict(X_test)

SVC_acc = accuracy_score(y_test, pred)

print(SVC_acc)

previsao = features_scale[2155:]

game_id_full = data['game_id']
game_id = game_id_full[2155:]

res_full = data['Res']
res = res_full[2155:]

pred = clf_LR.predict(previsao)

df = pd.DataFrame({'real': res, 'previsao':pred, 'game_id':game_id})
print(df.head(20))