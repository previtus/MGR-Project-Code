import csv
import psycopg2
from secrets import hostname,username,password,database

def load_key_attr_pairs( csv_name, limit_number = -1 ):

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


def build_sql_command(distinct_keys, sql_limit_rows=-1):
    # SELECT <> FROM planet_osm_line

    list = ["SELECT \""]
    list.append('\", \"'.join(distinct_keys))
    list.append("\" FROM planet_osm_line")
    if sql_limit_rows<>-1:
        list.append(" LIMIT ")
        list.append(str(sql_limit_rows))

    command = ''.join(list)
    return command

# DATABASE STUFF
def setup_db_connection(hostname,username, password, database):
    try:
        connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    except:
        print "I am unable to connect to the database"
    return connection

def process_query_into_key_attr_pairs( conn, command ) :
    cursor = conn.cursor()

    cursor.execute( command )

    rows = cursor.fetchall()

    colnames = [desc[0] for desc in cursor.description]
    #print colnames
    key_attr_pairs = []

    for row in rows:

        value_index = 0
        for value in row:
            key = colnames[value_index]
            attr = ""
            if value is not None:
                attr = value

            key_attr_pair = "=".join([key,attr])
            key_attr_pairs.append(key_attr_pair)

            value_index += 1
    return key_attr_pairs

[distinct_keys, list_of_watched_pairs, indices_dict] = load_key_attr_pairs('key-attr-pairs.csv', limit_number = 50)
print distinct_keys

connection = setup_db_connection(hostname,username,password,database)

sql_command = build_sql_command(distinct_keys, sql_limit_rows=-1)
print sql_command

key_attr_pairs = process_query_into_key_attr_pairs( connection, sql_command )
connection.close()

final_vector = [0] * len(list_of_watched_pairs)

for pair in key_attr_pairs:
    # pair can be 'building=yes' but also 'building='
    if pair in indices_dict:
        ind = indices_dict[pair]
        final_vector[ind] += 1

# debug report:
print "We ended up with these not-null:"
i = 0
sorted_final_vec = []
for value in final_vector:
    ind = list_of_watched_pairs[i]

    if (value > 0):
        print ind, " *= ", value
    i += 1

    sorted_final_vec.append([ind, value])

sorted_final_vec.sort(key=lambda x: -x[1])
print sorted_final_vec

#print final_vector

#print key_attr_pairs

#print list_of_watched_pairs
#print indices_dict

# What is on index <i>?
#print list_of_watched_pairs[0]