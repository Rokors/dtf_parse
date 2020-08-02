# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 14:28:51 2020

@author: barkov
"""


import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime 
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import json

# settings


#link = 'https://api.dtf.ru/v1.8/subsites_list/sections' # get subsites
#link = 'https://api.dtf.ru/v1.8/subsite/64959/timeline/new?count=50&offset=50' #  entries for subsite
link = 'https://api.dtf.ru/v1.8/user/11643/entries?count=50&offset=450' # entries for user (blog)


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 

request=urllib.request.Request(link,None,headers) 
response = urllib.request.urlopen(request)
data = response.read()
entry = json.loads(data)

#list_texts = [] # testing purposes
article_stats = []
# add time to stats
for i in range(len(entry['result'])):
    html = entry['result'][i]['entryContent']['html']
    soup = BeautifulSoup(html, 'html.parser')
    text = []
    
    for div in soup.find_all('div', class_ ="l-island-a"):
        text.append(div.text.strip())
    text.pop(0)
    text = ' '.join([str(elem) for elem in text])
    #text = str(text)
    text = entry['result'][i]['title'] + ' ' + text
    list_texts.append(text)
    print(i)
 
print(entry['result'][i]['dateRFC'])