# -*- coding: utf-8 -*-


import time
import pandas as pd
import urllib.request
import json
import csv
# settings


link = 'https://api.dtf.ru/v1.8/timeline/index/recent?count=5' #  entries for recent



user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 

request=urllib.request.Request(link,None,headers) 
response = urllib.request.urlopen(request)
data = response.read()
entry = json.loads(data)
entries = []
i = 0
entry['result'][0]['date'] = 1596528488
while entry['result'][0]['date'] > 1593561600:
    
    link = 'https://api.dtf.ru/v1.8/timeline/index/recent?count=50&offset=' + str(i * 50)
    request=urllib.request.Request(link,None,headers) 
    response = urllib.request.urlopen(request)
    entry = json.loads(response.read())
    entries.append(entry)
    i = i + 1
    print(i)
    time.sleep(0.5)

ids = [] 
subsites = []   
for elem in entries:
    for i in range(len(elem['result'])):
        ids.append(elem['result'][i]['id'])
        subsites.append([elem['result'][i]['subsite']['id'],elem['result'][i]['subsite']['name']])
        



with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows([ids, subsites])  
#ids = ids[:15] #testing purposes


comments = []
counter = 0
for i in range(len(ids)):
    link = 'https://api.dtf.ru/v1.8/entry/' + str(ids[i]) + '/comments/popular'
    request=urllib.request.Request(link,None,headers)
    try:
        response = urllib.request.urlopen(request)
    except Exception as e:
        print(e)
        if 'Too many requests' in e:
            time.sleep(30)
        print(link)
    else:
        entry = json.loads(response.read())
        for elem in entry['result']:
            comments.append([elem['author']['id'], 
                             elem['author']['name'], 
                             elem['text'], 
                             elem['likes']['summ'], 
                             elem['date'],
                             subsites[i],
                             ids[i]])
    counter = counter + 1
    print("{:.2f}%".format((counter / len(ids))*100))
    time.sleep(1)
    
df_comms = pd.DataFrame(comments)
df_comms.columns = ['user_id', 'user_name', 'comment', 'comm_rating', 'comm_date', 'subsite', 'article_id']
df_comms.to_csv('comments_new.csv')

