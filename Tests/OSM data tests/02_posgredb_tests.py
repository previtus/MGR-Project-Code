#!/usr/bin/python

from secrets import hostname,username,password,database

# Simple routine to run a query on a database and print the results:
def doQuery( conn, command ) :
    cursor = conn.cursor()

    cursor.execute( command )

    rows = cursor.fetchall()

    colnames = [desc[0] for desc in cursor.description]
    print colnames

    for row in rows:
        print "   ", row


print "Using psycopg2"
import psycopg2
try:
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
except:
    print "I am unable to connect to the database"

command = "SELECT building, highway, leisure, amenity, shop, barrier, railway, tourism, public_transport, bicycle, foot, historic, religion FROM planet_osm_line WHERE building IS NOT NULL LIMIT 13"
doQuery( myConnection, command )
myConnection.close()

'''
print "Using PyGreSQL"
import pgdb
myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
#doQuery( myConnection )
myConnection.close()
'''