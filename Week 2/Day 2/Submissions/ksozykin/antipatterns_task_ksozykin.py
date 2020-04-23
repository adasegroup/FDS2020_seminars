#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from abc import ABC, abstractmethod
import warnings
warnings.filterwarnings("ignore")


import argparse

parser = argparse.ArgumentParser(description='Run Experiment')
parser.add_argument("--seed", "-s", help='args.random_state',default=1,type=int)
parser.add_argument("--test_size", help='args.test_size',default=0.33,type=float)
parser.add_argument("--clf", help='args.clf_type',default='SVC',type=str)


args=parser.parse_args()

class SomeBrand(ABC):
    def __init__(self):
        self.name = None
        self.base_url = None
        self.plotting = False
      
    @abstractmethod
    def parse(self):
        pass

class BurberryBrand(SomeBrand):
    def __init__(self,plotting=False):
        self.name = 'Burberry'
        self.base_url = "https://us.burberry.com/womens-new-arrivals-new-in/"
        self.plotting = plotting
        
    def parse(self):
        
        urls = [
            self.base_url,
            "{}?start=2&pageSize=120&productsOffset=&cellsOffset=8&cellsLimit=&__lang=en".format(self.base_url)
        ]

        # SCRAPING & CREATING A LIST OF LINKS
        doc = []
        for url in urls:
            r = requests.get(url)
            html_doc = r.text
            soup = BeautifulSoup(html_doc)

            for link in soup.find_all("a"):
                l = link.get("href")
                if "-p80" in l: # <-- THIS WILL NEED TO CHANGE
                    doc.append(l)

        # DEDUPLICATING THE LIST OF LINKS
        doc_uniq = set(doc)
        
        # CREATING A DICTIONARY WITH WORDS : COUNTS AND KEY : VALUE PAIRS
        result = {}
        for link in doc_uniq:
            words = link.replace("/", "").split("-")
            for word in words:
                if word in result:
                    result[word] += 1
                else:
                    result[word] = 1

        words = list(result.keys())
        counts = list(result.values())

        # TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
        df = pd.DataFrame.from_dict({
            "words": words,
            "counts": counts,
        })

        df_sorted = df.sort_values("counts", ascending = True)
        df_rel = df_sorted[df_sorted['counts']>3]
    
        if self.plotting:
        # PLOTTING
            plt.barh(df_rel['words'], df_rel['counts'], color = "#C19A6B")
            plt.title("Most used words in Burberry 'New in' SS2020 Women collection")
            plt.xticks(np.arange(0, 18, step=2))
            plt.savefig("SS2020_Burberry_word_frequency.jpg")
        df_rel['brand']='burberry'
        return df_rel

class VersaceBrand(SomeBrand):
    def __init__(self,plotting=False):
        self.name = 'Versace'
        self.base_url = "https://www.versace.com/us/en-us/women/new-arrivals/new-in/"
        self.plotting = plotting
        
    def parse(self):
        
        url = self.base_url
    
        # SCRAPING & CREATING A LIST OF LINKS
        doc = []
        #for url in urls:
        r = requests.get(url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc)
        soup_f = soup.find_all("a")
        for t in soup_f:
            a = t.get("href")
            if a.startswith("/us/en-us/women/new-arrivals/new-in/"):
                doc.append(a)


        # DEDUPLICATING THE LIST OF LINKS
        doc_uniq = set(doc)
      

        result = {}
        garbage = []
        for link in doc_uniq:
            if link.startswith("/us/en-us/women/new-arrivals/new-in/?"):
                continue
            words = link.replace("/us/en-us/women/new-arrivals/new-in/", "") .split("/")
            words = words[0].split("-")

            for word in words:
                if word in result:
                    result[word] += 1
                else:
                    result[word] = 1

        words = list(result.keys())
        counts = list(result.values())

        # TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
        df = pd.DataFrame.from_dict({
            "words": words,
            "counts": counts,
        })

        df2 = df.set_index("words")
        df_sorted = df2.sort_values("counts", ascending = True)
        df_rel = df_sorted[df_sorted['counts']>2]


        if self.plotting:
            plt.barh(df_rel.index, df_rel['counts'], color = "#FFD700")
            plt.title("Most used words in Versace 'New in' SS2020 Women collection")
            plt.savefig("SS2020_Versace_word_frequency.jpg")
        df_rel['brand']='versace'
        return df_rel

class DgBrand(SomeBrand):
    def __init__(self,plotting=False):
        self.name = 'Dg'
        self.base_url = "https://us.dolcegabbana.com/en/women/highlights/new-in/?page="
        self.plotting = plotting
    
    def parse(self):
        # CREATING LIST OF RELEVANT URLS
        urls = []
        for i in [1,2,3,4]:
            u = "{}{}".format(self.base_url,str(i))
            urls.append(u)


        # SCRAPING & CREATING A LIST OF LINKS
        doc = []
        for url in urls:
            r = requests.get(url)
            html_doc = r.text
            soup = BeautifulSoup(html_doc)
            soup_f = soup.find_all("a")

            for t in soup_f:
                a = t.get("aria-label")
                if a != None and a.startswith("Visit"):
                    doc.append(a)


        # DEDUPLICATING THE LIST OF LINKS
        doc_uniq = set(doc)
       
        result = {}
        for link in doc_uniq:
            words = link.replace("Visit", "").replace(" product page","").split(" ")                                                                                                                                      
            for word in words:
                if word in result:
                    result[word] += 1
                else:
                    result[word] = 1
        del(result[""])
        words = list(result.keys())
        counts = list(result.values())

        # TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
        df = pd.DataFrame.from_dict({
            "words": words,
            "counts": counts,
        })

        df2 = df.set_index("words")
        df_sorted = df2.sort_values("counts", ascending = True)
        df_rel = df_sorted[df_sorted['counts']>4]


        if self.plotting:
            # PLOTTING
            plt.barh(df_rel.index, df_rel['counts'], color = "#E0115F")
            plt.title("Most used words in D&G 'New in' SS2020 Women collection")
            plt.savefig("SS2020_D&G_word_frequency.jpg", pad_inches=0.1)
        df_rel['brand']='d&g'
        return df_rel

def brand_target(brand):
    if 'versace' in brand:
        val = 0
    elif 'burberry' in brand:
        val = 1
    elif 'd&g' in brand:
        val = 2
    else:
        raise ValueError(f'Invalid brand: {brand}')
    return val

class BrandFactory:
    
    def __init__(self,name):
        self.name = name 
        
    def getbrand(self):
        if self.name == 'Burberry':
            return BurberryBrand()
        elif self.name == 'Versace':
            return VersaceBrand()
        elif self.name == 'Dg':
            return DgBrand()
        else:
            raise ValueError(name)


# In[3]:


brand_names = ['Burberry','Versace','Dg']

df_brands = pd.concat([BrandFactory(name).getbrand().parse().reset_index() for name in brand_names])

df_brands = df_brands.drop(columns=['index'])

# integer encode
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(df_brands['words'])

# binary encode
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

y = df_brands['brand'].apply(lambda brand: brand_target(brand)).values
X = onehot_encoded

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=args.seed)

models = []

if args.clf == 'DUMMY':
    
    models.append(("Baseline", DummyClassifier(random_state=args.seed)))

if args.clf == 'SVC':
    models.append(("Support vector (C=1.00)", SVC(C=1.00, gamma="scale")))
    models.append(("Support vector (C=0.25)", SVC(C=0.25, gamma="scale")))
    models.append(("Support vector (C=4.00)", SVC(C=4.00, gamma="scale")))


if args.clf == 'LOGREG':

    models.append(("Logistic Regression (C=1.00)",
                   LogisticRegression(C=1.00, solver="liblinear", penalty="l1")))

    models.append(("Logistic Regression (C=0.25)",
                   LogisticRegression(C=0.25, solver="liblinear", penalty="l1")))

    models.append(("Logistic Regression (C=4.00)",
                   LogisticRegression(C=4.00, solver="liblinear", penalty="l1")))

if args.clf == 'KNN':
   
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
scores = pd.DataFrame(scores)
scores.index.name = 'model'

print(scores)
