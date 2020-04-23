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
        
        self.clf = classifiers(self.model_type)(**clf_params)
        
    def fit_and_score(self, X_train, X_test, y_train, y_test):
        self.clf.fit(X_train, y_train)
        return self.clf.score(X_test, y_test)
    

def encode_words(data):
    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(data['words'])
    
    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    return onehot_encoded


def encode_brands(data):
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(data['brands'])
    return integer_encoded



    


class Brand:
    def __init__(self, name, urls, relevance_threshold):
        
        supported_brands = ['burberry', 'versace', 'd&g']
        if name not in supported_brands:
            raise ValueError(f'unsupported brand {name}')
        
        self.name = name
        self.urls = urls
        self.relevance_threshold = relevance_threshold
    
    def scrap_links(self):
        links = []
        for url in self.urls:
            r = requests.get(url)
            html_doc = r.text
            soup = BeautifulSoup(html_doc)

            for link in soup.find_all("a"):
                l = self.link_selector(link) 
                if l is not None:
                    doc.append(l)

        # DEDUPLICATING THE LIST OF LINKS
        unique_links = set(links)
        return unique_links
    
    def links_to_dataframe(self, links):
        # CREATING A DICTIONARY WITH WORDS : COUNTS AND KEY : VALUE PAIRS
        result = {}
        for link in links:
            words = self.word_extractor(link)
            for word in words:
                if word in result:
                    result[word] += 1
                else:
                    result[word] = 1

        words = list(result.keys())
        counts = list(result.values())

        # TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
        links_frame = pd.DataFrame.from_dict({
            "words": words,
            "counts": counts,
        })

        sorted_links = links_frame.sort_values("counts", ascending = True)
        relevant_links = sorted_links[sorted_links['counts'] > relevance_threshold]
        relevant_links.loc[:, 'brand'] = self.name
        return relevant_links
    
    def plot_most_used(self, data, image_path):
        plt.barh(words, counts, color = "#C19A6B")
        plt.title(f'{self.name} most frequent words')
        plt.xticks(np.arange(0, 18, step=2))
        plt.savefig(image_path)
    

class Burberry(Brand):
    
    def link_selector(self, link):
        l = link.get("href")
        if "-p80" in l: 
            return l
        else:
            return None
            
    def word_extractor(self, link):
        return link.replace("/", "").split("-")


class Versace(Brand):
    
    def link_selector(self, link):
        a = t.get("href")
        if a.startswith("/us/en-us/women/new-arrivals/new-in/") and not link.startswith("/us/en-us/women/new-arrivals/new-in/?"):
            return a
        else:
            return None
        
    def word_extractor(self, link):
        words = link.replace("/us/en-us/women/new-arrivals/new-in/", "") .split("/")
        words = words[0].split("-")
        return words
        
        
class DolceGabbana(Brand):
    
    def link_selector(self, link):
        a = t.get("aria-label")
        if a != None and a.startswith("Visit"):
            return a
        else:
            return None
            
    def word_extractor(self, link):
        return link.replace("Visit", "").replace(" product page","").split(" ")                                                                                                                                      

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Example of classifying links into url')
    parser.add_argument('--config', default='config.json', dest='config', type=str)
    parser.add_argument('--random_state', default=42, dest='random_state', type=int)
    parser.add_argument('--results_path', default='results.csv', dest='results_path', type=str)
    parser.add_argument('--verbose', default=False, dest='verbose', type=bool)

    args = parser.parse_args()
    
    with open(args.config, 'r') as config_file:
        config = json.load(config_file)
       
    
    burberry = Burberry('burberry', config['brands']['burberry']['urls'], config['brands']['burberry']['relevance_threshold'])
    versace = Versace('versace', config['brands']['versace']['urls'], config['brands']['versace']['relevance_threshold'])
    dolce_gabbana = DolceGabbana('d&g', config['brands']['d&g']['urls'], config['brands']['d&g']['relevance_threshold'])
    
    brands = [burberry, versace, dolce_gabbana]
    data = []
    for brand in brands:
        links = brand.scrap_links()
        if verbose:
            print(f'for brand {brand} we found {len(links)} unique links')
        brand_data = brand.links_to_dataframe(links)
        data.append(brand_data)
        brand.plot(brand_data, f'{brand_name}.png')
        
    data = pd.concat(data, axis=0, ignore_index=True)
    words_encoded = encode_words(data)
    brands_encoded = encode_brands(data)
    
    
    X_train, X_test, y_train, y_test = train_test_split(words_encoded, brands_encoded, test_size=0.33, random_state=args.random_state)
    
    accuracies = {}
    for model_type, params_list in config['models'].items():
        for params in params_list:
            model = Model(model_type, **params)
            accuracy = model.fit_and_score(X_train, X_test, y_train, y_test)
            accuracies[model.name] = accuracy
            if verbose:
                print(f'for model {model.name} we got {accuracy:.3f} accuracy')
                      
    results = pd.DataFrame.from_dict(accuracies)
    results.to_csv(args.results_path)
