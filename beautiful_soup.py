import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import datetime
import csv
from collections import Counter, namedtuple
from datetime import date, timedelta


#Let's get 1 day data

sdate = date(2021, 9, 17)   # start date
edate = date(2021, 9, 17)   # end date

delta = edate - sdate       # as timedelta

urls = []
url = 'https://www.ilmateenistus.ee/ilm/ilmavaatlused/vaatlusandmed/tunniandmed/?lang=en'


for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    d = day.strftime('%d')
    m = day.strftime('%m')
    y = day.strftime('%Y')

    for j in range(0,24):

        urls.append(f'{url}&filter%5Bdate%5D={d}.{m}.{y}&filter%5Bhour%5D={j}')
        
#URL = 'https://www.ilmateenistus.ee/ilm/ilmavaatlused/vaatlusandmed/tunniandmed/?lang=en&filter%5Bdate%5D=01.02.2018&filter%5Bhour%5D=0'

page = requests.get(urls[5])

soup = BeautifulSoup(page.content, 'html.parser')


tags = [tag.name for tag in soup.body.find_all(True)]
tables = soup.find_all('table', class_='table table-compressed table-striped table-bordered')
rows = tables[0].find_all('tr')
headers = [th.text for th in rows[0].find_all('th')]
td = soup.tbody.find_all("td")

headers.remove("Wind")
head_ = [th.text for th in rows[1].find_all('th')]
headers.insert(5, head_[0])
headers.insert(6, head_[1])
headers.insert(7, head_[2])


new_table = []
trow = soup.tbody.find_all("tr")
for tr in trow:
    td = tr.find_all('td')
    r = [i.text for i in td]
    print(r)
    new_table.append(r)
    
new_table_1 = pd.DataFrame(new_table)
new_table_1.columns = headers
data_table=new_table_1.apply(lambda x:x.str.replace("\n"," "))
data_table_ =data_table.apply(lambda x:x.str.replace(",","."))

time = soup.find("div", {"class": "datepicker-filter", "rel": True}).get("rel")
hour=soup.find("input", {"class": "filter-hour", "value": True}).get("value")
timestamp = []
for i in range(90):
    timestamp.append(time+'_'+hour+'GMT')
    
TS_ = pd.DataFrame({"Timestamp" : timestamp})
TS=TS_.apply(lambda x:x.str.replace(".","-"))

result = pd.concat([TS,data_table_], axis=1)
result.head()

        
        
