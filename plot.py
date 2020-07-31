# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 09:37:56 2020

@author: barkov
"""
import datetime 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

#list_score = list_score[:3377] 
#df = pd.DataFrame(list_score) # or df.from csv 'out.csv'
df = pd.read_csv('out.csv')
#df.columns = ['comments', 'likes', 'favs', 'red_key', 'time', 'holiday', 'views']


# settings
df = df.drop(df[df.red_key == True].index) # False = only posts from redactors
df = df.drop(df[df.holiday == True].index) # False = only weekends 


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
    
# there is definetely a way to do it properly    
def score_in_range(start, end, row, range_num):
    if time_in_range(start,end, row.time):
        no_art[range_num] = no_art[range_num] + 1
        no_com[range_num] = no_com[range_num] + row.comments
        no_likes[range_num] = no_likes[range_num] + row.likes
        no_favs[range_num] = no_favs[range_num] + row.favs
        no_views[range_num] = no_views[range_num] + row.views 
        if row.red_key == True:
            no_redact[range_num] = no_redact[range_num] + 1 

no_art = [0] * 48
no_com = [0] * 48
no_likes = [0] * 48
no_favs = [0] * 48 
no_views = [0] * 48 
no_redact = [0] * 48
middledates = []

#create ranges 
for index, row in df.iterrows():
    row.time = datetime.datetime.strptime(row.time, '%H:%M:%S').time()
    for i in range(23):
        score_in_range(datetime.time(i, 0, 0),datetime.time(i, 30, 0), row, i*2)
        score_in_range(datetime.time(i, 30, 0),datetime.time(i+1, 0, 0), row, i*2+1)
    score_in_range(datetime.time(23, 0, 0),datetime.time(23, 30, 0), row, 46)
    score_in_range(datetime.time(23, 30, 0),datetime.time(0, 0, 0), row, 47)

#arrange xticks names       
for i in range(23):
    middledates.append(datetime.time(i, 15, 0))
    middledates.append(datetime.time(i, 45, 0)) 
middledates.append(datetime.time(23, 15, 0)) 
middledates.append(datetime.time(23, 45, 0))  

lisd = [middledates, no_art, no_com, no_likes, no_favs, no_views, no_redact]    
df_ranges = pd.DataFrame(lisd)
df_ranges = df_ranges.transpose()        
df_ranges.columns = ['range', 'articles','comments','likes','favs','views','red_art']        

#get mean values
for index, row in df_ranges.iterrows():
    row.range = row.range.strftime('%H:%M')
    if row.articles == 0: 
        row.articles = 1

df_mean = pd.DataFrame()
df_mean['range'] = df_ranges.range
df_mean['view'] = df_ranges.views // df_ranges.articles
df_mean['comment'] = df_ranges.comments // df_ranges.articles
df_mean['like'] = df_ranges.likes // df_ranges.articles
df_mean['fav'] = df_ranges.favs // df_ranges.articles


# figure for total number of articles
def fig_article_num(df_mean,title):
    ind = np.arange(len(df_mean['range']))  # the x locations for the groups
    width = 0.9  # the width of the bars
    fig, ax = plt.subplots(figsize=(10,5))
    a_BSpline = interpolate.make_interp_spline(ind + width/2,df_ranges['articles'])
    x = np.linspace(ind[0], ind[47], 500)
    y = a_BSpline(x)
    ax.fill_between(x,y, color="skyblue", alpha=0.2)
    ax.fill_between(x,y, color="skyblue", alpha=0.01)
    ax.plot(x,y, color="Slateblue", alpha=0.4)
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xticks(ind)
    ax.set_xticklabels(df_mean['range'], rotation=75)
    ax.set_ylim([0,50])
    ax.set_title(title)
    ax.set_ylabel('количество постов')
    
    ax.legend(['посты'],loc='upper right')
    fig.tight_layout()
    
    plt.show()

# final figure, comments, likes, views
def fig_24_hours(df_mean,title):
    ind = np.arange(len(df_mean['range']))  # the x locations for the groups
    df_mean['view'] = df_mean['view'] // 10 
    fig, ax = plt.subplots(figsize=(13.5,6.75))
    barWidth = 0.9
    ax.bar(df_mean['range'], df_mean['comment'], width = barWidth, color = (0.3,0.1,0.4,0.6), label='comments')
    ax.bar(df_mean['range'], df_mean['like'], width = barWidth, color = (0.3,0.9,0.4,0.6), label='likes')
    
    ax2 = ax.twinx()
    
    from scipy import interpolate
    a_BSpline = interpolate.make_interp_spline(ind + barWidth/2,df_mean['view'])
    x = np.linspace(ind[0], ind[47], 500)
    y = a_BSpline(x)
    
    
    ax2.fill_between(x,y, color="skyblue", alpha=0.2)
    ax2.fill_between(x,y, color="skyblue", alpha=0.01)
    ax2.plot(x,y, color="Slateblue", alpha=0.4)
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylim([0,170])
    ax2.set_ylim([0,700])
    ax.set_ylabel('среднее количество \n комментариев/лайков на 1 пост')
    ax2.set_ylabel('среднее количество просмотров(x10) на 1 пост')
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(df_mean['range'], rotation=75)
    ax.legend(['комментарии','лайки'],loc='upper left')
    ax2.legend(['просмотры'],loc='upper right')
    fig.tight_layout()
    
    plt.show()



fig_24_hours(df_mean,'Будние дни, все посты')
fig_article_num(df_mean,'Активность редакции')
