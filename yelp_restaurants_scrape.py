from bs4 import BeautifulSoup

import requests

url = "https://www.yelp.com/search?find_desc=&find_loc=Chicago%2C+IL+60610&ns=1"
r = requests.get(url)
html_content = r.text
soup = BeautifulSoup(html_content, "html.parser")

lis = soup.find_all('li', attrs={'class': 'regular-search-result'})
for li in lis:
    #print(li)
    a = li.find('a').attrs['href']
    print(a)
