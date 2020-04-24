import pandas as pd
import matplotlib.pyplot as plt

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


from Submissions.samir.src import CounterWithRefactor, TextScraper


def result2dataframe(result):
    words = list(result.keys())
    counts = list(result.values())

    # TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
    df = pd.DataFrame.from_dict({
        "words": words,
        "counts": counts,
    })

    df2 = df.set_index("words")
    df_sorted = df2.sort_values("counts", ascending=True)
    return df_sorted


def plot_horizontal_bar(x, count, title, save=None,  color="#C19A6B"):
    # PLOTTING
    plt.barh(x, count, color=color)
    plt.title(title)
    if save:
        plt.savefig(save)
    plt.close()


def brand_target(brand):
    if not brand in ['versace', 'burberry', 'd&g']:
        raise ValueError(f'Invalid brand: {brand}')
    if 'versace' in brand:
        return 0
    if 'burberry' in brand:
        return 1
    if 'd&g' in brand:
        return 2

def get_models_dict():
    models = {}

    models.update({"Baseline": DummyClassifier(random_state=391488407)})
    # models.update({"Support vector (C=1.30)": SVC(C=1.30, gamma="scale")})
    # models.update({"Support vector (C=0.45)": SVC(C=0.45, gamma="scale")})
    # models.update({"Support vector (C=4.80)": SVC(C=4.80, gamma="scale")})
    models.update({"Support vector (C=1.00)": SVC(C=1.00, gamma="scale")})
    models.update({"Support vector (C=0.25)": SVC(C=0.25, gamma="scale")})
    models.update({"Support vector (C=4.00)": SVC(C=4.00, gamma="scale")})
    models.update({"Random Forest": RandomForestClassifier(n_estimators=100, random_state=1283220422)})
    models.update({"Logistic Regression (C=1.00)": LogisticRegression(C=1.00, solver="liblinear", penalty="l1")})
    models.update({"Logistic Regression (C=0.25)": LogisticRegression(C=0.25, solver="liblinear", penalty="l1")})
    models.update({"Logistic Regression (C=4.00)": LogisticRegression(C=4.00, solver="liblinear", penalty="l1")})
    models.update({"1-nn euclidean": KNeighborsClassifier(n_neighbors=1)})
    models.update({"1-nn cosine": KNeighborsClassifier(n_neighbors=1, metric="cosine")})
    models.update({"5-nn cosine": KNeighborsClassifier(n_neighbors=5, metric="cosine")})

    return models

def get_brand_1(URLS):
    # SCRAPING & CREATING A LIST OF LINKS
    doc = []
    for url in URLS:
        text_scraper = TextScraper(url)
        doc_i = text_scraper.get_words('a', 'href', '-p80')
        doc += doc_i

    # DUPLICATING THE LIST OF LINKS
    doc_uniq = set(doc)
    print("Number of unique items:" + str(len(doc_uniq)))

    # CREATING A DICTIONARY WITH WORDS : COUNTS AND KEY : VALUE PAIRS

    counter = CounterWithRefactor(doc_uniq)
    result = counter.get_count(replace_strings=["/"],
                               split_char="-",
                               must_start_with=False,
                               split_char_2=False)

    df_sorted = result2dataframe(result)
    df_rel = df_sorted[df_sorted['counts'] > 3]
    print(df_rel.head())
    print(df_rel.shape)

    # PLOTTING
    plot_horizontal_bar(df_rel.index, df_rel['counts'],
                        title="Most used words in Burberry 'New in' SS2020 Women collection",
                        save="SS2020_Burberry_word_frequency.jpg")

    df_rel['brand'] = 'burberry'

    return df_rel


# VERSACE

# CREATING LIST OF RELEVANT URLS

# SCRAPING & CREATING A LIST OF LINKS

def get_brand_2(URL):
    text_scraper = TextScraper(URL)
    doc = text_scraper.get_words('a', 'href', '/us/en-us/women/new-arrivals/new-in/')

    # for url in URLS:

    # DEDUPLICATING THE LIST OF LINKS
    doc_uniq = set(doc)
    print("Number of unique items:" + str(len(doc_uniq)))
    # print(doc_uniq)

    counter = CounterWithRefactor(doc_uniq)
    result = counter.get_count(replace_strings=["/us/en-us/women/new-arrivals/new-in/"],
                               split_char="/",
                               must_start_with="/us/en-us/women/new-arrivals/new-in/?",
                               split_char_2="-")

    df_sorted = result2dataframe(result)
    df_rel = df_sorted[df_sorted['counts'] > 2]
    # print(df_rel.head())
    # print(df_rel.shape)

    # PLOTTING
    plot_horizontal_bar(df_rel.index, df_rel['counts'], color="#FFD700",
                        title="Most used words in Versace 'New in' SS2020 Women collection",
                        save="SS2020_Versace_word_frequency.jpg")

    df_rel['brand'] = 'versace'

    return df_rel


def get_brand_3(URL_i):
    # CREATING LIST OF RELEVANT URLS

    url_i = []
    # URLS = list(URLS)
    for i in [1, 2, 3, 4]:
        u = str(URL_i) + str(i)
        url_i.append(u)

    # print(URLS)

    # SCRAPING & CREATING A LIST OF LINKS
    doc = []
    for url in url_i:
        text_scraper = TextScraper(url)
        doc_i = text_scraper.get_words('a', 'aria-label', 'Visit')
        doc += doc_i

    # print(doc)

    # DEDUPLICATING THE LIST OF LINKS
    doc_uniq = set(doc)
    print("Number of unique items:" + str(len(doc_uniq)))

    counter = CounterWithRefactor(doc_uniq)
    result = counter.get_count(replace_strings=["Visit", " product page"],
                               split_char=" ",
                               must_start_with=False,
                               split_char_2=False)

    df_sorted = result2dataframe(result)
    df_rel = df_sorted[df_sorted['counts'] > 4]
    # print(df_rel.head())
    # print(df_rel.shape)

    # PLOTTING
    plot_horizontal_bar(df_rel.index, df_rel['counts'], color="#E0115F",
                        title="Most used words in D&G 'New in' SS2020 Women collection",
                        save="SS2020_D&G_word_frequency.jpg")

    df_rel['brand'] = 'd&g'

    return df_rel
