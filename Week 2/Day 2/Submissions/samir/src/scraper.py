import requests
from bs4 import BeautifulSoup


class TextScraper(object):
    def __init__(self, url):
        self.url = url
        self.text_soup = self._get_text()

    def _get_text(self):
        r = requests.get(self.url)
        html_doc = r.text
        return BeautifulSoup(html_doc, "html.parser")

    def get_words(self, tag_to_find, label_to_get, word):
        doc = [t.get(label_to_get)
               for t in self.text_soup.find_all(tag_to_find)
               if t.get(label_to_get) is not None and (word in t.get(label_to_get) or t.get(label_to_get).startswith(word))]
        return doc


class CounterWithRefactor(object):
    def __init__(self, doc_uniq):
        self.doc_uniq = doc_uniq

    def get_count(self, replace_strings, split_char, split_char_2=False, must_start_with=False):
        result = {}
        for link in self.doc_uniq:
            if must_start_with and link.startswith(must_start_with):
                continue

            for _str in replace_strings:
                words = link.replace(_str, "")

            words = words.split(split_char)

            if split_char_2:
                words[0] = words[0].split(split_char_2)

            for word in words:
                if isinstance(word, list):
                    for word_i in word:
                        if word_i in result.keys():
                            result[word_i] += 1
                        else:
                            result[word_i] = 1
                else:
                    if word in result.keys():
                        result[word] += 1
                    else:
                        result[word] = 1

        return result
