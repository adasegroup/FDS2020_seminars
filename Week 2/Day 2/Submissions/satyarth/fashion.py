from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.dummy import DummyClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

def scrape_burberry():
    urls = [
        "https://us.burberry.com/womens-new-arrivals-new-in/",
        "https://us.burberry.com/womens-new-arrivals-new-in/?start=2&pageSize=120&productsOffset=&cellsOffset=8&cellsLimit=&__lang=en"
    ]

    doc = []
    for url in urls:
        r = requests.get(url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc)

        for link in soup.find_all("a"):
            l = link.get("href")
    #         if "-p80" in l: # <-- THIS WILL NEED TO CHANGE
            if not l.endswith('/'):
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
                
    return result

def scrape_versace():
    # CREATING LIST OF RELEVANT URLS
    url = "https://www.versace.com/us/en-us/women/new-arrivals/new-in/"

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
#     print("Number of unique items:"+str(len(doc_uniq)))
    #print(doc_uniq)

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
    
    return result

def scrape_dg():
    # CREATING LIST OF RELEVANT URLS
    urls = ["https://us.dolcegabbana.com/en/women/highlights/new-in/?page={}".format(i) for i in [1, 2, 3, 4]]
    #urls = list(urls)

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
    #print(doc)

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
    return result

def plot_frequencies(df_rel, brand):
    # PLOTTING
    fig = plt.figure(figsize=(9, 6))
    plt.barh(df_rel.index, df_rel['counts'], color = "#E0115F")
    plt.title("Most used words in {} 'New in' SS2020 Women collection".format(brand))
    plt.savefig("SS2020_{}_word_frequency.jpg".format(brand), pad_inches=0.1)
    
def dataframeize(result_dict, brand, count_threshold=3):
    
    words = list(result_dict.keys())
    counts = list(result_dict.values())
    
    df = pd.DataFrame.from_dict({
        "words": words,
        "counts": counts,
    })

    df2 = df.set_index("words")
    #df2.drop(["", "WITH"])
    df_sorted = df2.sort_values("counts", ascending = True)
    df_rel = df_sorted[df_sorted['counts']>count_threshold]
    df_rel['brand']=brand
    return df_rel

parser = argparse.ArgumentParser(description='Process one integer')
parser.add_argument('-t', '--thresh', type=int, default=3,
                    help='Lower threshold for word frequencies')
args = parser.parse_args()
print('Word frequency threshold: {}'.format(args.thresh))

brands = ['burberry', 'd&g', 'versace']
result_dicts = {}
dataframes = {}

for brand, scraper in zip(brands, [scrape_burberry, scrape_dg, scrape_versace]):
    print("Scraping {}".format(brand))
    result_dicts[brand] = scraper()
    
for brand in brands:
    dataframes[brand] = dataframeize(result_dicts[brand], brand, count_threshold=args.thresh)
    plot_frequencies(dataframes[brand], brand)
    
df_brands = pd.concat([dataframes[brand].reset_index() for brand in brands])
df_brands['words'] = df_brands['words'].str.upper()

label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(df_brands['words'])
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
X = onehot_encoder.fit_transform(integer_encoded)

y = df_brands['brand'].map({'versace': 0,
                            'burberry': 1,
                            'd&g': 2}).values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

models = []

models.append(("Baseline", DummyClassifier(random_state=391488407)))
models.append(("Support vector (C=1.00)", SVC(C=1.00, gamma="scale")))
models.append(("Support vector (C=0.25)", SVC(C=0.25, gamma="scale")))
models.append(("Support vector (C=4.00)", SVC(C=4.00, gamma="scale")))
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
    print("Model: {}\tAccuracy: {}".format(name, clf.score(X_test, y_test)))