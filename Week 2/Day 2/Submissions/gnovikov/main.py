#!/bin/bash


from abc import ABC, abstractmethod
from collections import Counter

import requests
import pandas as pd
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import numpy as np

from scrapping import pipeline, Scrapper
from ml_pipeline import process


class BurberryScrapper(Scrapper):
    URLS = [
        'https://us.burberry.com/womens-new-arrivals-new-in/',
        "https://us.burberry.com/womens-new-arrivals-new-in/?start=2&pageSize=120&productsOffset=&cellsOffset=8&cellsLimit=&__lang=en",
    ]

    def get_urls(self):
        yield from self.URLS

    def links_from_soup(self, soup):
        for link in soup.find_all("a"):
            l = link.get("href")
            if "-p80" in l:
                yield l

    def words_from_link(self, link):
        yield from link.replace("/", "").split("-")


class VersaceScrapper(Scrapper):
    URL = "https://www.versace.com/us/en-us/women/new-arrivals/new-in/"

    def get_urls(self):
        yield self.URL

    def links_from_soup(self, soup):
        for t in soup.find_all("a"):
            a = t.get("href")
            if a.startswith("/us/en-us/women/new-arrivals/new-in/"):
                yield a

    def words_from_link(self, link):
        if link.startswith("/us/en-us/women/new-arrivals/new-in/?"):
            return

        yield from link.replace("/us/en-us/women/new-arrivals/new-in/", "") .split("/")[0].split('-')


class DnGScrapper(Scrapper):
    BASE = "https://us.dolcegabbana.com/en/women/highlights/new-in/?page="

    def get_urls(self):
        for i in range(1, 5):
            yield f'{self.BASE}{i}'

    def links_from_soup(self, soup):
        for t in soup.find_all("a"):
            a = t.get("aria-label")
            if a is not None and a.startswith("Visit"):
                yield a

    def words_from_link(self, link):
        words = link.replace("Visit", "").replace(" product page","").split(" ")
        yield from filter(bool, words)
        # for word in words:
        #     if word != '':
        #         yield word


if __name__ == '__main__':
    burberry_df = pipeline(BurberryScrapper(), 'Burberry', 3, '#C19A6B')
    versace_df = pipeline(VersaceScrapper(), 'Versace', 2, '#FFD700')
    df_dg = pipeline(DnGScrapper(), 'DnG', 4, '#E0115F')

    process([burberry_df, versace_df, df_dg])
