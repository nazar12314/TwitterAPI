import tweepy
# from key import *
from geopy.geocoders import Nominatim
import folium
from typing import List
from configparser import ConfigParser


def authentication():
    """
    Authentication to Twitter API service
    return api object
    """
    config = ConfigParser()
    config.read("config.ini")
    api_key = config['keys']['api_key']
    api_key_secret = config["keys"]['api_key_secret']
    access_token = config['keys']['access_token']
    access_token_secret = config['keys']['access_token_secret']
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def get_locations_of_friends(api: object, screen_name: str, count: int):
    """
    A function to find locations of friends of given person
    Takes API object, name of the Twitter user and amount of friends
    returns List of friends with locations converted into coordinates via geopy
    """
    geolocator = Nominatim(user_agent="my_user_agent")
    result = {}
    friends = api.get_friends(screen_name=screen_name, count=50)
    for friend in friends:
        try:
            location = geolocator.geocode(friend.location)
            if location is not None:
                result[friend.screen_name] = (location.latitude, location.longitude)
        except Exception:
            continue

    return list(result.items())[:int(count)]


def create_map(data: List):
    """
    Creates a web-map
    Data -> None
    """
    map_object = folium.Map(location=[49.8397, 24.0297], zoom_start=6)
    for marker in data:
        i_frame = folium.IFrame(f"<strong>{marker[0]}</strong><br><br><strong>")
        popup = folium.Popup(i_frame, min_width=100, max_width=100)
        folium.Marker(marker[1], popup=popup).add_to(map_object)
    map_object.save("templates/map.html")


def create_web_page(name, count=50):
    """
    A main function that creates a web-page of given coordinates of friends received from Twitter API
    """
    api = authentication()
    data = get_locations_of_friends(api, name, count)
    create_map(data)
