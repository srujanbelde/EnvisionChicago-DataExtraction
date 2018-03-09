from bs4 import BeautifulSoup
import yaml
import sys
import requests


config_file_path = "config.yml"


def url_pattern(zipcode):
    with open(config_file_path) as paramStream:
        param_dict = yaml.load(paramStream)
        return param_dict["parameters"]["main_url_pattern"].format(zip_code=zipcode)


def configured_zip():
    with open(config_file_path) as paramStream:
        param_dict = yaml.load(paramStream)
        return param_dict["parameters"]["zipcode"]


def url_next_pattern(zipcode, count):
    with open(config_file_path) as paramStream:
        param_dict = yaml.load(paramStream)
        return param_dict["parameters"]["main_url_next_page_pattern"].format(zip_code=zipcode, count=count)


def create_soup(curr_count):
    if curr_count == 0:
        url = url_pattern(configured_zip())
    else:
        url = url_next_pattern(configured_zip(),curr_count)
    r = requests.get(url)
    html_content = r.text
    soup_obj = BeautifulSoup(html_content, "html.parser")
    return soup_obj

def get_restaurant_link():
    restaurant_link_list = []
    restaurant_name_list = []
    restaurant_zipcodes_list = []
    restaurant_complete_details_list = []

    soup = create_soup(0)
    print("Extracting links....")
    limit = soup.find('span', attrs={'class': 'pagination-results-window'}).text.strip()[-4:]
    limit = int(limit)
    count = 10

    while count <= limit:
        lis = soup.find_all('li', attrs={'class': 'regular-search-result'})
        for li in lis:
            a = li.find('a').attrs['href']
            if a is None:
                break
            a = "https://www.yelp.com" + a
            span = li.find('span', attrs={'class': 'indexed-biz-name'})
            if span is None:
                break
            address = li.find('address')
            if address is None:
                break
            restaurant_link_list.append(a)
            restaurant_name_list.append(span.text.replace("  ", "").strip()[3:])
            sys.stdout.write("\r" + "Extracting: " + restaurant_name_list[-1] + "(" + str(int((count/limit)*100)) + "% done)")
            restaurant_zipcodes_list.append(address.text.strip()[-5:])
        soup = create_soup(count)
        err = soup.find('div', attrs={'class': 'container with-search-exception'})
        if not err is None:
            break
        count += 10

    for idx in range(0, len(restaurant_name_list)):
        if restaurant_zipcodes_list[idx] == "60610":
                detail_dict = {}
                detail_dict['name'] = restaurant_name_list[idx]
                detail_dict['link'] = restaurant_link_list[idx]
                restaurant_complete_details_list.append(detail_dict)
    sys.stdout.write("\r" + "Extracted: " + str(len(restaurant_complete_details_list)) + " links for the zipcode: 60610")
    sys.stdout.flush()
    print()
    print(restaurant_complete_details_list)
    return restaurant_complete_details_list


#print(get_restaurant_link())
