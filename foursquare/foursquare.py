import requests
import pandas as pd


class Settings:

    version = 20180605
    radius = 20
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

    def get_nearby_venues(self, names, latitudes, longitudes):

        venues_list = []

        for lat, lng, name in zip(latitudes, longitudes, names):

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
                name,
                lat,
                lng,
                v['venue']['id'],
                v['venue']['name'],
                v['venue']['location']['lat'],
                v['venue']['location']['lng'],
                v['venue']['categories'][0]['name']) for v in results])

        nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
        nearby_venues.columns = ['Name',
                                 'Name Latitude',
                                 'Name Longitude',
                                 'venue_id',
                                 'Venue',
                                 'Venue Latitude',
                                 'Venue Longitude',
                                 'Venue Category']

        self.venue_df = nearby_venues


class Reviews(Settings, Credentials):

    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)

    def get_venue_review(self, venue_id):
        url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(
            venue_id,
            self.client_id,
            self.client_secret,
            Settings.version)

        response = requests.get(url).json()

        res_df = pd.DataFrame(columns=['venue_id', 'venue_name', 'rating', 'likes_cnt'])
        d = {
            'venue_id': venue_id,
            'venue_name': response['response']['venue']['name'],
            'rating': response['response']['venue']['rating'],
            'likes_cnt': response['response']['venue']['likes']['count']
        }
        res_df = res_df.append(d, ignore_index=True)

        return res_df
