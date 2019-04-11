import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyD3kp9wN8dFRqTf6YVYFiha-lJ9DuUIAOA')

# Geocoding an address

# Look up an address with reverse geocoding

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.distance_matrix({'lat': 37.348739,
                                           'lng': -121.865082},
                                          [{'lat': 37.348739,
                                           'lng': -121.865082},
                                           {'lat': 36.975142,
                                           'lng': -122.018630}],
                                          units='imperial', mode='driving')
print(directions_result['rows'][0]['elements'])


