from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


class AbstractScraper(ABC):

    def __init__(self, name='', urls=(), min_count=1):
        self.min_count = min_count
        self.urls = urls
        self.name = name

        self.docs = None
        self.counts = None

    def collect_docs(self):
        docs = []
        for url in self.urls:
            r = requests.get(url)
            html_doc = r.text
            soup = BeautifulSoup(html_doc)

            docs += self.docs_from_soup(soup)
        self.docs = set(docs)

        print("Number of unique items:" + str(len(self.docs)))

    @abstractmethod
    def docs_from_soup(self, soup):
        pass

    @abstractmethod
    def words_from_doc(self, doc):
        pass

    def compute_counts(self):
        self.collect_docs()

        result = {}
        for doc in self.docs:
            words = self.words_from_doc(doc)
            for word in words:
                if word in result:
                    result[word] += 1
                else:
                    result[word] = 1

        words = list(result.keys())
        counts = list(result.values())

        df = pd.DataFrame.from_dict({
            "words": words,
            "counts": counts,
        }) \
            .set_index("words") \
            .sort_values("counts", ascending=True) \
            .query('counts > {}'.format(self.min_count))

        df['brand'] = self.name.lower()

        self.counts = df

    def get_counts(self):
        self.collect_docs()
        self.compute_counts()

        return self.counts


class BurberryScraper(AbstractScraper):

    def __init__(self, min_count=2):
        super().__init__(name='Burberry',
                         urls=("https://us.burberry.com/womens-new-arrivals-new-in/",
                               "https://us.burberry.com/womens-new-arrivals-new-in/?start=2&pageSize=120"
                               "&productsOffset=&cellsOffset=8&cellsLimit=&__lang=en"),
                         min_count=min_count)

    def docs_from_soup(self, soup):
        docs = []
        for link in soup.find_all("a"):
            l = link.get("href")
            if "-p80" in l:  # <-- THIS WILL NEED TO CHANGE
                docs.append(l)
        return docs

    def words_from_doc(self, doc):
        return doc.replace("/", "").split("-")


class VersaceScraper(AbstractScraper):

    def __init__(self, min_count=3):
        super().__init__(name='Versace',
                         urls=("https://www.versace.com/us/en-us/women/new-arrivals/new-in/",),
                         min_count=min_count)

    def docs_from_soup(self, soup):
        docs = []
        soup_f = soup.find_all("a")
        for t in soup_f:
            a = t.get("href")
            if a.startswith("/us/en-us/women/new-arrivals/new-in/"):
                docs.append(a)
        return docs

    def words_from_doc(self, doc):
        if doc.startswith("/us/en-us/women/new-arrivals/new-in/?"):
            return []
        else:
            words = doc.replace("/us/en-us/women/new-arrivals/new-in/", "").split("/")
            words = words[0].split("-")
            return words


class DGScraper(AbstractScraper):

    def __init__(self, min_count=4):
        urls = tuple("https://us.dolcegabbana.com/en/women/highlights/new-in/?page={}".format(i) for i in range(1, 5))

        super().__init__(name='D&G',
                         urls=urls,
                         min_count=min_count)

    def docs_from_soup(self, soup):
        docs = []
        soup_f = soup.find_all("a")

        for t in soup_f:
            a = t.get("aria-label")
            if (a is not None) and a.startswith("Visit"):
                docs.append(a)
        return docs

    def words_from_doc(self, doc):
        return doc.replace("Visit", "").replace(" product page", "").split(" ")


name2scraper = {"burberry": BurberryScraper,
                "d&g": DGScraper,
                "versace": VersaceScraper}


def create_scraper(name, min_count):
    return name2scraper[name](min_count=min_count)
