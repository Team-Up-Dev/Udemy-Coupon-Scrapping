import bs4
import requests
import json
import time
import urllib.parse
import csv

f = open('udemyCourse.json', 'w', encoding='utf-8')
csv_file = open('udemyCourse.csv', 'w', encoding='utf-8')
f_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

geeksgod_link = []
course_title = []
course_coupon = []
course_url = []
full_url = []

url = 'https://geeksgod.com/category/freecoupons/udemy-courses-free/page/2'
page_still_valid = True
page = 1
print(page)
limiter = 0
# Concatenate to get new page URL
# Obtain Request
page_url = url+'page/'+str(page)
if page > 1:
    res = requests.get(page_url)
else:
    res = requests.get(url)
# Check to see if we're on the last page
# Turn into Soup
soup = bs4.BeautifulSoup(res.text,'lxml')
# Add Authors to our set
for tag in soup.find_all("h3", {"class":"td-module-title"}):
    link = tag.a
    if 'udemy-free-course' in link['href']:
        if limiter == 16:
            limiter = 0
            break
        else:
            print(link['href'])
            geeksgod_link.append(link['href'])
            course_title.append(tag.text)
            limiter += 1
for i in geeksgod_link:
    res = requests.get(i)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    if soup.find('p', {'class':'elementor-heading-title'}) == None:
        pass
    else:
        course_coupon.append(soup.find('p', {'class':'elementor-heading-title'}).text)
    safe_link = requests.get(soup.find('a', {'class':'elementor-button-link'}, href=True)['href'])
    safe_link = bs4.BeautifulSoup(safe_link.text, 'lxml')
    time.sleep(4)
    a = safe_link.find('a', {'id':'timerbut'}, href=True)
    course_url.append(urllib.parse.unquote(a['href'])[69:].replace('?', ''))
    full_url.append(course_url[-1]+'?couponCode='+course_coupon[-1])
    print(course_url)
# Go to Next Page
print(course_coupon)
print(course_title)
print(course_url)

udemy_course = {'udemy':[]}
f_writer.writerow(['index', 'Course Title', 'Course URL', "Course Coupon", "Course Full URL"])
for i, t, c, u, fu in zip(range(len(course_coupon)), course_title, course_coupon, course_url, full_url):
    f_writer.writerow([i, t, u, c, fu])
    udemy_course['udemy'].append({'course':t, 'URL':u, 'coupon':c, 'fullUrl':fu})
json.dump(udemy_course, f, ensure_ascii=False, indent=4)