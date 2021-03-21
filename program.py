# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 09:22:31 2021

@author: Alvin
"""

from bs4 import BeautifulSoup
import requests
import json
import csv
import pandas as pd

def parserURL(url=""):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

data = {}
data['udemy'] = []   
datasize = 0
number = 1;

for i in range(4):
    url = "https://insidelearn.com/courses/all?page=" + str(i+1)
    soup = parserURL(url)

    allsoupcourse = soup.findAll('div',{'class':'job-title'})
    try:
        udemyname = pd.read_csv('data.csv')['course']
    except:
        udemyname = None
    

    try:
        datasize = udemyname.size if udemyname is not None else 0
    except:
        datasize = 0
    
    trigger1 = None if datasize == 0 and udemyname is None else 1
    
    for item in allsoupcourse:
        linktovisit = item.find('a')

        try:
            searchString = udemyname.str.contains(linktovisit.string,regex=False).any()
        except:
            searchString = None
        
        if searchString is None or bool(searchString) is False:
            
            content = parserURL(linktovisit['href'])
            fullURL = content.find('a',{'class':'btn btn-purplex btn-effect mt15 mb5'})['href']
            
            try:
                splitdata = fullURL.split('?couponCode=')
            except:
                splitdata = fullURL
            
            print(splitdata == fullURL, splitdata, fullURL, len(splitdata),splitdata[0])
            data['udemy'].append({
                'ID': number,
                'course' : linktovisit.string,
                'URL' : splitdata[0] if len(splitdata) == 1 else splitdata[0],
                'coupon' : "" if len(splitdata) == 1 else splitdata[len(splitdata) - 1],
                'fullURL' : fullURL
            })
            
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)
            
            with open('data.csv','a',encoding="UTF-8",newline='') as f:
                header_data = ['ID','course','URL','coupon','fullURL']
                writer = csv.DictWriter(f, fieldnames=header_data)
                
                try:
                    if not(trigger1):
                        writer.writeheader()
                        trigger1 = 1
                        
                except:
                    trigger1 = 1
                    writer.writeheader()
                    
                writer.writerow({
                    header_data[0]:number,
                    header_data[1]:linktovisit.string,
                    header_data[2]:splitdata[0] if len(splitdata) == 1 else splitdata[0],
                    header_data[3]:"" if len(splitdata) == 1 else splitdata[len(splitdata) - 1],
                    header_data[4]:fullURL
                    })
            number += 1
    