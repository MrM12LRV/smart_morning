from instagram.client import InstagramAPI
import httplib2
import json
import sys

access_token = "305057786.eca884d.4e28837ad0f34ffa97b323b40ab41eba"
client_secret = "e425943412cd4a55b74d0671c896e123"
user_id = "305057786"
client_id = "eca884df1cad4666a82432e314de7737"

lat_cmu = "79.9435"
long_cmu = "40.4435"
place_id_cmu = "384628"

api = InstagramAPI(access_token=access_token)

recent_location, next = api.location_recent_media(location_id = place_id_cmu)

photo_URL = []
for media in recent_location:
	
	try:
		newURL =  media.images['standard_resolution'].url
		photoURL.append(newURL)
		
	except:
		continue

print photo_URL