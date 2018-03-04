from bs4 import BeautifulSoup
import yaml


config_file_path = "config.yml"


def url_patter(zipcode):
    with open(config_file_path) as paramStream:
        param_dict = yaml.load(paramStream)
        return param_dict["parameters"]["main_url_pattern"].format(zip_code=zipcode)


def configured_zip():
    with open(config_file_path) as paramStream:
        param_dict = yaml.load(paramStream)
        return param_dict["parameters"]["zipcode"]


import requests

url = url_patter(configured_zip())
r = requests.get(url)
html_content = r.text
soup = BeautifulSoup(html_content, "html.parser")

lis = soup.find_all('li', attrs={'class': 'regular-search-result'})
for li in lis:
    #print(li)
    a = li.find('a').attrs['href']
    print(a)
