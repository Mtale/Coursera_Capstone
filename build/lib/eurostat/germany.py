import requests
from pyjstat import pyjstat
import pandas as pd

from openstreetmap import openstreetmap


class Germany:
    """
    Parent class containing methods and attributes needed in all dataset queries
    """

    def __init__(self):

        self.url_constant_beginning = 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/'

        # https://ec.europa.eu/eurostat/cache/metadata/en/urb_esms.htm
        # Annex: List of Cities 2018
        self.german_cities = [
            'DE001C1'  # Berlin
            , 'DE002C1'  # Hamburg
            , 'DE003C1'  # München
            , 'DE004C1'  # Köln
            , 'DE005C1'  # Frankfurt am Main
            , 'DE006C1'  # Essen
            , 'DE007C1'  # Stuttgart
            , 'DE008C1'  # Leipzig
            , 'DE009C1'  # Dresden
            , 'DE010C1'  # Dortmund
            , 'DE011C1'  # Düsseldorf
            , 'DE012C1'  # Bremen
            , 'DE013C1'  # Hannover
            , 'DE014C1'  # Nürnberg
            , 'DE015C1'  # Bochum
            , 'DE017C1'  # Bielefeld
            , 'DE018C1'  # Halle an der Saale
            , 'DE019C1'  # Magdeburg
            , 'DE020C1'  # Wiesbaden
            , 'DE021C1'  # Göttingen
            , 'DE022C1'  # Mülheim a.d.Ruhr
            , 'DE023C1'  # Moers
            , 'DE025C1'  # Darmstadt
            , 'DE026C1'  # Trier
            , 'DE027C1'  # Freiburg im Breisgau
            , 'DE028C1'  # Regensburg
            , 'DE029C1'  # Frankfurt (Oder)
            , 'DE030C1'  # Weimar
            , 'DE031C1'  # Schwerin
            , 'DE032C1'  # Erfurt
            , 'DE033C1'  # Augsburg
            , 'DE034C1'  # Bonn
            , 'DE035C1'  # Karlsruhe
            , 'DE036C1'  # Mönchengladbach
            , 'DE037C1'  # Mainz
            , 'DE039C1'  # Kiel
            , 'DE040C1'  # Saarbrücken
            , 'DE041C1'  # Potsdam
            , 'DE042C1'  # Koblenz
            , 'DE043C1'  # Rostock
            , 'DE044C1'  # Kaiserslautern
            , 'DE045C1'  # Iserlohn
            , 'DE046C1'  # Esslingen am Neckar
            , 'DE047C1'  # Hanau
            , 'DE048C1'  # Wilhelmshaven
            , 'DE049C1'  # Ludwigsburg
            , 'DE050C1'  # Tübingen
            , 'DE051C1'  # Villingen-Schwenningen
            , 'DE052C1'  # Flensburg
            , 'DE053C1'  # Marburg
            , 'DE054C1'  # Konstanz
            , 'DE055C1'  # Neumünster
            , 'DE056C1'  # Brandenburg an der Havel
            , 'DE057C1'  # Gießen
            , 'DE058C1'  # Lüneburg
            , 'DE059C1'  # Bayreuth
            , 'DE060C1'  # Celle
            , 'DE061C1'  # Aschaffenburg
            , 'DE062C1'  # Bamberg
            , 'DE063C1'  # Plauen
            , 'DE064C1'  # Neubrandenburg
            , 'DE065C1'  # Fulda
            , 'DE066C1'  # Kempten (Allgäu)
            , 'DE067C1'  # Landshut
            , 'DE068C1'  # Sindelfingen
            , 'DE069C1'  # Rosenheim
            , 'DE070C1'  # Frankenthal (Pfalz)
            , 'DE071C1'  # Stralsund
            , 'DE072C1'  # Friedrichshafen
            , 'DE073C1'  # Offenburg
            , 'DE074C1'  # Görlitz
            , 'DE075C1'  # Sankt Augustin
            , 'DE076C1'  # Neu-Ulm
            , 'DE077C1'  # Schweinfurt
            , 'DE078C1'  # Greifswald
            , 'DE079C1'  # Wetzlar
            , 'DE080C1'  # Speyer
            , 'DE081C1'  # Passau
            , 'DE082C1'  # Dessau-Roßlau
            , 'DE501C1'  # Duisburg
            , 'DE502C1'  # Mannheim
            , 'DE503C1'  # Gelsenkirchen
            , 'DE504C1'  # Münster
            , 'DE505C1'  # Chemnitz
            , 'DE506C1'  # Braunschweig
            , 'DE507C1'  # Aachen
            , 'DE508C1'  # Krefeld
            , 'DE509C1'  # Oberhausen
            , 'DE510C1'  # Lübeck
            , 'DE511C1'  # Hagen
            , 'DE513C1'  # Kassel
            , 'DE514C1'  # Hamm
            , 'DE515C1'  # Herne
            , 'DE516C1'  # Solingen
            , 'DE517C1'  # Osnabrück
            , 'DE518C1'  # Ludwigshafen am Rhein
            , 'DE519C1'  # Leverkusen
            , 'DE520C1'  # Oldenburg (Oldenburg)
            , 'DE521C1'  # Neuss
            , 'DE522C1'  # Heidelberg
            , 'DE523C1'  # Paderborn
            , 'DE524C1'  # Würzburg
            , 'DE525C1'  # Recklinghausen
            , 'DE526C1'  # Wolfsburg
            , 'DE527C1'  # Bremerhaven
            , 'DE528C1'  # Bottrop
            , 'DE529C1'  # Heilbronn
            , 'DE530C1'  # Remscheid
            , 'DE531C1'  # Offenbach am Main
            , 'DE532C1'  # Ulm
            , 'DE533C1'  # Pforzheim
            , 'DE534C1'  # Ingolstadt
            , 'DE535C1'  # Gera
            , 'DE536C1'  # Salzgitter
            , 'DE537C1'  # Reutlingen
            , 'DE538C1'  # Fürth
            , 'DE539C1'  # Cottbus
            , 'DE540C1'  # Siegen
            , 'DE541C1'  # Bergisch Gladbach
            , 'DE542C1'  # Hildesheim
            , 'DE543C1'  # Witten
            , 'DE544C1'  # Zwickau
            , 'DE545C1'  # Erlangen
            , 'DE546C1'  # Wuppertal
            , 'DE547C1'  # Jena
            , 'DE548C1'  # Düren, Stadt
            , 'DE549C1'  # Bocholt, Stadt
        ]

        # Create parameter list of cities for API query
        self.city_code_list = ''.join(f'&cities={city}' for city in self.german_cities)

        # Define years of interest
        self.years_of_interest = [2016, 2017, 2018, 2019]

        # Create parameter list of years for API query
        self.time_code_list = ''.join(f'&time={year}' for year in self.years_of_interest)

        # Define precision level
        self.precision_level = '1'

        # Init variables to be used in child classes
        self.api_query = None
        self.api_query_result = None
        self.api_response_status = None
        self.dataset = None

    # Define api query
    def define_api_query(self):

        self.api_query = self.url_constant_beginning + \
                          self.dataset + '?' + \
                          self.time_code_list + \
                          self.city_code_list + \
                          self.precision_level

    # define function for API call to be used in subclasses
    def call_api(self):
        try:
            # read from json-stat
            jstat_response = pyjstat.Dataset.read(self.api_query)
            self.api_query_result = jstat_response.write('dataframe')

        except Exception as ex:
            response = requests.get(self.api_query)
            self.api_query_result = response.status_code
            self.api_response_status = response.status_code
            print('Query completed with status code <> 200')

    def transform_data(self):

        # Transform data to a tidy format where city and time(=year) are the keys and stats are columns
        try:
            self.api_query_result = self.api_query_result[self.api_query_result['cities']
                .isin(openstreetmap.top20_cities.keys())]
            self.api_query_result = pd.pivot_table(self.api_query_result, index=['cities', 'time'],
                                                   columns=['indic_ur'], values=['value']).reset_index()
            col_list = list(self.api_query_result.columns.get_level_values(1))
            col_list[0:2] = ['cities', 'time']
            self.api_query_result.columns = col_list

        except:
            print('Data transformation failed')

class Population_by_age_groups_and_sex(Germany):
    """
    https://ec.europa.eu/eurostat/web/cities/data/database
    """

    def __init__(self):
        super().__init__()
        self.dataset = 'urb_cpop1'

        self.define_api_query()
        self.call_api()
        self.transform_data()


class Population_structure(Germany):
    """
    https://ec.europa.eu/eurostat/web/cities/data/database
    """

    def __init__(self):
        super().__init__()
        self.dataset = 'urb_cpopstr'

        # Define query
        self.define_api_query()

        # Execute query
        self.call_api()

        # Transform data
        self.transform_data()


class Population_by_citizenship(Germany):
    """
    https://ec.europa.eu/eurostat/web/cities/data/database
    """

    def __init__(self):
        super().__init__()
        self.dataset = 'urb_cpopcb'

        # Define query
        self.define_api_query()

        # Execute query
        self.call_api()

        # Transform data
        self.transform_data()


class Fertility_and_mortality(Germany):
    """
    https://ec.europa.eu/eurostat/web/cities/data/database

    THE DATA IS NOT USED IN THE ANALYSIS AS THERE ARE NO STATS IN 2016-2019!!!
    """

    def __init__(self):
        super().__init__()
        self.dataset = 'urb_cfermor'

        # Define query
        self.define_api_query()

        # Execute query
        self.call_api()

        # Transform data
        self.transform_data()


class Living_conditions(Germany):
    """
    https://ec.europa.eu/eurostat/web/cities/data/database
    """

    def __init__(self):
        super().__init__()
        self.dataset = 'urb_clivcon'

        # Define query
        self.define_api_query()

        # Execute query
        self.call_api()

        # Transform data
        self.transform_data()


class Education(Germany):
    """
    https://ec.europa.eu/eurostat/web/cities/data/database
    """

    def __init__(self):
        super().__init__()
        self.dataset = 'urb_ceduc'

        # Define query
        self.define_api_query()

        # Execute query
        self.call_api()

        # Transform data
        self.transform_data()


class Culture_and_tourism(Germany):
    """
    https://ec.europa.eu/eurostat/web/cities/data/database
    """

    def __init__(self):
        super().__init__()
        self.dataset = 'urb_ctour'

        # Define query
        self.define_api_query()

        # Execute query
        self.call_api()

        # Transform data
        self.transform_data()


class Labour_market(Germany):
    """
    https://ec.europa.eu/eurostat/web/cities/data/database
    """

    def __init__(self):
        super().__init__()
        self.dataset = 'urb_clma'

        # Define query
        self.define_api_query()

        # Execute query
        self.call_api()

        # Transform data
        self.transform_data()


class Transport(Germany):
    """
    https://ec.europa.eu/eurostat/web/cities/data/database
    """

    def __init__(self):
        super().__init__()
        self.dataset = 'urb_ctran'

        # Define query
        self.define_api_query()

        # Execute query
        self.call_api()

        # Transform data
        self.transform_data()


class Environment(Germany):
    """
    https://ec.europa.eu/eurostat/web/cities/data/database
    """

    def __init__(self):
        super().__init__()
        self.dataset = 'urb_cenv'

        # Define query
        self.define_api_query()

        # Execute query
        self.call_api()

        # Transform data
        self.transform_data()
