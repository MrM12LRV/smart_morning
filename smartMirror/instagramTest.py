from instagram.client import InstagramAPI
import httplib2
import json
import sys

access_token = "305057786.eca884d.4e28837ad0f34ffa97b323b40ab41eba"
client_secret = "e425943412cd4a55b74d0671c896e123"
user_id = "305057786"
client_id = "eca884df1cad4666a82432e314de7737"


api = InstagramAPI(access_token=access_token)

photoURL = []
recent_media, next = api.user_recent_media(user_id=user_id, count=10)
for media in recent_media:
	try:
		newURL =  media.images['standard_resolution'].url
		photoURL.append(newURL)
		
	except:
		continue
