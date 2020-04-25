import time
import numpy as np
import requests
import pandas as pd
from tqdm import tqdm


class Settings:

    version = 20180605
    radius = 25
    limit = 100

    # Categories to search:
    # German Restaurant: 4bf58dd8d48988d10d941735
    # Bar: 4bf58dd8d48988d116941735
    # Brewery: 50327c8591d4c4b30a586d5d
    category_list = '4bf58dd8d48988d10d941735,4bf58dd8d48988d116941735,50327c8591d4c4b30a586d5d'


class Credentials:

    def __init__(self, client_id, client_secret):

        self.client_id = client_id
        self.client_secret = client_secret


class Venues(Settings, Credentials):

    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)
        self.venue_df = pd.DataFrame()

    def get_nearby_venues(self, city_list, latitudes, longitudes):

        print("Matching biergartens in " + city_list[0] + ' to Foursquare venues...')

        venues_list = []

        for city, lat, lng in tqdm(zip(city_list, latitudes, longitudes)):

            while True:

                try:

                    # create the API request URL
                    url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{} \
                    &categoryId={}&radius={}&limit={}&intent=browse'.format(
                        self.client_id,
                        self.client_secret,
                        Settings.version,
                        lat,
                        lng,
                        Settings.category_list,
                        Settings.radius,
                        Settings.limit)

                    # make the GET request
                    results = requests.get(url).json()["response"]['groups'][0]['items']

                    # return only relevant information for each nearby venue
                    venues_list.append([(
                        city,
                        lat,
                        lng,
                        v['venue']['id'],
                        v['venue']['name'],
                        v['venue']['location']['lat'],
                        v['venue']['location']['lng'],
                        v['venue']['categories'][0]['name']) for v in results])

                    # Sleep long enough to ensure compliance with Foursquare API guidelines
                    time.sleep(0.51)

                except:
                    time.sleep(0.51)
                    continue

                break

        nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
        nearby_venues.columns = ['City',
                                 'OSM Latitude',
                                 'OSM Longitude',
                                 'venue_id',
                                 'Venue',
                                 'Venue Latitude',
                                 'Venue Longitude',
                                 'Venue Category']

        self.venue_df = nearby_venues


class Reviews(Settings, Credentials):

    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)
        self.review_df = None

    def get_venue_review(self, city_list, venue_id_list):

        print("Fetching reviews for identified biergartens in " + city_list[0] + '...')

        res_df = pd.DataFrame(columns=['venue_id', 'venue_name', 'rating', 'likes_cnt'])

        for city, venue_id in tqdm(zip(city_list, venue_id_list)):

            while True:

                try:

                    url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(
                        venue_id,
                        self.client_id,
                        self.client_secret,
                        Settings.version)

                    response = requests.get(url).json()

                    d = {
                        'city': city,
                        'venue_id': venue_id,
                        'venue_name': response['response']['venue'].get('name'),
                        'rating': response['response']['venue'].get('rating'),
                    }

                    if response['response']['venue']['likes']:
                        d['likes_cnt'] = response['response']['venue']['likes'].get('count')
                    else:
                        d['likes_cnt'] = np.NaN

                    res_df = res_df.append(d, ignore_index=True)

                    # Sleep long enough to ensure compliance with Foursquare API guidelines
                    time.sleep(0.51)

                except:
                    time.sleep(0.51)
                    continue

                break

        self.review_df = res_df

        return self.review_df
