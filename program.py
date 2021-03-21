# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 09:22:31 2021

@author: Alvin
"""

from bs4 import BeautifulSoup
import requests

url = "https://insidelearn.com/courses/all"

def parserURL(url=""):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

soup = parserURL(url)
allsoupcourse = soup.findAll('div',{'class':'job-title'})

for item in allsoupcourse:
    linktovisit = item.find('a')['href']
    content = parserURL(linktovisit)
    print(content.find('a',{'class':'btn btn-purplex btn-effect mt15 mb5'})['href'])
