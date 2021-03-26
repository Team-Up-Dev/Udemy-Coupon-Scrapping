import bs4
import requests
import json
import time
import urllib.parse
import csv

f = open('udemyCourse2.json', 'w', encoding='utf-8')
csv_file = open('udemyCourse2.csv', 'w', encoding='utf-8')
f_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

realdiscount_link = []
course_title = []
course_coupon = []
course_url = []
full_url = []

url = 'https://app.real.discount/editors-choices/'

limiter = 0
# Concatenate to get new page URL
# Obtain Request
res = requests.get(url)
# Check to see if we're on the last page
# Turn into Soup
soup = bs4.BeautifulSoup(res.text,'lxml')
for tag, n in zip(soup.find_all("a"), range(1, len(soup.find_all("a")))):
    if n == 1:
        continue
    if 'offer' in tag['href']:
        if limiter == 12:
            limiter = 0
            break
        else:
            realdiscount_link.append('https://app.real.discount'+tag['href'])
            limiter += 1
            print(realdiscount_link[-1])
for h in soup.find_all('h3', {'class':'card-title'}):
    course_title.append(h.text)
for i in realdiscount_link:
    res = requests.get(i)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    for tag in soup.find_all('a'):
        if 'couponCode' in tag['href']:
            full_url.append(urllib.parse.unquote(tag['href'])[110:])
            print(full_url[-1][:full_url[-1].index('?')])
            break
    course_url.append(full_url[-1][:full_url[-1].index('?')])
    course_coupon.append(full_url[-1][full_url[-1].index('?couponCode=')+12:])
realdiscount_link = []
# Go to Next
print(course_coupon)
print(course_title)
print(course_url)
print(full_url)

udemy_course = {'udemy':[]}
f_writer.writerow(['index', 'Course Title', 'Course URL', "Course Coupon", "Course Full URL"])
for i, t, c, u, fu in zip(range(1, len(course_coupon)+1), course_title, course_coupon, course_url, full_url):
    f_writer.writerow([i, t, u, c, fu])
    udemy_course['udemy'].append({'course':t, 'URL':u, 'coupon':c, 'fullUrl':fu})
json.dump(udemy_course, f, ensure_ascii=False, indent=4)