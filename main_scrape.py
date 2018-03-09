from yelp_restaurants_scrape import *
from yelp_reviews_scrape import *
import csv

restaurant_csv_path = "restaurant.csv"

restaurant_list = []

header_list = [["restaurantID", "name", "location", "reviewCount", "rating", "categories", "address", "Hours", "GoodforKids", "AcceptsCreditCards", "Parking", "Attire", "GoodforGroups", "PriceRange", "TakesReservations", "Delivery", "Takeout", "WaiterService", "OutdoorSeating", "WiFi", "GoodFor", "Alcohol", "NoiseLevel", "Ambience", "HasTV", "Caters", "WheelchairAccessible", "webSite", "phoneNumber"]]

name_link = get_restaurant_link()

for x in name_link:
    restaurant_list.append(get_reviews_for_restaurant(x['link']))


with open(review_csv_path, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(header_list)
    writer.writerows(restaurant_list)
