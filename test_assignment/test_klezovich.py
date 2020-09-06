# author: Anna Klezovich
# Python 3.7.1


import re
import csv
import requests
import json
from collections import Counter
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def clean(text):
    text = re.sub('\W', ' ', text.lower())
    text = [word for word in text.split() if word.isalpha()]
    return text


def frequency(initial_text): return Counter(initial_text)


def write_csv(freq):
    with open('out_file.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['word', 'freq'])
        writer.writerows(sorted(freq.items(), key=lambda x: x[1], reverse=True))

# === functions for the second part of the task

def lemmatize(text):
    lemmas = []
    known_words = {}
    for word in text:
        if word in known_words:
            lemmas.append(known_words[word])
        else:
            result = morph.parse(word)[0].normal_form
            lemmas.append(result)
            known_words[word] = result
    return lemmas


def two_letters_o(lemmas):
    two_o_words = []
    for word in lemmas:
        if list(word).count('о') == 2:
            two_o_words.append(word)
    return two_o_words


def write_txt(data):
    with open('two_os.txt', 'w', encoding='utf-8') as f:
        for word in data:
            f.write(word + '\n')


def write_json(data):
    ordered = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    with open('freq_dict.json', 'w', encoding='utf-8') as f:
        json.dump(ordered, f, ensure_ascii=False, indent=2)


def download_from_url(url):
    pessoa = requests.get(url)
    return pessoa.text


def main():
    # first part
    path = '.\\test_text.txt'
    write_csv(frequency(clean(read_file(path))))
    # second part
    write_txt(two_letters_o(lemmatize(clean(read_file(path)))))
    url = 'http://lib.ru/POEZIQ/PESSOA/lirika.txt'
    write_json(frequency(clean(download_from_url(url))))


if __name__ == '__main__':
    main()
