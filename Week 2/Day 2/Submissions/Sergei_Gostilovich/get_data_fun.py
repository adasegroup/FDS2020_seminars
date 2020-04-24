from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_burberry_df():
    urls = [
        "https://us.burberry.com/womens-new-arrivals-new-in/",
        "https://us.burberry.com/womens-new-arrivals-new-in/?start=2&pageSize=120&productsOffset=&cellsOffset=8&cellsLimit=&__lang=en"
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
    print("Number of unique items:"+str(len(doc_uniq)))

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
    print(df_rel.head())
    print(df_rel.shape)

    # PLOTTING
    plt.barh(df_rel['words'], df_rel['counts'], color = "#C19A6B")
    plt.title("Most used words in Burberry 'New in' SS2020 Women collection")
    plt.xticks(np.arange(0, 18, step=2))
    plt.savefig("SS2020_Burberry_word_frequency.png")
    df_rel['brand']='burberry'

    return df_rel

def get_versace_df():
    # VERSACE

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
    print("Number of unique items:"+str(len(doc_uniq)))
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

    words = list(result.keys())
    counts = list(result.values())
    #print(result)

    # TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
    df = pd.DataFrame.from_dict({
        "words": words,
        "counts": counts,
    })

    df2 = df.set_index("words")
    #df2 = df.drop(["a1008"],axis=0)
    df_sorted = df2.sort_values("counts", ascending = True)
    df_rel = df_sorted[df_sorted['counts']>2]
    #print(df_rel.head())
    #print(df_rel.shape)

    #PLOTTING
    plt.barh(df_rel.index, df_rel['counts'], color = "#FFD700")
    plt.title("Most used words in Versace 'New in' SS2020 Women collection")
    plt.savefig("SS2020_Versace_word_frequency.png")
    df_rel['brand']='versace'

    return df_rel

def get_dg_df():
    # CREATING LIST OF RELEVANT URLS
    urls = []
    #urls = list(urls)
    for i in [1,2,3,4]:
        u = str("https://us.dolcegabbana.com/en/women/highlights/new-in/?page=") + str(i)
        urls.append(u)

    #print(urls)

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
    print("Number of unique items:"+str(len(doc_uniq)))

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
    #df2.drop(["", "WITH"])
    df_sorted = df2.sort_values("counts", ascending = True)
    df_rel = df_sorted[df_sorted['counts']>4]
    #print(df_rel.head())
    #print(df_rel.shape)


    # PLOTTING
    plt.barh(df_rel.index, df_rel['counts'], color = "#E0115F")
    plt.title("Most used words in D&G 'New in' SS2020 Women collection")
    plt.savefig("SS2020_D&G_word_frequency.png", pad_inches=0.1)
    df_rel['brand']='d&g'

    return df_rel