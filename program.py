# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 09:22:31 2021

@author: Alvin
"""

from bs4 import BeautifulSoup
import requests

url = "https://geeksgod.com/category/freecoupons/udemy-courses-free/"

def parserURL(url=""):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

soup = parserURL(url)
allsoupcourse = soup.findAll('h3',{'class':'entry-title td-module-title'})

for item in allsoupcourse:
    linktovisit = item.find('a')['href']
    print(linktovisit)
    #content = parserURL(linktovisit)
    #print(content.find('a',{'class':'btn btn-purplex btn-effect mt15 mb5'})['href'])
    #(content)