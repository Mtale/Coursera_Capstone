import overpy
import requests
import pandas as pd


class OpenStreetMap:

    def __init__(self, city_name):
        self.overpass_api = overpy.Overpass()
        self.city_name = city_name
        self.city_id = None
        self.api_response = None
        self.no_of_biergartens = None

    def get_city_id(self):
        response = requests.get(
            'https://nominatim.openstreetmap.org/search?country=Germany&city=' + self.city_name + '&format=json').json()

        self.city_id = str(response[0]['osm_id'] + 3600000000)

    def overpass_query(self):
        self.api_response = self.overpass_api.query(
            "[out:json];"
            "area(" + self.city_id + ")->.searchArea;"
                                     "("
                                     "node[amenity=biergarten](area.searchArea);"
                                     "way[amenity=biergarten](area.searchArea);"
                                     "relation[amenity=biergarten](area.searchArea);"
                                     ");"
                                     "(._;>;);"
                                     "out center;"
        )

    def get_biergartens_for_city(self):
        self.get_city_id()

        self.overpass_query()

        parsing = Parsing(self.api_response)
        res_df = parsing.parse_response()

        res_df['city'] = self.city_name
        res_df['city_id'] = self.city_id

        self.no_of_biergartens = res_df.shape[0]

        return res_df


class Parsing:

    def __init__(self, response):
        self.response = response

    def parse_response(self):

        nodes_df = self.parse_nodes(self.response)
        ways_df = self.parse_ways(self.response)
        relations_df = self.parse_relations(self.response)

        response_df = pd.DataFrame()
        if not nodes_df.empty:
            response_df = response_df.append(nodes_df)
        if not ways_df.empty:
            response_df = response_df.append(ways_df)
        if not relations_df.empty:
            response_df = response_df.append(relations_df)

        return response_df.reset_index(drop=True)

    @staticmethod
    def parse_nodes(response):

        res_df = pd.DataFrame()

        # Nodes
        for i, node in enumerate(response.nodes):

            if not not response.nodes[i].tags:

                if 'amenity' in response.nodes[i].tags.keys():

                    if response.nodes[i].tags['amenity'] == 'biergarten':
                        d = {
                            'id': response.nodes[i].id,
                            'type': 'Node',
                            'latitude': float(response.nodes[i].lat),
                            'longitude': float(response.nodes[i].lon),
                            'tags': response.nodes[i].tags
                        }
                        res_df = res_df.append(d, ignore_index=True)

        return res_df

    @staticmethod
    def parse_ways(response):

        res_df = pd.DataFrame()

        # Nodes
        for i, way in enumerate(response.ways):

            if not not response.ways[i].tags:

                if 'amenity' in response.ways[i].tags.keys():

                    if response.ways[i].tags['amenity'] == 'biergarten':
                        d = {
                            'id': response.ways[i].id,
                            'type': 'Way',
                            'latitude': float(response.ways[i].center_lat),
                            'longitude': float(response.ways[i].center_lon),
                            'tags': response.ways[i].tags
                        }
                        res_df = res_df.append(d, ignore_index=True)

        return res_df

    @staticmethod
    def parse_relations(response):

        res_df = pd.DataFrame()

        # Nodes
        for i, relation in enumerate(response.relations, start=0):

            if not not response.relations[i].tags:

                if 'amenity' in response.relations[i].tags.keys():

                    if response.relations[i].tags['amenity'] == 'biergarten':
                        d = {
                            'id': response.relations[i].id,
                            'type': 'Relation',
                            'latitude': float(response.relations[i].center_lat),
                            'longitude': float(response.relations[i].center_lon),
                            'tags': response.relations[i].tags
                        }
                        res_df = res_df.append(d, ignore_index=True)

        return res_df
