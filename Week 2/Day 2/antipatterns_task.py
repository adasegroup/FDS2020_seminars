#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

from src import result2dataframe, plot_horizontal_bar, TextScraper, CounterWithRefactor

URLS = ["https://us.burberry.com/womens-new-arrivals-new-in/",
        "https://us.burberry.com/womens-new-arrivals-new-in/?start=2&pageSize=120&productsOffset=&cellsOffset=8&cellsLimit=&__lang=en"]

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

df_burberry = df_rel

# In[2]:


# VERSACE

# CREATING LIST OF RELEVANT URLS
url = "https://www.versace.com/us/en-us/women/new-arrivals/new-in/"

# SCRAPING & CREATING A LIST OF LINKS


text_scraper = TextScraper(url)
doc = text_scraper.get_words('a', 'href', '/us/en-us/women/new-arrivals/new-in/')

# for url in URLS:


# DEDUPLICATING THE LIST OF LINKS
doc_uniq = set(doc)
print("Number of unique items:" + str(len(doc_uniq)))
# print(doc_uniq)

result = {}
garbage = []
for link in doc_uniq:
    if link.startswith("/us/en-us/women/new-arrivals/new-in/?"):
        continue
    words = link.replace("/us/en-us/women/new-arrivals/new-in/", "").split("/")
    words = words[0].split("-")

    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1

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

df_versace = df_rel

# In[3]:


# CREATING LIST OF RELEVANT URLS
URLS_i = []
# URLS = list(URLS)
for i in [1, 2, 3, 4]:
    u = str("https://us.dolcegabbana.com/en/women/highlights/new-in/?page=") + str(i)
    URLS_i.append(u)

# print(URLS)

# SCRAPING & CREATING A LIST OF LINKS
doc = []
for url in URLS_i:
    text_scraper = TextScraper(url)
    doc_i = text_scraper.get_words('a', 'aria-label', 'Visit')
    doc += doc_i

# print(doc)

# DEDUPLICATING THE LIST OF LINKS
doc_uniq = set(doc)
print("Number of unique items:" + str(len(doc_uniq)))

result = {}
for link in doc_uniq:
    words = link.replace("Visit", "").replace(" product page", "").split(" ")
    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
del (result[""])

df_sorted = result2dataframe(result)
df_rel = df_sorted[df_sorted['counts'] > 4]
# print(df_rel.head())
# print(df_rel.shape)


# PLOTTING
plot_horizontal_bar(df_rel.index,  df_rel['counts'], color="#E0115F",
                    title="Most used words in D&G 'New in' SS2020 Women collection",
                    save="SS2020_D&G_word_frequency.jpg")

df_rel['brand'] = 'd&g'

df_dg = df_rel

# In[22]:


df_brands = pd.concat([df_versace.reset_index(), df_burberry.reset_index(), df_dg.reset_index()])

# In[23]:
print()

# df_brands = df_brands.drop(columns=['index'])

# In[24]:


df_brands['words'] = df_brands['words'].str.upper()

# In[29]:


# In[30]:


# integer encode
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(df_brands['words'])
print(integer_encoded)

# In[31]:


# binary encode
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)


# In[62]:


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


# In[63]:


def apply_brand_loop(df):
    brand_list = []
    for i in range(len(df)):
        brand = df.iloc[i]['brand']
        target = brand_target(brand)
        brand_list.append(target)
    return brand_list


# In[67]:


brands_transformed = apply_brand_loop(df_brands.copy())
y = brands_transformed

X = onehot_encoded

# In[68]:



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# In[70]:


models = []

# In[71]:



models.append(("Baseline", DummyClassifier(random_state=391488407)))

# In[72]:



# models.append(("Support vector (C=1.30)", SVC(C=1.30, gamma="scale")))
# models.append(("Support vector (C=0.45)", SVC(C=0.45, gamma="scale")))
# models.append(("Support vector (C=4.80)", SVC(C=4.80, gamma="scale")))
models.append(("Support vector (C=1.00)", SVC(C=1.00, gamma="scale")))
models.append(("Support vector (C=0.25)", SVC(C=0.25, gamma="scale")))
models.append(("Support vector (C=4.00)", SVC(C=4.00, gamma="scale")))

# In[73]:




models.append(("Random Forest", RandomForestClassifier(n_estimators=100, random_state=1283220422)))

models.append(("Logistic Regression (C=1.00)",
               LogisticRegression(C=1.00, solver="liblinear", penalty="l1")))

models.append(("Logistic Regression (C=0.25)",
               LogisticRegression(C=0.25, solver="liblinear", penalty="l1")))

models.append(("Logistic Regression (C=4.00)",
               LogisticRegression(C=4.00, solver="liblinear", penalty="l1")))

# In[74]:



models.append(("1-nn euclidean",
               KNeighborsClassifier(n_neighbors=1)))

models.append(("1-nn cosine",
               KNeighborsClassifier(n_neighbors=1, metric="cosine")))

models.append(("5-nn cosine",
               KNeighborsClassifier(n_neighbors=5, metric="cosine")))

# In[75]:


models = dict(models)

# In[76]:


for name, clf in models.items():
    clf.fit(X_train, y_train)

# In[80]:


scores = pd.Series({name: clf.score(X_test, y_test) for name, clf in models.items()}, name="Accuracy")

# In[81]:


scores

# In[ ]:
