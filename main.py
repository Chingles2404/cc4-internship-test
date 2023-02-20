from urllib import request
import json
import pandas as pd



# ------------------------------



def get_restaurants_list():
    json_req = request.urlopen('https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json')
    data = json.load(json_req)
    restaurants = []
    for collection in data:
        for restaurant in collection["restaurants"]:
            # remove restaurants with dummy values
            if int(restaurant["restaurant"]["location"]["country_id"]) != 17:
                restaurants.append(restaurant)
    return restaurants

"""
Extract following fields:
- Restaurant Id
- Restaurant Name
- Country
- City
- User Rating Votes
- User Aggregate Rating (in float)
- Cuisines
"""
def get_restaurants_info(restaurant_list):
    result = []
    for restaurant in restaurant_list:
        temp = {}
        temp["Restaurant Id"] = restaurant["restaurant"]["id"]
        temp["Restaurant Name"] = restaurant["restaurant"]["name"]
        temp["Country"] = restaurant["restaurant"]["location"]["country_id"]
        temp["City"] = restaurant["restaurant"]["location"]["city"]
        temp["User Rating Votes"] = restaurant["restaurant"]["user_rating"]["votes"]
        temp["User Aggregate Rating"] = float(restaurant["restaurant"]["user_rating"]["aggregate_rating"])
        temp["Cuisines"] = restaurant["restaurant"]["cuisines"]
        result.append(temp)
    return result

def country_codes():
    data = pd.read_excel("Country-Code.xlsx", engine="openpyxl")
    codes = {}
    for row in range(data.shape[0]):
        codes[data.loc[row, "Country Code"]] = data.loc[row, "Country"]
    return codes
    
def modify_to_country(restaurants, codes):
    for restaurant in restaurants:
        restaurant["Country"] = codes[restaurant["Country"]]

def create_restaurants(restaurants):
    new_file = open("restaurant.csv", "w", encoding="utf-8")
    write_list = []
    temp = ""
    for keys in restaurants[0].keys():
        temp += keys + ","
    write_list.append(temp[:-1] + "\n")
    for restaurant in restaurants:
        temp = f'{restaurant["Restaurant Id"]},{restaurant["Restaurant Name"]},{restaurant["Country"]},{restaurant["City"]},{restaurant["User Rating Votes"]},{restaurant["User Aggregate Rating"]},{restaurant["Cuisines"]}\n'
        write_list.append(temp)
    new_file.writelines(write_list)
    new_file.close()


"""
restaurant_list = get_restaurants_list()
restaurants = get_restaurants_info(restaurant_list)
codes = country_codes()
modify_to_country(restaurants, codes)
create_restaurants(restaurants)
"""


# ------------------------------



def get_events(restaurant_list):
    result = []
    for restaurant in restaurant_list:
        try: 
            for event in restaurant["restaurant"]["zomato_events"]:
                start_date = event["event"]["start_date"].split("-")
                end_date = event["event"]["end_date"].split("-")
                start_year = int(start_date[0])
                start_month = int(start_date[1])
                end_year = int(end_date[0])
                end_month = int(end_date[1])
                if (end_year > 2019 or (end_year == 2019 and end_month >= 4)) and (start_year < 2019 or (start_year == 2019 and start_month <= 4)):
                    temp = {}
                    temp["Event Id"] = event["event"]["event_id"]
                    temp["Restaurant Id"] = restaurant["restaurant"]["id"]
                    temp["Restaurant Name"] = restaurant["restaurant"]["name"]
                    temp["Photo URL"] = restaurant["restaurant"]["photos_url"]
                    # some titles have newlines which do not conform to csv formatting
                    temp["Event Title"] = event["event"]["title"].strip()
                    temp["Event Start Date"] = event["event"]["start_date"]
                    temp["Event End Date"] = event["event"]["end_date"]
                    result.append(temp)
        except:
            KeyError
    return result

def create_events(restaurants):
    new_file = open("restaurant_events.csv", "w", encoding="utf-8")
    write_list = []
    temp = ""
    for key in restaurants[0].keys():
        temp += key + ","
    write_list.append(temp[:-1] + "\n")
    for restaurant in restaurants:
        temp = f'{restaurant["Event Id"]},{restaurant["Restaurant Id"]},{restaurant["Restaurant Name"]},{restaurant["Photo URL"]},{restaurant["Event Title"]},{restaurant["Event Start Date"]},{restaurant["Event End Date"]}\n'
        write_list.append(temp)
    new_file.writelines(write_list)
    new_file.close()
    print("done")


create_events(get_events(get_restaurants_list()))