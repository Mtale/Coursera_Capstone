import overpy
import requests
import pandas as pd

# https://worldpopulationreview.com/countries/germany-population/cities/
# Bochum-Hordel was omitted due to proximity of Bochum
# Wandsbek was omitted due to proximity of Hamburg
# City codes acquired manually from http://nominatim.openstreetmap.org/
top20_cities = {
    'Berlin': '62422'
    , 'Hamburg': '62782'
    , 'München': '62428'
    , 'Köln': '62578'
    , 'Frankfurt am Main': '62400'
    , 'Essen': '62713'
    , 'Stuttgart': '2793104'
    , 'Dortmund': '1829065'
    , 'Düsseldorf': '62539'
    , 'Bremen': '62559'
    , 'Hannover': '59418'
    , 'Leipzig': '62649'
    , 'Duisburg': '62456'
    , 'Nürnberg': '62780'
    , 'Dresden': '191645'
    , 'Bochum': '62644'
    , 'Wuppertal': '62478'
    , 'Bielefeld': '62646'
    , 'Bonn': '62508'
    , 'Mannheim': '62691'}


class OpenStreetMap:
    """
    Class to get biergartens in provided city
    """
    def __init__(self, city_name, city_id):
        self.overpass_api = overpy.Overpass()
        self.city_name = city_name
        self.city_id = city_id
        self.overpass_city_id = None
        self.api_response = None
        self.no_of_biergartens = None
        self.df_biergartens = None

    def calc_overpass_city_id(self):

        # Transform city code to a format required by Overpass API
        self.overpass_city_id = str(int(self.city_id) + 3600000000)

    def overpass_query(self):

        # Define query to Overpass API
        self.api_response = self.overpass_api.query(
            "[out:json];"
            "area(" + self.overpass_city_id + ")->.searchArea;"
                                     "("
                                     "node[amenity=biergarten](area.searchArea);"
                                     "way[amenity=biergarten](area.searchArea);"
                                     "relation[amenity=biergarten](area.searchArea);"
                                     ");"
                                     "(._;>;);"
                                     "out center;"
        )

    def get_biergartens_for_city(self):

        print("Finding biergartens in " + self.city_name + '...')

        # Transform city code to a format required by Overpass API
        self.calc_overpass_city_id()

        # Execute query to Overpass API
        self.overpass_query()

        # Parse response
        parsing = Parsing(self.api_response)
        res_df = parsing.parse_response()

        # Store parsed results in class attributes
        res_df['city'] = self.city_name
        res_df['city_id'] = self.city_id
        self.df_biergartens = res_df
        self.no_of_biergartens = res_df.shape[0]

        print("Found " + str(self.no_of_biergartens) + " biergartens in " + self.city_name)

        return res_df


class Parsing:
    """
    Class to parse Overpass API response
    """

    def __init__(self, response):
        self.response = response

    def parse_response(self):

        # Parse nodes, ways and relations in response
        nodes_df = self.parse_nodes(self.response)
        ways_df = self.parse_ways(self.response)
        relations_df = self.parse_relations(self.response)

        # Collect results into a single dataframe
        response_df = pd.DataFrame()
        if not nodes_df.empty:
            response_df = response_df.append(nodes_df)
        if not ways_df.empty:
            response_df = response_df.append(ways_df)
        if not relations_df.empty:
            response_df = response_df.append(relations_df)

        # Return single dataframe
        return response_df.reset_index(drop=True)

    @staticmethod
    def parse_nodes(response):

        # Create empty dataframe for parsing results
        res_df = pd.DataFrame()

        # Do for all nodes in response
        for i, node in enumerate(response.nodes):

            # Ensure that tags exist
            if not not response.nodes[i].tags:

                # Ensure that amenities exist
                if 'amenity' in response.nodes[i].tags.keys():

                    # Get coordinates and tags if amenity is biergarten
                    if response.nodes[i].tags['amenity'] == 'biergarten':
                        d = {
                            'id': response.nodes[i].id,
                            'type': 'Node',
                            'latitude': float(response.nodes[i].lat),
                            'longitude': float(response.nodes[i].lon),
                            'tags': response.nodes[i].tags
                        }

                        # Append dict to results dataframe
                        res_df = res_df.append(d, ignore_index=True)

        return res_df

    @staticmethod
    def parse_ways(response):

        # Create empty dataframe for parsing results
        res_df = pd.DataFrame()

        # Do for all ways in response
        for i, way in enumerate(response.ways):

            # Ensure that tags exist
            if not not response.ways[i].tags:

                # Ensure that amenities exist
                if 'amenity' in response.ways[i].tags.keys():

                    # Get coordinates and tags if amenity is biergarten
                    if response.ways[i].tags['amenity'] == 'biergarten':
                        d = {
                            'id': response.ways[i].id,
                            'type': 'Way',
                            'latitude': float(response.ways[i].center_lat),
                            'longitude': float(response.ways[i].center_lon),
                            'tags': response.ways[i].tags
                        }

                        # Append dict to results dataframe
                        res_df = res_df.append(d, ignore_index=True)

        return res_df

    @staticmethod
    def parse_relations(response):

        # Create empty dataframe for parsing results
        res_df = pd.DataFrame()

        # Do for all relations in response
        for i, relation in enumerate(response.relations, start=0):

            # Ensure that tags exist
            if not not response.relations[i].tags:

                # Ensure that amenities exist
                if 'amenity' in response.relations[i].tags.keys():

                    # Get coordinates and tags if amenity is biergarten
                    if response.relations[i].tags['amenity'] == 'biergarten':
                        d = {
                            'id': response.relations[i].id,
                            'type': 'Relation',
                            'latitude': float(response.relations[i].center_lat),
                            'longitude': float(response.relations[i].center_lon),
                            'tags': response.relations[i].tags
                        }

                        # Append dict to results dataframe
                        res_df = res_df.append(d, ignore_index=True)

        return res_df
