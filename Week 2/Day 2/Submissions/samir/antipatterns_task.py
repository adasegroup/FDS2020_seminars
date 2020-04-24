#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

from src import get_brand_2, get_brand_1, get_brand_3, get_models_dict, brand_target

URLS = ["https://us.burberry.com/womens-new-arrivals-new-in/",
        "https://us.burberry.com/womens-new-arrivals-new-in/?start=2&pageSize=120&productsOffset=&cellsOffset=8&cellsLimit=&__lang=en"]
URL = "https://www.versace.com/us/en-us/women/new-arrivals/new-in/"
URL_i = "https://us.dolcegabbana.com/en/women/highlights/new-in/?page="

if __name__ == '__main__':
    df_versace = get_brand_1(URLS)
    df_burberry = get_brand_2(URL)
    df_dg = get_brand_3(URL_i)

    df_brands = pd.concat([df_versace.reset_index(), df_burberry.reset_index(), df_dg.reset_index()])

    # df_brands = df_brands.drop(columns=['index'])

    df_brands['words'] = df_brands['words'].str.upper()

    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(df_brands['words'])
    print(integer_encoded)

    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)

    X = onehot_encoder.fit_transform(integer_encoded)
    y = df_brands['brand'].apply(lambda x: brand_target(x))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    models = get_models_dict()

    for clf_key in models.keys():
        clf = models[clf_key]
        clf.fit(X_train, y_train)

    scores = pd.Series({clf_name: models[clf_name].score(X_test, y_test) for clf_name in models.keys()}, name="Accuracy")

    print(scores)
