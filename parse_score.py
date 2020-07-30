# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:49:22 2020

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
browser = webdriver.Chrome()

browser.get("https://dtf.ru/new")
time.sleep(1)



elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 2800

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1
    print(no_of_pagedowns)
    if no_of_pagedowns == 1300:
        post_elems = browser.find_elements_by_class_name("content-feed__link")
        links1 = [elem.get_attribute('href') for elem in post_elems]

post_elems = browser.find_elements_by_class_name("content-feed__link")
links = [elem.get_attribute('href') for elem in post_elems]

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 


list_score = []

def get_entry_data(entry):
    entry = entry.replace('{','')
    entry = entry.replace('}','')
    entry = entry.replace('\"','')
    if 'editor' in entry:
        red_key = True
    else:
        red_key = False
    entry = entry.split(':',12)
    entry = [str.split(',',1) for str in entry]
    comments = int(entry[4][0])
    likes = int(entry[5][0])
    favs = int(entry[6][0])
    time = entry[12][1]
    time = time.split(' ',5)[4]
    time = datetime.datetime.strptime(time, '%H:%M:%S').time()
    if 'Sun' in entry[12][0] or 'Sat' in entry[12][0]:
        holiday = True
    else:
        holiday = False
    return [comments, likes, favs, red_key, time, holiday]
linknum = 0
for link in links:
    time.sleep(0.2)
    #if linknum > 2500:
        #time.sleep(0.3)
    request=urllib.request.Request(link,None,headers) #The assembled request
    try:
        response = urllib.request.urlopen(request)
    except Exception:
        print('pass witch exception')
        pass
    else:
        data = response.read() # The data u need
        soup = BeautifulSoup(data, 'html.parser')
        entry = soup.find('div',{'class':'l-hidden entry_data'}).text
        views = soup.find('span',{'class':'views__value'}).text
        #for div in soup.findAll('div',{'class':'review_body'}):
        #    text.append(div.text.strip())
        try:
            views = views.replace('\xa0','')
            views = int(views)
        except Exception:
            views = 0
        score = get_entry_data(entry) + [views]
        list_score.append(score)
        linknum = linknum + 1
        print(linknum)

df = pd.DataFrame(list_score)
#df = df.transpose()
df.columns = ['comments', 'likes', 'favs', 'red_key', 'time', 'holiday', 'views']
df.to_csv('out.csv')

