import argparse
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
            soup = BeautifulSoup(html_doc, features="lxml")

            for link in soup.find_all("a"):
                l = self.link_selector(link) 
                if l is not None:
                    links.append(l)

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
        relevant_links = sorted_links[sorted_links['counts'] > self.relevance_threshold].copy()
        relevant_links.loc[:, 'brand'] = self.name
        relevant_links.loc[:, 'words'] = relevant_links.loc[:, 'words'].str.upper()
        return relevant_links
    
    def plot_most_used(self, data, image_path):
        plt.barh(data['words'], data['counts'], color = "#C19A6B")
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
        a = link.get("href")
        if a is None:
            return None
        if a.startswith("/us/en-us/women/new-arrivals/new-in/") and not a.startswith("/us/en-us/women/new-arrivals/new-in/?"):
            return a
        else:
            return None
        
    def word_extractor(self, link):
        words = link.replace("/us/en-us/women/new-arrivals/new-in/", "") .split("/")
        words = words[0].split("-")
        return words
        
        
class DolceGabbana(Brand):
    
    def link_selector(self, link):
        a = link.get("aria-label")
        if a != None and a.startswith("Visit"):
            return a
        else:
            return None
            
    def word_extractor(self, link):
        return link.replace("Visit", "").replace(" product page","").split(" ")                                                 