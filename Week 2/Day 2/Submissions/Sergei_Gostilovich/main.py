from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from  get_data_fun import get_burberry_df, get_versace_df, get_dg_df
from for_ml_fun import apply_brand_loop
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier






#GETTING DATA
df_burberry = get_burberry_df()
df_versace = get_versace_df()
df_dg = get_dg_df()

df_brands = pd.concat([df_versace.reset_index(), df_burberry.reset_index(), df_dg.reset_index()])
df_brands = df_brands.drop(columns=['index'])
df_brands['words'] = df_brands['words'].str.upper()

# integer encode
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(df_brands['words'])
print(integer_encoded)
# binary encode
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

brands_transformed = apply_brand_loop(df_brands.copy())
y = brands_transformed

X = onehot_encoded

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
models = []


models.append(("Baseline", DummyClassifier(random_state=391488407)))

models.append(("Support vector (C=1.00)", SVC(C=1.00, gamma="scale")))
models.append(("Support vector (C=0.25)", SVC(C=0.25, gamma="scale")))
models.append(("Support vector (C=4.00)", SVC(C=4.00, gamma="scale")))
models.append(("Random Forest", RandomForestClassifier(n_estimators=100, random_state=1283220422)))
models.append(("Logistic Regression (C=1.00)",
               LogisticRegression(C=1.00, solver="liblinear", penalty="l1")))
models.append(("Logistic Regression (C=0.25)",
               LogisticRegression(C=0.25, solver="liblinear", penalty="l1")))
models.append(("Logistic Regression (C=4.00)",
               LogisticRegression(C=4.00, solver="liblinear", penalty="l1")))
models.append(("1-nn euclidean",
               KNeighborsClassifier(n_neighbors=1)))
models.append(("1-nn cosine",
               KNeighborsClassifier(n_neighbors=1, metric="cosine")))
models.append(("5-nn cosine",
               KNeighborsClassifier(n_neighbors=5, metric="cosine")))


models = dict(models)
for name, clf in models.items():
    clf.fit(X_train, y_train)

scores = pd.Series({name: clf.score(X_test, y_test) for name, clf in models.items()}, name="Accuracy")
print(scores)