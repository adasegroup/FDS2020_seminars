from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

class DataDesc():
    def __init__(self, img_title, img_name, brand_name):
        self.img_title = img_title
        self.img_name = img_name
        self.brand_name = brand_name
        
burberry_desc = DataDesc("Most used words in Burberry 'New in' SS2020 Women collection",
                        "SS2020_Burberry_word_frequency.jpg",
                        'burberry')

versace_desc = DataDesc("Most used words in Versace 'New in' SS2020 Women collection",
                        "SS2020_Versace_word_frequency.jpg",
                        'versace')

dg_desc = DataDesc("Most used words in D&G 'New in' SS2020 Women collection",
                   "SS2020_D&G_word_frequency.jpg",
                   'd&g')

class Data():
    def __init__(self, desc):
        self.desc = desc
        
    def plot(self, df_rel):
        pass
    
    def get_docs(self):
        pass
    
    def get_counts(self, doc_uniq):
        pass
    
    def post_processing(self, df):
        pass
    
    def prepare_data(self):
        doc_uniq = self.get_docs()
        print("Number of unique items: %d" % len(doc_uniq))
        
        result = self.get_counts(doc_uniq)
        
        words = list(result.keys())
        counts = list(result.values())
        
        # TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
        df = pd.DataFrame.from_dict({
            "words": words,
            "counts": counts,
        })
        
        df_rel = self.post_processing(df)
        
        self.plot(df_rel)
        df_rel["brand"] = self.desc.brand_name
        return df_rel

class BurberryData(Data):
    def plot(self):
        pass
    
    def get_docs(self):
        burberry_urls = [
            "https://us.burberry.com/womens-new-arrivals-new-in/",
            "https://us.burberry.com/womens-new-arrivals-new-in/?start=2&pageSize=120&productsOffset=&cellsOffset=8&cellsLimit=&__lang=en"
        ]
        # SCRAPING & CREATING A LIST OF LINKS
        doc = []
        for url in burberry_urls:
            r = requests.get(url)
            html_doc = r.text
            soup = BeautifulSoup(html_doc)

            for link in soup.find_all("a"):
                l = link.get("href")
                if "-p80" in l: # <-- THIS WILL NEED TO CHANGE
                    doc.append(l)

        # DEDUPLICATING THE LIST OF LINKS
        doc_uniq = set(doc)
        return doc_uniq
    
    def get_counts(self, doc_uniq):
        result = {}
        for link in doc_uniq:
            words = link.replace("/", "").split("-")
            for word in words:
                if word in result:
                    result[word] += 1
                else:
                    result[word] = 1
        return result
    
    def post_processing(self, df):
        df_sorted = df.sort_values("counts", ascending = True)
        df_rel = df_sorted[df_sorted['counts']>3]
        return df_rel
    
    def plot(self, df_rel):
        plt.barh(df_rel['words'], df_rel['counts'], color = "#C19A6B")
        plt.title(self.desc.img_title)
        plt.xticks(np.arange(0, 18, step=2))
        plt.savefig(self.desc.img_name)


class VersaceData(Data):       
    def plot(self, df_rel):
        plt.barh(df_rel.index, df_rel['counts'], color = "#FFD700")
        plt.title(self.desc.img_title)
        plt.savefig(self.desc.img_name)
    
    def get_docs(self):
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
        return doc_uniq
    
    def get_counts(self, doc_uniq):
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
    
    def post_processing(self, df):
        df2 = df.set_index("words")
        df_sorted = df2.sort_values("counts", ascending = True)
        df_rel = df_sorted[df_sorted['counts']>2]
        return df_rel


class DgData(Data):
    def __init__(self, desc):
        self.desc = desc
        
    def plot(self, df_rel):
        plt.barh(df_rel.index, df_rel['counts'], color = "#E0115F")
        plt.title(self.desc.img_title)
        plt.savefig(self.desc.img_name, pad_inches=0.1)
    
    def get_docs(self):
        # CREATING LIST OF RELEVANT URLS
        root_url = "https://us.dolcegabbana.com/en/women/highlights/new-in/?page={page}"
        pages = [1,2,3,4]
        urls = [root_url.format(page=page) for page in pages]


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
        return doc_uniq
    
    def get_counts(self, doc_uniq):
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
    
    def post_processing(self, df):
        df2 = df.set_index("words")
        df_sorted = df2.sort_values("counts", ascending = True)
        df_rel = df_sorted[df_sorted['counts']>4]
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


def apply_brand_loop(df):
    brand_list = []
    for i in range(len(df)):
        brand = df.iloc[i]['brand']
        target = brand_target(brand)
        brand_list.append(target)
    return brand_list


def get_data():
    df_burberry = BurberryData(burberry_desc).prepare_data() 
    df_versace =  VersaceData(versace_desc).prepare_data() 
    df_dg = DgData(dg_desc).prepare_data()

    df_brands = pd.concat([df_versace.reset_index(), df_burberry.reset_index(), df_dg.reset_index()])
    df_brands = df_brands.drop(columns=['index'])
    df_brands['words'] = df_brands['words'].str.upper()

    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(df_brands['words'])

    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

    brands_transformed = apply_brand_loop(df_brands.copy())
    y = brands_transformed
    X = onehot_encoded

    return X, y