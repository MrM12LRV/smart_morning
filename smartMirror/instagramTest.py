from instagram.client import InstagramAPI
import httplib2
import json
import sys
import urllib
import os


from StringIO import StringIO

access_token = "305057786.eca884d.4e28837ad0f34ffa97b323b40ab41eba"
client_secret = "e425943412cd4a55b74d0671c896e123"
user_id = "305057786"
client_id = "eca884df1cad4666a82432e314de7737"


api = InstagramAPI(access_token=access_token)

photoURL = []
like_count_array = []

final_array = []

num = 0
recent_media, next = api.user_recent_media(user_id=user_id, count=10)
for media in recent_media:
	try:
		newURL =  media.images['standard_resolution'].url
		photoURL.append(newURL)

		new_count = media.like_count
		like_count_array.append(new_count)


	except:

		continue
	filename = "test" + str(num) + ".gif"
	halffilename = os.path.join('C:\Users\Shreya\Documents\GitHub\smart_morning\smartMirror\images',filename)
	urllib.urlretrieve(newURL, halffilename)
	num +=1


final_array = zip(photoURL,like_count_array)

tagName = "carnegie mellon"

recent_media = api.tag_recent_media(tag_name = tagName)
for media in recent_media:
	try:
		newURL =  media.images['standard_resolution'].url
		photoURL.append(newURL)

		print photoURL


	except:

		continue


