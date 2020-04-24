from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

@dataclass    
class Company():
    urls: list(str)
    filename: str
    doc_uniq: set
    words: list
    counts: list
    df_rel
    
    def get_doc_uniq(self):
        return
    
    def get_words_counts(self):
        return
    
    def get_df_rel(self):
        df = pd.DataFrame.from_dict({
        "words": words,
        "counts": counts,
        })
        df_sorted = df.sort_values("counts", ascending = True)
        self.df_rel = df_sorted[df_sorted['counts']>3]
        print(self.df_rel.head())
        print(self.df_rel.shape)
        
    def prepare_data(self)
        self.get_doc_uniq()
        self.get_words_counts()
        self.get_df_rel()
        
    def plot(self):
        # PLOTTING
        df_rel = self.df_rel
        plt.barh(df_rel['words'], df_rel['counts'], color = "#C19A6B")
        plt.xticks(np.arange(0, 18, step=2))
        plt.title("Most used words in " + df_rel['brand'][0])
        plt.savefig(self.filename + ".jpg")


class Burberry(Company):
    filename = 'SS2020_Burberry_word_frequency'
    urls = [
    "https://us.burberry.com/womens-new-arrivals-new-in/",
    "https://us.burberry.com/womens-new-arrivals-new-in/?start=2&pageSize=120&productsOffset=&cellsOffset=8&cellsLimit=&__lang=en"
]
    def get_doc_uniq():
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
        print("Number of unique items:"+str(len(doc_uniq)))
        self.doc_uniq = set(doc)
        return
    def get_words_counts(self):
        # burb
        words_dict = {}
        for link in self.doc_uniq:
            words = link.replace("/", "").split("-")
            for word in words:
                if word in words_dict:
                    words_dict[word] += 1
                else:
                    words_dict[word] = 1

        self.words = list(words_dict.keys())
        self.counts = list(words_dict.values())
        

        
class Versace(Company):
    filename = "SS2020_Versace_word_frequency"
    urls = ["https://www.versace.com/us/en-us/women/new-arrivals/new-in/"
]
    def get_doc_uniq():
        doc = []
        for url in self.urls:
            r = requests.get(url)
            html_doc = r.text
            soup = BeautifulSoup(html_doc)
            soup_f = soup.find_all("a")
            for t in soup_f:
                a = t.get("href")
                if a.startswith("/us/en-us/women/new-arrivals/new-in/"):
                    doc.append(a)

            # DEDUPLICATING THE LIST OF LINKS
            self.doc_uniq = set(doc)
            return
    def get_words_counts(self):
        words_dict = {}
        garbage = []
        for link in doc_uniq:
            if link.startswith("/us/en-us/women/new-arrivals/new-in/?"):
                continue
            words = link.replace("/us/en-us/women/new-arrivals/new-in/", "") .split("/")
            words = words[0].split("-")

            for word in words:
                if word in words_dict:
                    words_dict[word] += 1
                else:
                    words_dict[word] = 1

        self.words = list(words_dict.keys())
        self.counts = list(words_dict.values())

class Dolce(Company):
    filename = "SS2020_D&G_word_frequency"
    urls = ['https://us.dolcegabbana.com/en/women/highlights/new-in/?page=1',
            'https://us.dolcegabbana.com/en/women/highlights/new-in/?page=2',
            'https://us.dolcegabbana.com/en/women/highlights/new-in/?page=3',
            'https://us.dolcegabbana.com/en/women/highlights/new-in/?page=4']
    def get_doc_uniq():
        doc = []
        for url in self.urls:
            r = requests.get(url)
            html_doc = r.text
            soup = BeautifulSoup(html_doc)
            soup_f = soup.find_all("a")

            for t in soup_f:
                a = t.get("aria-label")
                if a != None and a.startswith("Visit"):
                    doc.append(a)

        # DEDUPLICATING THE LIST OF LINKS
        self.doc_uniq = set(doc)
        return
    
    def get_words_counts(self):
        words_dict = {}
        for link in doc_uniq:
            words = link.replace("Visit", "").replace(" product page","").split(" ")                                                                                                                                      
            for word in words:
                if word in words_dict:
                    words_dict[word] += 1
                else:
                    words_dict[word] = 1
        del(words_dict[""])
        self.words = list(words_dict.keys())
        self.counts = list(words_dict.values())


# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--what1')
#     parser.add_argument('--what2')
#     args = parser.parse_args()
#     return args

        
def main()
    bur = Burberry()
    ver = Versace()
    dol = Dolce()
    datas = [bur, dol, ver]
    
    for data in datas:
        data.prepare_data()

    
        
        
    df_versace = ver.df_rel
    #... code for training should be here
