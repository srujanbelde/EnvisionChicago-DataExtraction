import urllib.request
from bs4 import BeautifulSoup
import yaml
import requests
import json


config_file_path = "config.yml"

funny_count_identifier = "ybtn ybtn--small funny js-analytics-click"
useful_count_identifier = "ybtn ybtn--small useful js-analytics-click"
cool_count_identifier = "ybtn ybtn--small cool js-analytics-click"
rating_identifier = "i-stars"
total_reviews_identifier = "ylist ylist-bordered reviews"
username_identifier = "user-display-name js-analytics-click"
userid_identifier = "review review--with-sidebar"


def formatted_id(userid):
    fid = userid.replace("user_id:", "")
    return fid.strip()


def formatted_rating(rating):
    frating = rating.replace("star rating", "")
    return frating.strip()


def formatted_count(count):
    fcount = 0
    if count.strip() == '':
        fcount = 0
    else:
        fcount = int(count.strip())

    return fcount


def get_reviews_for_restaurant(restaurant_url):

    print("\nExtracting Reviews....\n")

    rev_data_list = []
    url = restaurant_url
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, "html.parser")

    rev_count_tag = soup.find_all("span", attrs={'itemprop':'reviewCount'})[0]
    rev_count = int(rev_count_tag.text)
    rev_page_count = int(rev_count / 20) - 1

    for i in range(0,rev_page_count):

        ul_html = soup.find_all("ul", class_=total_reviews_identifier)[0]
        li_list = ul_html.find_all("li", recursive=False)

        for li in li_list:

            new_review_dict = {}

            if len(li.find_all("div", class_=userid_identifier)) != 0:
                userid_tag = li.find_all("div", class_=userid_identifier)[0]
                new_review_dict["user_id"] = formatted_id(userid_tag.attrs["data-signup-object"])

            if len(li.find_all("a", class_=username_identifier)) != 0:
                username_tag = li.find_all("a", class_=username_identifier)[0]
                new_review_dict["user_name"] = username_tag.text

            if len(li.find_all("div", class_ = rating_identifier)) != 0:
                rating_tag = li.find_all("div", class_ = rating_identifier)[0]
                new_review_dict["rating"] = formatted_rating(rating_tag.attrs["title"])

            if len(li.find_all("p")) != 0:
                feedback_tag = li.find_all("p")[0]
                new_review_dict["review"] = feedback_tag.text

            if len(li.find_all("a", class_=useful_count_identifier)) != 0:
                useful_count_tree = li.find_all("a", class_=useful_count_identifier)[0]
                new_review_dict["useful_votes"] = formatted_count(useful_count_tree.find_all("span", class_="count")[0].text)

            if len(li.find_all("a", class_=funny_count_identifier)) != 0:
                funny_count_tree = li.find_all("a", class_=funny_count_identifier)[0]
                new_review_dict["funny_votes"] = formatted_count(funny_count_tree.find_all("span", class_="count")[0].text)

            if len(li.find_all("a", class_=cool_count_identifier)) != 0:
                cool_count_tree = li.find_all("a", class_=cool_count_identifier)[0]
                new_review_dict["cool_votes"] = formatted_count(cool_count_tree.find_all("span", class_="count")[0].text)

            rev_data_list.append(new_review_dict)

        percent = int((i * 100)/rev_page_count)
        print('\r[{0}] {1}%'.format('#' * percent, percent), end="")

    print('\r[{0}] {1}%'.format('#' * 100, 100))
    print("\nReviews successfully extracted for {0}".format(restaurant_url))
    return rev_data_list[1:]


print("{0} {1}".format("\n\n",get_reviews_for_restaurant("https://www.yelp.com/biz/meli-cafe-and-juice-bar-chicago")))