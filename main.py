from urllib import request
import json
import pandas as pd



# ------------------------------
# Function to create a general list of restaurants 



def get_restaurants_list():
    """ Add the multiple lists of restaurants without dummy restaurants and return the full list of actual restaurants """
    json_req = request.urlopen('https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json')
    data = json.load(json_req)
    restaurants = []
    for collection in data:
        for restaurant in collection["restaurants"]:
            # remove restaurants with dummy values
            if int(restaurant["restaurant"]["location"]["country_id"]) != 17:
                restaurants.append(restaurant)
    return restaurants



# ------------------------------
# Part 1: Extract the following fields and store the data as restaurants.csv



def get_restaurants_info(restaurant_list):
    """
    Extract the following fields:
    - Restaurant Id
    - Restaurant Name
    - Country
    - City
    - User Rating Votes
    - User Aggregate Rating (in float)
    - Cuisines
    And return it as a list of dictionaries

    Keyword arguments:
    restaurant_list -- the list of restaurants obtained from get_restaurants_list()
    """
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
    """ Extract country codes from the Country-Code.xlsx Excel sheet and return the information as a dictionary """
    data = pd.read_excel("Country-Code.xlsx", engine="openpyxl")
    codes = {}
    for row in range(data.shape[0]):
        codes[data.loc[row, "Country Code"]] = data.loc[row, "Country"]
    return codes
    
def modify_to_country(restaurants, codes):
    """
    Replaces the country code in each restaurant's information with the country name

    Keyword arguments:
    restaurants -- the list of dictionaries storing the restaurants' information
    codes -- the dictionary of country codes obtained from country_codes()
    """
    for restaurant in restaurants:
        restaurant["Country"] = codes[restaurant["Country"]]

def create_restaurants(restaurants):
    """
    Creates the file restaurant.csv that displays the information of each restaurant

    Keyword arguments:
    restaurants -- the list of dictionaries storing the restaurants' information
    """
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
    print("File restaurant.csv created successfully.")



# ------------------------------
# Part 2: Extract the list of restaurants that have past event in the month of April 2019 and store the data as restaurant_events.csv



def get_events(restaurant_list):
    """
    Extract the following fields:
    - Event Id
    - Restaurant Id
    - Restaurant Name
    - Photo URL
    - Event Title
    - Event Start Date
    - Event End Date
    And return it as a list of dictionaries

    Keyword arguments:
    restaurant_list -- the list of restaurants obtained from get_restaurants_list()
    """
    result = []
    for restaurant in restaurant_list:
        if "zomato_events" in restaurant["restaurant"].keys():
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
                    temp["Photo URL"] = event["event"]["photos"]
                    # some titles have newlines which do not conform to CSV formatting
                    temp["Event Title"] = event["event"]["title"].strip()
                    temp["Event Start Date"] = event["event"]["start_date"]
                    temp["Event End Date"] = event["event"]["end_date"]
                    result.append(temp)
    return result

def get_photo_url(events):
    """
    Replaces the list of photos in each event's information with a list of URLs

    Keyword arguments:
    events -- the list of dictionaries storing the events' information
    """
    for event in events:
        temp = []
        if len(event["Photo URL"]) == 0:
            temp.append("NA")
        else:
            for photo in event["Photo URL"]:
                temp.append(photo["photo"]["url"])
        event["Photo URL"] = temp

def create_events(events):
    """
    Creates the file restaurant_events.csv that displays the information of each restaurant event

    Keyword arguments:
    events -- the list of dictionaries storing the events' information
    """
    new_file = open("restaurant_events.csv", "w", encoding="utf-8")
    write_list = []
    temp = ""
    for key in events[0].keys():
        temp += key + ","
    write_list.append(temp[:-1] + "\n")
    for event in events:
        temp = f'{event["Event Id"]},{event["Restaurant Id"]},{event["Restaurant Name"]},{";".join(event["Photo URL"])},{event["Event Title"]},{event["Event Start Date"]},{event["Event End Date"]}\n'
        write_list.append(temp)
    new_file.writelines(write_list)
    new_file.close()
    print("File restaurant_events.csv created successfully.")



# ------------------------------
# Part 3: Determine the threshold for the different rating text based on aggregate rating



def get_ratings(restaurant_list):
    """
    Find the range of aggregate ratings for each rating text and print the ranges out

    Rating texts for the ranges to be found:
    - Excellent
    - Very Good
    - Good
    - Average
    - Poor

    Keyword arguments:
    restaurant_list -- the list of restaurants obtained from get_restaurants_list()
    """
    dict_keys = ["Excellent", "Very Good", "Good", "Average", "Poor"]
    ratings_dict = {}
    for key in dict_keys:
        ratings_dict[key] = {"lower": 5, "upper": 0}
    
    for restaurant in restaurant_list:
        # ensure that the rating text is in title case
        text = restaurant["restaurant"]["user_rating"]["rating_text"].title()
        aggregate = float(restaurant["restaurant"]["user_rating"]["aggregate_rating"])
        if text in ratings_dict.keys():
            if aggregate < ratings_dict[text]["lower"]:
                ratings_dict[text]["lower"] = aggregate
            if aggregate > ratings_dict[text]["upper"]:
                ratings_dict[text]["upper"] = aggregate
    
    print("The ranges of the aggregates for each rating text are")
    for key in ratings_dict.keys():
        print(f'{key}: {ratings_dict[key]["lower"]} - {ratings_dict[key]["upper"]}')


# ------------------------------
# Running of functions for the various parts



restaurant_list = get_restaurants_list()

# Part 1
restaurants = get_restaurants_info(restaurant_list)
codes = country_codes()
modify_to_country(restaurants, codes)
create_restaurants(restaurants)

# Part 2
events = get_events(restaurant_list)
get_photo_url(events)
create_events(events)

# Part 3
get_ratings(restaurant_list)