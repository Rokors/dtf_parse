# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:10:05 2020

@author: barkov
"""

import pandas as pd
import numpy as np

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer, snowball
from string import punctuation
from collections import Counter
from pymystem3 import Mystem
from collections import OrderedDict
import re
import warnings
from rutermextract import TermExtractor

term_extractor = TermExtractor()
warnings.filterwarnings("ignore", category=DeprecationWarning)
porter = PorterStemmer()
wnl = WordNetLemmatizer() 
mystem = snowball.RussianStemmer()


stop = stopwords.words('english')
stop.append("но")
stop.append("и")
stop.append("это")
stop.append("или")
stop.append("на")
stop.append("их")
stop.append('по')
stop.append('в')
stop.append('the')
stop.append('of')
stop.append('and')
stop.append('to')
stop.append('of')
stop.append('be')
stop.append('with')
stop.append('that')
stop.append('plus')
stop.append('at')
stop.append('for')
stop.append('http')
stop.append('are')
stop.append('http')
stop = stop + stopwords.words('russian')
stop.append('комментариев')
stop.append('комментария')
stop = set(stop)

def tokenizer(text):

    tokens_ = [word_tokenize(sent) for sent in sent_tokenize(text)]

    tokens = []
    for token_by_sent in tokens_:
        tokens += token_by_sent

    tokens = list(filter(lambda t: t.lower() not in stop, tokens))
    tokens = list(filter(lambda t: t not in punctuation, tokens))
    tokens = list(filter(lambda t: t not in [u"'s", u"n't", u"...", u"''", u'``', u'\u2014', u'\u2026', u'\u2013'], tokens))
     
    filtered_tokens = []
    for token in tokens:
        #token = mystem.stem(token)
        token1 = wnl.lemmatize(token)
        token1 = token1.encode('ascii', 'ignore').decode('ascii')

        #if re.search('[a-zA-Zа-яА-ЯёЁ]', token):
        if re.search('[a-zA-Zа-яА-ЯёЁ]', token1):
            filtered_tokens.append(token1)

    filtered_tokens = list(map(lambda token: token.lower(), filtered_tokens))

    return filtered_tokens

def get_keywords(tokens, num):
    return Counter(tokens).most_common(num)

def build_article_df(raw_data):
    articles = []
    for row in raw_data:
        try:
            data = row
              #data = data.encode('ascii', 'ignore').decode('ascii')
            #document = tokenizer(data)
            #top_5 = get_keywords(document, 3)
            #top_5 = [x[0] for x in top_5]
            # LIMIT SHOULD BE LOWER FOR BIG DATA (3)
            term = term_extractor(data,limit=5,nested=False)
            term1 = [elem.normalized for elem in term]
#              unzipped = zip(*top_5)
#              kw= list(unzipped[0])
#              kw=",".join(str(x) for x in kw)
            #articles.append((top_5 + term1))
            articles.append((term1))
            
        except Exception as e:
            print(e)
            #print data
            #break
            pass
        #break
    #article_df = pd.DataFrame(articles, columns=['keywords', 'title', 'pubdate'])
    return articles

#articles = build_article_df(raw_data)
articles = build_article_df(list_texts)    
#articles = articles[:2]
#articles = pd.DataFrame(articles)
keywords_array= []
for row in articles:
    keywords = row
    for kw in keywords:
        keywords_array.append((kw, row))
kw_df = pd.DataFrame(keywords_array).rename(columns={0:'keyword', 1:'keywords'})

document = kw_df.keywords.tolist()
names = kw_df.keyword.tolist()

document_array = document
#for item in document:
#    items = item.split(',')
#    document_array.append((items))

occurrences = OrderedDict((name, OrderedDict((name, 0) for name in names)) for name in names)

# Find the co-occurrences:
for l in document_array:
    for i in range(len(l)):
        for item in l[:i] + l[i + 1:]:
            occurrences[l[i]][item] += 1

co_occur = pd.DataFrame.from_dict(occurrences )


co_occur.to_csv('shiryaev.csv')