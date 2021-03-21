# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 09:22:31 2021

@author: Alvin
"""

from bs4 import BeautifulSoup
import requests
import json

url = "https://insidelearn.com/courses/all"

def parserURL(url=""):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

soup = parserURL(url)
allsoupcourse = soup.findAll('div',{'class':'job-title'})


data = {}
data['udemy'] = []   
    
for item in allsoupcourse:
    linktovisit = item.find('a')
    content = parserURL(linktovisit['href'])
    fullURL = content.find('a',{'class':'btn btn-purplex btn-effect mt15 mb5'})['href']
    data['udemy'].append({
        'course' : linktovisit.string,
        'URL' : fullURL.split('?couponCode=')[0],
        'coupon' : fullURL.split('?couponCode=')[1],
        'fullURL' : fullURL
    })
    
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)