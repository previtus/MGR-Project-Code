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
    opened = False

    foo = -1

    def __init__(self):
        key_attr_pairs_file = 'key-attr-pairs.csv'
        number_of_loaded_pairs = 1103 # out of 1103 rows

        self.__connection = self.setup_db_connection(hostname,username, password, database)
        columns_we_have_in_database = self.get_column_names_in_db()
        #print columns_we_have_in_database

        [self.__distinct_keys, self.__list_of_watched_pairs, self.__indices_dict] = self.load_key_attr_pairs(
            key_attr_pairs_file, limit_number=number_of_loaded_pairs,
            dont_take_keys_which_are_not_in_list = columns_we_have_in_database )

        return None

    def final_vec_invert_indices(self, i):
        return self.__list_of_watched_pairs[i]

    def setup_db_connection(self, hostname, username, password, database):
        '''
        Establish connection
        '''
        connection = None
        try:
            connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
            print "Connected to DB."
            self.opened = True

        except:
            print "I am was to connect to host "+ hostname +" and database " + database + " with username " + username
        return connection

    def close_connection(self):
        self.__connection.close()
        self.opened = False

    def load_key_attr_pairs(self, csv_name, dont_take_keys_which_are_not_in_list, limit_number = -1):
        '''
        Builds the lists of interesting key-attribute pairs.
         distinct_keys contains just the names of keys
            ex: ['building', 'bridge', 'amenity', ...]
            We will load these columns out of the database.

         list_of_watched_pairs contains
            ex: ['building=yes', 'highway=residential', 'building=house', ...]
            We will count these occurances in the resulting neighborhood.

        In list_of_watched_pairs we can find only combinations of key=attribute which have keys from distinct_keys!

        In dont_take_keys_which_are_not_in_list we have column names of our available database, those show us, which
        keys we actually have about the data - so for any key not in there, we don't have to make space in the final
        vector (as it would always be 0, for all the data).

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

                if key in dont_take_keys_which_are_not_in_list:

                    key_attr_pair = "=".join([key, attr])

                    list_of_watched_pairs.append( key_attr_pair )
                    indices_dict[key_attr_pair] = i # inverted indices to the pairs

                    keys.append(key)
                    attributes.append(attr)
                    counts.append(count)
                    i += 1

        distinct_keys = set(keys)

        return [distinct_keys, list_of_watched_pairs, indices_dict]

    def run_command(self, command):
        '''
        Runs command and returns the rows and column names
        :param command: sql command
        :return:
        '''
        cursor = self.__connection.cursor()
        cursor.execute(command)
        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        return [rows, colnames]

    def get_column_names_in_db(self):
        table_name = 'planet_osm_line'
        command = 'SELECT * FROM ' + table_name + " LIMIT 1"
        [_, columns_we_have] = self.run_command(command)
        return columns_we_have

    def extract_all_pairs(self, rows, colnames, excluded_column='dist_meters'):
        key_attr_pairs = []

        for row in rows:

            value_index = 0
            for value in row:
                key = colnames[value_index]
                attr = ""
                if value is not None:
                    attr = value

                #print key, attr

                # temporary solution - we exclude the 'dist_meters' column
                if (key != excluded_column):
                    key_attr_pair = "=".join([key, attr])
                    key_attr_pairs.append(key_attr_pair)

                value_index += 1
        return key_attr_pairs

    def query_location(self, location, radius, table_name):
        # run query to get neighborhood
        #sql_command = self.sql_cmd_everywhere(column_names = self.__distinct_keys)
        sql_command = self.sql_cmd_radius(column_names = self.__distinct_keys, location=location, radius=radius, table_name=table_name)
        #print sql_command

        [rows, colnames] = self.run_command(sql_command)

        all_pairs = self.extract_all_pairs(rows, colnames)

        # count the occurrences
        nearby_vector = [0] * len(self.__list_of_watched_pairs)

        for pair in all_pairs:
            # pair can be 'building=yes' but also 'building='
            if pair in self.__indices_dict:
                ind = self.__indices_dict[pair]
                nearby_vector[ind] += 1

        # debug report:
        # print "We ended up with these not-null:"
        i = 0
        final_vec_dict = {}
        sorted_final_vec = []
        for value in nearby_vector:
            ind = self.__list_of_watched_pairs[i]

            #if (value > 0):
            #    print ind, " *= ", value
            i += 1

            sorted_final_vec.append([ind, value])
            final_vec_dict[ind] = value

        sorted_final_vec.sort(key=lambda x: -x[1])

        #for itm in sorted_final_vec:
        #    print itm[0], itm[1]
        #    if int(itm[1]) == 0:
        #        print "The rest is just zero values!"
        #        break
        #print sorted_final_vec

        # final neighborhood vector is in nearby_vector
        # and final neighborhood dictionary in final_vec_dict
        #print nearby_vector
        #print final_vec_dict

        # i-th value in nearby_vector has descriptor (key=attr pair) of self.__list_of_watched_pairs[i]
        return [nearby_vector, self.__list_of_watched_pairs]

    def sql_cmd_radius(self, column_names, table_name = 'planet_osm_line',sql_limit_rows=-1, location=[], radius=10):
        # SELECT <> FROM planet_osm_line

        list = ["SELECT * FROM ( "]


        inner_select = ["SELECT ST_Distance(ST_Transform(way, 4326), ST_MakePoint(", str(location[0]),", ", str(location[1]), ")::geography) AS dist_meters, "]
        inner_select.append("\"")
        inner_select.append('\", \"'.join(column_names))
        inner_select.append("\" FROM "+table_name)

        list = list + inner_select

        list.append(") AS A WHERE A.dist_meters < ")
        list.append(str(radius))
        list.append(";")

        command = ''.join(list)

        #print ''.join(inner_select)
        print command

        return command

    def sql_cmd_everywhere(self, column_names, table_name = 'planet_osm_line',sql_limit_rows=-1):
        # SELECT <> FROM planet_osm_line

        list = ["SELECT \""]
        list.append('\", \"'.join(column_names))
        list.append("\" FROM "+table_name)
        if sql_limit_rows<>-1:
            list.append(" LIMIT ")
            list.append(str(sql_limit_rows))

        # TODO> WHERE location is nearby location
        list.append(";")

        command = ''.join(list)
        return command

    def report(self):
        if self.opened:
            print "Connection is opened to host "+ hostname +" and database " + database + " with username " + username
        else:
            print "Connection is closed."
