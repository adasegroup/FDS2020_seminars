from abc import ABC, abstractmethod
from collections import Counter

import requests
import pandas as pd
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import numpy as np


class Scrapper(ABC):
    @abstractmethod
    def get_urls(self):
        pass

    @abstractmethod
    def links_from_soup(self, soup):
        pass

    @abstractmethod
    def words_from_link(self, link):
        pass


def parse_urls(filename):
    with open(filename, 'r') as f:
        return [url.strip() for url in f.readlines()]


def request_url(url):
    r = requests.get(url)
    html_doc = r.text
    return BeautifulSoup(html_doc)


def scrap_words(scrapper: Scrapper):
    links = {
        link
        for url in scrapper.get_urls()
        for link in scrapper.links_from_soup(request_url(url))
    }
    print(f'Number of unique elements: {len(links)}')

    for link in links:
        yield from scrapper.words_from_link(link)


def analize_words(df, top_count, title, color):
    df_sorted = df.sort_values("counts", ascending = True)
    df_rel = df_sorted[df_sorted['counts'] > top_count]
    print(df_rel.head())
    print(df_rel.shape)

    plt.figure()
    plt.barh(df_rel['words'], df_rel['counts'], color = color)
    plt.title(f"Most used words in {title} 'New in' SS2020 Women collection")
    plt.savefig(f'SS2020_{title}_word_frequency.png')

    df_rel['brand'] = title

    return df_rel


def counts_to_df(counts):
    return pd.DataFrame.from_dict({
        'words': list(counts.keys()),
        'counts': list(counts.values()),
    })


def pipeline(scrapper, title, top_count, color):
    words = scrap_words(scrapper)
    counts = Counter(words)
    print(counts)
    df = counts_to_df(counts)
    return analize_words(df, top_count, title, color)
