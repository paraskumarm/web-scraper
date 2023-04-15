#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json
import csv
import sqlite3


# In[2]:


URL='https://www.theverge.com'


# In[3]:


HEADERS=({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15','Accept-Language':'en-US,en;q=0.5'})


# In[4]:


webpage=requests.get(URL,headers=HEADERS)


# In[5]:


print(webpage)


# In[6]


soup = BeautifulSoup(webpage.content, 'html.parser')


# In[7]:


data_from_script_tag=soup.find("script",id="__NEXT_DATA__")


# In[8]:


jsondata=json.loads(data_from_script_tag.contents[0])


# In[9]:


data_list=(jsondata['props']['pageProps']['hydration']['responses'][0]['data']['community']['frontPage']['placements'])


# In[10]:


data_csv={"uid":[],"title":[],"author":[],"url":[],"publishDate":[]}


# In[11]:



for i in range (0,len(data_list)):
    if(data_list[i]['placeable']!=None):
        uid=data_list[i]['placeable']['uid'][6:]
        title=data_list[i]['placeable']['title']
        author=data_list[i]['placeable']['author']['fullName']
        publishDate=data_list[i]['placeable']['publishDate']
        url=data_list[i]['placeable']['url']
        data_csv['uid'].append(uid)
        data_csv['title'].append(title)
        data_csv['author'].append(author)
        data_csv['url'].append(url)
        data_csv['publishDate'].append(publishDate)


# In[12]:


data_frame=pd.DataFrame.from_dict(data_csv)


# In[ ]:


data_frame.to_csv('16042023_verge.csv')


# In[ ]:


data_frame


# In[ ]:


sqliteConnection = sqlite3.connect('db.sqlite3')
cursor = sqliteConnection.cursor()


# In[ ]:


cursor.execute(
    '''CREATE TABLE TheVerge (
        ID CHAR(50) PRIMARY KEY     NOT NULL, 
       Headlines           TEXT    NOT NULL, 
       Author            CHAR(50)     NOT NULL, 
       url        CHAR(50), 
       date         CHAR(50)
    );'''
)  


# In[ ]:



  
# Open file 
with open('16042023_verge.csv') as file_obj:
      
    # Create reader object by passing the file 
    # object to reader method
    reader_obj = csv.reader(file_obj)
    
    # Iterate over each row in the csv 
    # file using reader object
    for row in reader_obj:
        if(row[1]=='uid'):#not reading first row
            pass
        uid=row[1]
        headlines=row[2]
        author=row[3]
        url=row[4]
        publishDate=row[5]
        cursor.execute("insert into theverge (id, Headlines, author,url,date) values (?, ?, ?, ?, ?)",
            (uid, headlines, author,url,publishDate))
        


# In[ ]:


# Commit your changes in the database    
sqliteConnection.commit()
  
# Closing the connection
sqliteConnection.close()


# In[ ]:




