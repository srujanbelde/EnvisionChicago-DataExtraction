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
location_identifier = "user-location responsive-hidden-small"
friends_count_identifier = "friend-count responsive-small-display-inline-block"
review_count_identifier = "review-count responsive-small-display-inline-block"
photo_count_identifier = "photo-count responsive-small-display-inline-block"
business_name_identifier = "biz-page-title embossed-text-white"
neighborhood_identifier = "neighborhood-str-list"
map_identifier = "lightbox-map hidden"
category_identifier = "category-str-list"
hours_identifier = "table table-simple hours-table"
price_range_identifier = "business-attribute price-range"
website_identifier = "biz-website js-biz-website js-add-url-tagging"

rev_data_list = []
author_data_list = []
restaurant_data_list = []


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


def get_more_biz_info(div_tag, rest_dict):
    final_div = ""
    for div in div_tag:
        if "More business info" in div.find('h3'):
            final_div = div
            break

    for dl in final_div.find_all('dl'):
        if dl.find('dt').text.strip() == "Good for Kids":
            rest_dict['GoodforKids'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Accepts Credit Cards":
            rest_dict['AcceptsCreditCards'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Parking":
            rest_dict['Parking'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Attire":
            rest_dict['Attire'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Good for Groups":
            rest_dict['GoodforGroups'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Takes Reservations":
            rest_dict['TakesReservations'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Delivery":
            rest_dict['Delivery'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Take-out":
            rest_dict['Takeout'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Waiter Service":
            rest_dict['WaiterService'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Outdoor Seating":
            rest_dict['OutdoorSeating'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Wi-Fi":
            rest_dict['WiFi'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Good For":
            rest_dict['GoodFor'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Alcohol":
            rest_dict['Alcohol'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Noise Level":
            rest_dict['NoiseLevel'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Ambience":
            rest_dict['Ambience'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Has TV":
            rest_dict['HasTV'] = dl.find('dd').text.strip()
        elif dl.find('dt').text.strip() == "Caters":
            rest_dict['Caters'] = dl.find('dd').text.strip()
        elif "wheelchair" in dl.find('dt').text.strip().lower():
            rest_dict['WheelchairAccessible'] = dl.find('dd').text.strip()
    return rest_dict


def get_reviews_for_restaurant(restaurant_url):
    print("\nExtracting Reviews....\n")

    url = restaurant_url
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, "html.parser")


    restaurant_csv = {}
    restaurant_name = soup.find('h1', attrs={'class': business_name_identifier})

    address_tag = soup.find('address').text.strip()
    address = address_tag.replace('Chicago', ', Chicago')
    address += " Neighborhood: " + soup.find('span', attrs={'class': neighborhood_identifier}).text.strip()

    rev_count_tag = soup.find_all("span", attrs={'itemprop': 'reviewCount'})[0]
    rev_count = int(rev_count_tag.text)
    rev_page_count = int(rev_count / 20) - 1

    rating = soup.find('meta', attrs={'itemprop': 'ratingValue'})

    location_obj = json.loads(soup.find('div', class_=map_identifier)['data-map-state'])
    categories_list = soup.find('span', class_=category_identifier)

    hours_tag = soup.find('table', class_=hours_identifier)
    hours = ""
    for tr in hours_tag.find_all('tr'):
        for th in tr.find_all('th'):
            hours += th.text
            for td in tr.find_all('td'):
                hours += td.text
                if tr.find('span', class_="nowrap closed") is not None or tr.find('span', class_="nowrap open") is not None:
                    break
    hours = hours.replace("\n", " ").strip()

    restaurant_csv['WheelchairAccessible'] = "No"
    div_biz_info = soup.find_all('div', class_='ywidget')
    restaurant_csv = get_more_biz_info(div_biz_info, restaurant_csv)



    price_range = soup.find('span', class_=price_range_identifier)
    website_span = soup.find('span', class_=website_identifier)
    phone_number = soup.find('span', class_="biz-phone").text.strip()

    restaurant_csv['name'] = restaurant_name.text.strip()
    restaurant_csv['restaurantID'] = location_obj['markers'][1]['resourceId']
    restaurant_csv['location'] = location_obj['center']
    restaurant_csv['address'] = address
    restaurant_csv['reviewCount'] = rev_count
    restaurant_csv['rating'] = float(rating['content'])
    restaurant_csv['categories'] = categories_list.text.replace("  ", "").replace("\n", " ").strip()
    restaurant_csv['Hours'] = hours
    restaurant_csv['PriceRange'] = price_range.text.strip()
    restaurant_csv['webSite']= website_span.find('a').text.strip()
    restaurant_csv['phoneNumber'] = phone_number
    restaurant_data_list.append(restaurant_csv)

    for i in range(0, rev_page_count):

        url = restaurant_url + "?start=" + str(i * 20)
        r = requests.get(url)
        html_content = r.text
        soup = BeautifulSoup(html_content, "html.parser")

        ul_html = soup.find_all("ul", class_=total_reviews_identifier)[0]
        li_list = ul_html.find_all("li", recursive=False)

        for li in li_list:
            generate_review_list(li)
            generate_author_list(li)

        percent = int((i * 100) / rev_page_count)
        print('\r[{0}] {1}%'.format('#' * percent, percent), end="")

    print('\r[{0}] {1}%'.format('#' * 100, 100))
    print("\nReviews successfully extracted for {0}".format(restaurant_url))
    return rev_data_list[1:]


def generate_review_list(li):
    new_review_dict = {}

    if len(li.find_all("div", class_=userid_identifier)) != 0:
        userid_tag = li.find_all("div", class_=userid_identifier)[0]
        new_review_dict["user_id"] = formatted_id(userid_tag.attrs["data-signup-object"])

    if len(li.find_all("a", class_=username_identifier)) != 0:
        username_tag = li.find_all("a", class_=username_identifier)[0]
        new_review_dict["user_name"] = username_tag.text

    if len(li.find_all("div", class_=rating_identifier)) != 0:
        rating_tag = li.find_all("div", class_=rating_identifier)[0]
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


def generate_author_list(li):
    new_author_list = []
    if len(li.find_all("div", class_=userid_identifier)) != 0:
        userid_tag = li.find_all("div", class_=userid_identifier)[0]
        new_author_list.append(formatted_id(userid_tag.attrs["data-signup-object"]))

    if len(li.find_all("a", class_=username_identifier)) != 0:
        username_tag = li.find_all("a", class_=username_identifier)[0]
        new_author_list.append(username_tag.text)

    if len(li.find_all("li", class_=location_identifier)) != 0:
        location_tag = li.find_all("li", class_=location_identifier)[0]
        new_author_list.append(location_tag.text.strip())

    if len(li.find_all("li", class_=friends_count_identifier)) != 0:
        friend_count_tag = li.find_all("li", class_=friends_count_identifier)[0]
        new_author_list.append(friend_count_tag.text.strip().split(" ")[0])

    if len(li.find_all("li", class_=review_count_identifier)) != 0:
        review_count_tag = li.find_all("li", class_=review_count_identifier)[0]
        new_author_list.append(review_count_tag.text.strip().split(" ")[0])

    if len(li.find_all("li", class_=photo_count_identifier)) != 0:
        photo_count_tag = li.find_all("li", class_=photo_count_identifier)[0]
        new_author_list.append(photo_count_tag.text.strip().split(" ")[0])

    author_data_list.append(new_author_list)


print("{0} {1}".format("\n\n", get_reviews_for_restaurant("https://www.yelp.com/biz/meli-cafe-and-juice-bar-chicago")))

get_reviews_for_restaurant("https://www.yelp.com/biz/big-and-littles-restaurant-chicago-3")
for x in restaurant_data_list:
    for key, value in x.items():
        print(key, value)
