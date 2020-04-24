import argparse
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.dummy import DummyClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

from brand import Brand, Burberry, Versace, DolceGabbana


class Model:
    
    def __init__(self, name, **clf_params):
        supported_names = ['Dummy', 'SVC', 'RandomForest', 'LogisticRegression', 'KNeighbors']
        if name not in supported_names:
            raise ValueError(f'model name {name} not in supported models: {supported_names}')
        self.name = name + str(clf_params)
        self.model_type = name
        
        classifiers = {
            'SVC': SVC,
            'Dummy': DummyClassifier,
            'RandomForest': RandomForestClassifier,
            'LogisticRegression': LogisticRegression,
            'KNeighbors': KNeighborsClassifier
        }
        
        self.clf = classifiers[self.model_type](**clf_params)
        
    def fit_and_score(self, X_train, X_test, y_train, y_test):
        self.clf.fit(X_train, y_train)
        return self.clf.score(X_test, y_test)
    

def encode_words(data):
    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(data['words'])
    
    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False, categories='auto')
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    return onehot_encoded


def encode_brands(data):
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(data['brand'])
    return integer_encoded


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Example of classifying links into url')
    parser.add_argument('--config', default='config.json', dest='config', type=str)
    parser.add_argument('--random_state', default=42, dest='random_state', type=int)
    parser.add_argument('--results_path', default='results.csv', dest='results_path', type=str)
    parser.add_argument('--verbose', default=False, dest='verbose', type=bool)

    args = parser.parse_args()
    
    with open(args.config, 'r') as config_file:
        config = json.load(config_file)
       
    
    burberry_conf = config['brands']['burberry']
    burberry = Burberry('burberry', burberry_conf['urls'], burberry_conf['relevance_threshold'])

    versace_conf = config['brands']['versace']
    versace = Versace('versace', versace_conf['urls'], versace_conf['relevance_threshold'])

    dg_conf = config['brands']['d&g']
    dolce_gabbana = DolceGabbana('d&g', dg_conf['urls'], dg_conf['relevance_threshold'])
    
    brands = [burberry, versace, dolce_gabbana]
    data = []
    for brand in brands:
        links = brand.scrap_links()
        if args.verbose:
            print(f'for brand {brand.name} we found {len(links)} unique links')
        brand_data = brand.links_to_dataframe(links)
        data.append(brand_data)
        brand.plot_most_used(brand_data, f'{brand.name}.png')
        
    data = pd.concat(data, axis=0, ignore_index=True)
    words_encoded = encode_words(data)
    brands_encoded = encode_brands(data)
    
    
    X_train, X_test, y_train, y_test = train_test_split(words_encoded, brands_encoded, test_size=0.33, random_state=args.random_state)
    
    accuracies = {'model': [], 'accuracy': []}
    for model_type, params_list in config['models'].items():
        for params in params_list:
            model = Model(model_type, **params)
            accuracy = model.fit_and_score(X_train, X_test, y_train, y_test)
            accuracies['model'].append(model.name)
            accuracies['accuracy'].append(accuracy)
            if args.verbose:
                print(f'for model {model.name} we got {accuracy:.3f} accuracy')
                      
    results = pd.DataFrame.from_dict(accuracies)
    results.to_csv(args.results_path)
