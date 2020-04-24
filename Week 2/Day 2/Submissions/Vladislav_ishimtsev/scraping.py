import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests

from bs4 import BeautifulSoup
from itertools import Counter


class Scraping:
    def __init__(self, verbose=True):
        self.documents = []
        self.counter = None
        self.verbose = verbose

        self.most_common = None

    def process(self, urls, condition, get_words, filename, brand):
        # SCRAPING & CREATING A LIST OF LINKS
        for url in urls:
            self.scrap_url(url, condition)

        if self.verbose:
            print("Number of unique items: %d" % len(self.documents))

        # CREATING A DICTIONARY WITH WORDS : COUNTS AND KEY : VALUE PAIRS
        self.count(get_words)

        if self.verbose:
            print(self.most_common.head())
            print(self.most_common.shape)

        # PLOTTING
        self.save_plot(filename)
        self.most_common['brand'] = brand
        return self.most_common

    def scrap_url(self, url, condition):
        r = requests.get(url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc)

        for link in soup.find_all("a"):
            l = link.get("href")
            if condition(l):  # <-- THIS WILL NEED TO CHANGE
                self.documents.append(l)

        # DEDUPLICATING THE LIST OF LINKS
        self.documents = set(self.documents)

    def count(self, get_words):
        if len(self.documents) == 0:
            raise Exception('Call scraping first')

        all_documents = get_words(self.documents).split('-')
        self.counter = Counter(all_documents)

        # TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
        df = pd.DataFrame.from_dict(self.counter).reset_index()
        df.columns = ['words', 'counts']

        df_sorted = df.sort_values("counts", ascending=True)
        self.most_common = df_sorted[df_sorted['counts'] > 3]

    def save_plot(self, filename):
        plt.barh(self.most_common['words'], self.most_common['counts'], color="#C19A6B")
        plt.title("Most used words in Burberry 'New in' SS2020 Women collection")
        plt.xticks(np.arange(0, 18, step=2))
        plt.savefig(filename)