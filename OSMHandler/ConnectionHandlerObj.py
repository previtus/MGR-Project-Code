# Manages the connection with our OSM data resource, the PosgreSQL database
# also has the individual queries.

print "imported ConnectionHandlerObj.py, inside DB requiring section."


import csv
import psycopg2
from OSMHandler.ConnectionSettingsSecrets import hostname,username,password,database


class ConnectionHandler:
    '''
    Connection Handler

    What does ConnectionHandler have?

     - link to the database, set in initialization

    What can it do?

     - initialize connection to DB, prepare lists of columns we want to pay attention too
     - query for a location

    '''

    __connection = []
    __distinct_keys = []
    __list_of_watched_pairs = []
    __indices_dict = []
    # inverted indices with location of watcher key=attr pair in the final vector
    # ex: final_vector[ indices_dict[pair] ] = 4
    # indices_dict['highway=bus_stop'] = 39, so in final_vector[39] we indicate that there are 4 bus stops nearby


    foo = -1

    def __init__(self):
        key_attr_pairs_file = 'key-attr-pairs.csv'
        number_of_loaded_pairs = 50 # out of 1103 rows

        self.__connection = self.setup_db_connection(hostname,username, password, database)
        [self.__distinct_keys, self.__list_of_watched_pairs, self.__indices_dict] = self.load_key_attr_pairs(key_attr_pairs_file,
                                                                                   limit_number=number_of_loaded_pairs)
        print self.__distinct_keys
        print self.__list_of_watched_pairs
        print self.__indices_dict

        return None

    def setup_db_connection(self, hostname, username, password, database):
        '''
        Establish connection
        '''
        connection = None
        try:
            connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
            print "Connected to DB."
        except:
            print "I am was to connect to host "+ hostname +" and database " + database + " with username " + username
        return connection

    def load_key_attr_pairs(self, csv_name, limit_number = -1 ):
        '''
        Builds the lists of interesting key-attribute pairs.
         distinct_keys contains just the names of keys
            ex: ['building', 'bridge', 'amenity', ...]
            We will load these columns out of the database.

         list_of_watched_pairs contains
            ex: ['building=yes', 'highway=residential', 'building=house', ...]
            We will count these occurances in the resulting neighborhood.

        In list_of_watched_pairs we can find only combinations of key=attribute which have keys from distinct_keys!

        :param csv_name: Name of tha file containing most common pairs of key-attribute combinations
        :param limit_number: Number of rows we would like to look at
        :return: lists of distinct keys and key=attribute pairs we will pay attention to in sql query results
        '''

        keys = []
        attributes = []
        counts = []

        list_of_watched_pairs = []
        indices_dict = {}

        with open(csv_name, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            i = 0
            for row in reader:
                if i>=limit_number and limit_number<>-1:
                    break

                key = row[0]
                attr = row[1]
                count = row[2]

                key_attr_pair = "=".join([key, attr])

                list_of_watched_pairs.append( key_attr_pair )
                indices_dict[key_attr_pair] = i # inverted indices to the pairs

                keys.append(key)
                attributes.append(attr)
                counts.append(count)
                i += 1

        distinct_keys = set(keys)

        return [distinct_keys, list_of_watched_pairs, indices_dict]
