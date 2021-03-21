# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 09:22:31 2021

@author: Alvin
"""

from bs4 import BeautifulSoup
import requests
import json
import csv

url = "https://insidelearn.com/courses/all"

def parserURL(url=""):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

soup = parserURL(url)
allsoupcourse = soup.findAll('div',{'class':'job-title'})


data = {}
data['udemy'] = []   

number = 1;
trigger1 = None
for item in allsoupcourse:
    linktovisit = item.find('a')
    content = parserURL(linktovisit['href'])
    fullURL = content.find('a',{'class':'btn btn-purplex btn-effect mt15 mb5'})['href']
    data['udemy'].append({
        'ID': number,
        'course' : linktovisit.string,
        'URL' : fullURL.split('?couponCode=')[0],
        'coupon' : fullURL.split('?couponCode=')[1],
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
            header_data[2]:fullURL.split('?couponCode=')[0],
            header_data[3]:fullURL.split('?couponCode=')[1],
            header_data[4]:fullURL
            })
    number += 1

        
        