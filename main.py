from urllib import request
import json
import pandas as pd



# ------------------------------



def get_restaurants_list():
    json_req = request.urlopen('https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json')
    data = json.load(json_req)
    restaurants = []
    for collection in data:
        restaurants += collection["restaurants"]
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
    counter = 0
    while counter < len(restaurants):
        try:
            restaurants[counter]["Country"] = codes[restaurants[counter]["Country"]]
        except:
            # By doing
            # print(restaurant["Country"], restaurant["Restaurant Name"])
            # It was discovered that the country codes are consistently 17.
            # Upon looking at the JSON file, it was observed that all restaurants with country code 17 had their city listed as Dummy
            # Therefore, we will assume that these restaurants do not exist, and we will remove these entries
            print(restaurants[counter])
            restaurants.pop(counter)
            counter -= 1
            KeyError
        counter += 1

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



restaurant_list = get_restaurants_list()
restaurants = get_restaurants_info(restaurant_list)
codes = country_codes()
modify_to_country(restaurants, codes)
create_restaurants(restaurants)



# ------------------------------



def get_events():
    json_req = request.urlopen('https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json')
    data = json.load(json_req)
    restaurants = data[0]["restaurants"]
    print(len(restaurants))
    result = []
    for restaurant in restaurants:
        try: 
            for event in restaurant["restaurant"]["zomato_events"]:
                start_month = int(event["event"]["start_date"].split("-")[1])
                end_month = int(event["event"]["end_date"].split("-")[1])
                print(start_month, end_month)
        except:
            KeyError

#get_events()