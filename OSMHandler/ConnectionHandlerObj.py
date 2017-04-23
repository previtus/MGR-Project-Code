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
        [self.__distinct_keys, self.__list_of_watched_pairs, self.__indices_dict] = self.load_key_attr_pairs(key_attr_pairs_file,
                                                                                   limit_number=number_of_loaded_pairs)

        #print len(self.__distinct_keys), self.__distinct_keys
        #print len(self.__list_of_watched_pairs), self.__list_of_watched_pairs
        #print len(self.__indices_dict), self.__indices_dict

        return None

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

    def check_column_names(self, columns_we_want_to_call):
        '''
        Tries to look into the database and checks all its available column values. From the list of columns we would
        like to know about subtracts the ones we cannot call (doing an intersection between columns_we_want_to_call
        and the columns we actually have in the db).

        :param columns_we_want_to_call: Column names of the ones we would like to know
        :return: Column names of those which we actually can call (so it's subset of columns_we_want_to_call)
        '''
        columns_we_want_to_call = self.__distinct_keys

        table_name = 'planet_osm_line'
        command = 'SELECT * FROM ' + table_name + " LIMIT 1"
        [_, columns_we_have] = self.run_command(command)

        #print len(columns_we_have), columns_we_have

        columns_we_dont_have = set(columns_we_want_to_call) - set(columns_we_have)
        columns_we_will_call = set(columns_we_have) & set(columns_we_want_to_call)

        #print len(columns_we_dont_have), columns_we_dont_have
        #print len(columns_we_will_call), columns_we_will_call

        return list(columns_we_will_call)

    def extract_all_pairs(self, rows, colnames):
        key_attr_pairs = []

        for row in rows:

            value_index = 0
            for value in row:
                key = colnames[value_index]
                attr = ""
                if value is not None:
                    attr = value

                key_attr_pair = "=".join([key, attr])
                key_attr_pairs.append(key_attr_pair)

                value_index += 1
        return key_attr_pairs

    def query_location(self, location):
        # run query to get neighborhood
        filtered_column_names = self.check_column_names(self.__distinct_keys)

        sql_command = self.build_sql_command_REWRITE(column_names = filtered_column_names, location=location)
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
        sorted_final_vec = []
        for value in nearby_vector:
            ind = self.__list_of_watched_pairs[i]

            #if (value > 0):
            #    print ind, " *= ", value
            i += 1

            sorted_final_vec.append([ind, value])

        sorted_final_vec.sort(key=lambda x: -x[1])

        #for itm in sorted_final_vec:
        #    print itm[0], itm[1]
        #    if int(itm[1]) == 0:
        #        print "The rest is just zero values!"
        #        break

        #print sorted_final_vec
        return []

    def build_sql_command_REWRITE(self, column_names, table_name = 'planet_osm_line',sql_limit_rows=-1, location=[]):
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