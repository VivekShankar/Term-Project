from googleplaces import GooglePlaces, types, lang
import pygeocoder

def findNearbyAttractions(r, loc):
    #takes in radius (miles), loc (an address)
    mapCityToLatLong = dict()
    YOUR_API_KEY = 'AIzaSyBrDq_8ZKnBgqKW9x30gw5PgaggyM_Ta2M'
    r *= 1609.34 #convert input radius in miles to meters (to work with API)
    google_places = GooglePlaces(YOUR_API_KEY)
    query_result = google_places.nearby_search(
            location=loc,
            radius=r, types=[types.TYPE_GAS_STATION])
    for place in query_result.places:
        place.get_details()
        print place.details()
        mapCityToLatLong[place.name]=(place.geo_location['lat'],place.geo_location['lng'])
        #print place.geo_location
    return mapCityToLatLong

#cityMap = findNearbyAttractions(1, '163 Cherry Dr., Troy, MI')
#print cityMap

##def convertLatLongToAddresses(latLong):
##    #takes in lat, long tuple, returns address
##    fp=open('test.txt','a')
##    geoCoder = pygeocoder.Geocoder()
##    print >> fp, geoCoder.reverse_geocode(latLong[0],latLong[1])
##    # >> for append
##    fp.close()
##
##convertLatLongToAddresses(cityMap['Marathon Gas'])
##
##def readFile(filename, mode="rt"):
##    # rt = "read text"
##    with open(filename, mode) as fin:
##        return fin.read()
##
##def writeFile(filename, contents, mode="wt"):
##    # wt = "write text"
##    with open(filename, mode) as fout:
##        fout.write(contents)
##        
##contents = readFile('test.txt')
##newLineIndex = contents[::-1].index('\n')
##print contents[newLineIndex:]
##
##writeFile('test.txt', '')

from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = 'AIzaSyBrDq_8ZKnBgqKW9x30gw5PgaggyM_Ta2M'

google_places = GooglePlaces(YOUR_API_KEY)

# You may prefer to use the text_search API, instead.
query_result = google_places.nearby_search(
        location='163 Cherry Dr., Troy, MI',
        radius=1609.34, types=[types.TYPE_GAS_STATION])

if query_result.has_attributions:
    print query_result.html_attributions


for place in query_result.places:
    # Returned places from a query are place summaries.
    print place.name
    print place.geo_location
    print place.reference

    # The following method has to make a further API call.
    place.get_details()
    # Referencing any of the attributes below, prior to making a call to
    # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    print place.details['vicinity'] #address # A dict matching the JSON response from Google.
##    print place.local_phone_number
##    print place.international_phone_number
##    print place.website
##    print place.url
