# Checks (Check()) if loaded Segments file is properly marked with the data of nearby locations to the data,
# according to our last and active formula (OSM_MARKING_VERSION).
# By default doesn't need or even import the other parts, which require access to PostgreSQL db.
#
# Can Ensure() the validity of Segments - aka it checks and if we are not up to date, then we will use Marker
# this section will import some of the parts requiring running db.

def Check(Segments):
    if len(Segments) == 0:
        print "Size of Segments is 0!"
        return False
    else:
        return Segments[0].checkOSMVersion()

