import urllib.request
from bs4 import BeautifulSoup
import yaml
import requests

config_file_path = "config.yml"


def url_patter(zipcode):
    with open(config_file_path) as paramStream:
        param_dict = yaml.load(paramStream)
        return param_dict["parameters"]["main_url_pattern"].format(zip_code=zipcode)


def configured_zip():
    with open(config_file_path) as paramStream:
        param_dict = yaml.load(paramStream)
        return param_dict["parameters"]["zipcode"]


dict = []

def main():

    rev_data_list = []

    url = "https://www.yelp.com/biz/girl-and-the-goat-chicago"
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, "html.parser")

    class1 ="ylist ylist-bordered reviews"
    lis2 = soup.find_all("ul", class_= class1)[0]

    lis = lis2.find_all("li", recursive=False)
    print(len(lis))

    #lis = soup.find_all('ul', attrs={'class:ylist ylist-bordered reviews'})
    for li in lis:

        new_review_dict = {}

        if len(li.find_all("div", class_="review review--with-sidebar")) != 0:
            rating = li.find_all("div", class_="review review--with-sidebar")[0]
            new_review_dict["user_id"] = rating.attrs["data-signup-object"]
            print(rating.attrs["data-signup-object"])

        if len(li.find_all("a", class_="user-display-name js-analytics-click")) != 0:
            rating = li.find_all("a", class_="user-display-name js-analytics-click")[0]
            new_review_dict["user_name"] = rating.text
            print(rating.text)

        if len(li.find_all("div", class_ = "i-stars")) != 0:
            rating = li.find_all("div", class_ = "i-stars")
            new_review_dict["rating"] = rating[0].attrs["title"]
            print(rating[0].attrs["title"])

        if len(li.find_all("p")) != 0:
            rating = li.find_all("p")
            new_review_dict["review"] = rating[0].text
            print(rating[0].text)

        if len(li.find_all("a", class_="ybtn ybtn--small useful js-analytics-click")) != 0:
            child = li.find_all("a", class_="ybtn ybtn--small useful js-analytics-click")[0]
            new_review_dict["useful_votes"] = child.find_all("span",class_="count")[0].text
            print(child.find_all("span",class_="count")[0].text)

        if len(li.find_all("a", class_="ybtn ybtn--small funny js-analytics-click")) != 0:
            child = li.find_all("a", class_="ybtn ybtn--small funny js-analytics-click")[0]
            new_review_dict["funny_votes"] = child.find_all("span", class_="count")[0].text
            print(child.find_all("span", class_="count")[0].text)

        if len(li.find_all("a", class_="ybtn ybtn--small cool js-analytics-click")) != 0:
            child = li.find_all("a", class_="ybtn ybtn--small cool js-analytics-click")[0]
            new_review_dict["cool_votes"] = child.find_all("span", class_="count")[0].text
            print(child.find_all("span", class_="count")[0].text)

        rev_data_list.append(new_review_dict)

    return rev_data_list


print(main())