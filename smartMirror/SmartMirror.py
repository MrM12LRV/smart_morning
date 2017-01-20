from tkinter import *
import time
import datetime

#Will need downloading
from lxml import html           # `python3 -m pip install lxml`
import json
import requests                 # `python3 -m pip install requests`
from requests import get

from speech_recognition import Microphone, Recognizer, AudioData
from PIL import Image, ImageTk  # `python3 -m pip install pillow`
from os.path import join
from pprint import PrettyPrinter

from instagram.client import InstagramAPI
import httplib2
import sys

BASE_PATH = "images"

class SpeechFunctioner():

    def __init__(self):
        self.prettyprinter = PrettyPrinter(indent=4)

        self.HIGH = 4000
        self.LOW = 1000
        self.SENSITIVITY = self.HIGH
        self.response_json = None
        self.voice_function = None


    def __async_listener_fn(self, recognizer_instance, audio_data):

        print("Performing Sphinx Speech to Text asynchronously")
        try:
            text_from_audio = \
                recognizer_instance.recognize_sphinx( \
                    audio_data, show_all = False)
        except Exception as e:
            print(
                "Exception in recognizer: " + str(e))
            text_from_audio = None

        print("Text recognized:\n\t", end="")
        print(text_from_audio)
        print("Sending HTTP request to API AI")
        self.response_json = \
            get('https://api.api.ai/v1/query?v=20150910&query=%s&lang=en&sessionId=1234567890' % text_from_audio,
                headers={
                    'language-tag'  : 'en',
                    'Authorization' : 'Bearer e4099166fd7a41218ba851d21e6866f5',
                    'Content-Type'  : 'application/json; charset=utf-8'
                }
            )

        print("Got structure back:")
        try: self.prettyprinter.pprint(self.response_json.json())
        except: print("Could not print JSON result.")

        try:
            self.voice_function = eval(self.response_json.json()['result']['metadata']['intentName'])
        except Exception as err:
            print("Not a valid voice function", self.voice_function)
            print("Exception: {0}".format(err))
            voice_function = None

        return text_from_audio

    # developer:    cac03a5b9aca49e2b63e97f7c0ae0cec    (managing entities and intents)
    # client:       e4099166fd7a41218ba851d21e6866f5    (making queries)
    # Authorization: Bearer YOUR_ACCESS_TOKEN

    def async_read_microphone(self):
        recognizer_instance = Recognizer()
        recognizer_instance.energy_threshold = self.SENSITIVITY
        recognizer_instance.phrase_time_limit = 20 # TODO: I don't think this variable is working
                                                   #       find out how to change phrase time limit.
                                                   #       Do we want this phrase time_limit?
        audio_source = Microphone()
        print("Spawning reader")
        stop_listener_fn = \
            recognizer_instance.listen_in_background( \
                audio_source, self.__async_listener_fn)

        print("Leaving read microphone")
        """print("Waiting to read for 10 seconds")
        from time import sleep
        sleep(100)                  # TODO: when do we stop lisening?
        stop_listener_fn()          #       Probably never; Maybe when we
                                    #       just quit out of app?
        print("No longer taking audio input")
        
        return
        """


    def sync_read_microphone(self, duration = 5):
        with Microphone() as audio_source:
            recognizer_instance = Recognizer()
            recognizer_instance.energy_threshold = self.SENSITIVITY

            print("Reading")
            audio_data = \
                recognizer_instance.record( \
                    audio_source, duration = duration)

            print("Performing Sphinx Speech to Text")
            try:
                text_from_audio = \
                    recognizer_instance.recognize_sphinx( \
                        audio_data, show_all = False)
            except Exception as e:
                print(
                    "Exception in recognizer: " + str(e))
                text_from_audio = None

            print(text_from_audio)
            print("Sending HTTP request to API AI")

            self.response_json = \
                get('https://api.api.ai/v1/query?v=20150910&query=%s&lang=en&sessionId=1234567890' % text_from_audio,
                    headers={
                        'language-tag'  : 'en',
                        'Authorization' : 'Bearer e4099166fd7a41218ba851d21e6866f5',
                        'Content-Type'  : 'application/json; charset=utf-8'
                    }
                )
            print("Got structure back:")
            try: self.prettyprinter.pprint(self.response_json.json())
            except: print("Could not print JSON result.")

            try:
                self.voice_function = \
                    eval(self.response_json.json()['result']['metadata']['intentName'])
            except Exception as err:
                print("Not a valid voice function", self.voice_function)
                print("Exception: {0}".format(err))
                self.voice_function = None
        return None

##### Write functions for voice commands

def Appearance():
    return "What is up yo?"


#####
"""
def showInsta():
    access_token = "305057786.eca884d.4e28837ad0f34ffa97b323b40ab41eba"
    client_secret = "e425943412cd4a55b74d0671c896e123"
    user_id = "305057786"
    client_id = "eca884df1cad4666a82432e314de7737"


    api = InstagramAPI(access_token=access_token)

    photoURL = []
    like_count_array = []
    final_array = []

    recent_media, next = api.user_recent_media(user_id=user_id, count=10)
    for media in recent_media:
        try:
            newURL =  media.images['standard_resolution'].url
            photoURL.append(newURL)

            new_count = media.like_count
            like_count_array.append(new_count)
        except:
            continue

    final_array = zip(photoURL,like_count_array)
    return final_array

#def drawInstaScreen(final_array):

"""
#####
def cleanTime(time): #destructively removes leading 0 in 12 hr time
    if time[0] == "0": time = time[1:]
    return time

class Text(object):
    def __init__(self, x, y, text, fontSize, color = "white", anc = 'center'):
        self.font = "Times " + str(fontSize)
        self.x, self.y, self.text, self.color, self.anc = x, y, str(text), color, anc

    def drawText(self, canvas):
        canvas.create_text(self.x, self.y, text = self.text, font = self.font, fill = self.color, anchor = self.anc)

class Weather(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.update()
         
    def update(self):
        self.weather = self.getWeather()
        self.extract(self.weather)

    def getLatLon(self):
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = 40.4434660 #j['latitude']
        lon = -79.9434570 #j['longitude']
        return lat, lon

    def getWeather(self):
        lat, lon = 40.4435, -79.9435 #self.getLatLon() 
        apiKey = '5740d2c30126407518998689a40335ad'
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s&units=imperial' % (lat, lon, apiKey))
        return(r.json())

    def extract(self, weather):
        self.temp = int(round(weather['main']['temp']))
        self.humidity = weather['main']['humidity']
        self.cityName = weather['name']
        self.country = weather['sys']['country']
        self.sunrise24 = cleanTime(datetime.datetime.fromtimestamp(int(weather['sys']['sunrise'])).strftime('%H:%M'))
        self.sunset24 = cleanTime(datetime.datetime.fromtimestamp(int(weather['sys']['sunset'])).strftime('%H:%M'))
        self.sunset = cleanTime(datetime.datetime.fromtimestamp(int(weather['sys']['sunset'])).strftime('%I:%M %p'))
        self.cloudCover = weather['clouds']['all']
        self.windSpeed = weather['wind']['speed']
        self.visibility = weather['visibility']
        self.descript = weather['weather'][0]['description'].title()
        self.id = weather['weather'][0]['id']

    def isDayTime(self, time, sunrise, sunset):
        sunriseH = int(sunrise.split(":")[0])
        sunriseM = int(sunrise.split(":")[1][:2])
        sunriseTotal = sunriseH * 60 + sunriseM

        timeH = int(time.split(":")[0])
        timeM = int(time.split(":")[1][:2])
        timeTotal = timeH * 60 + timeM

        sunsetH = int(sunset.split(":")[0])
        sunsetM = int(sunset.split(":")[1][:2])
        sunsetTotal = int(sunsetH * 60 + sunsetM)
        return sunriseTotal <= timeTotal <=  sunsetTotal

    def draw(self, canvas):
        line1 = Text(self.x, self.y - 50, str(self.temp) + chr(176), 36, anc = 'w')
        line2 = Text(self.x, self.y - 15, self.descript, 22, anc = 'w')
        line3 = Text(self.x, self.y + 15, "Cloud Cover: " + str(self.cloudCover) + "%", 22, anc = 'w')
        line4 = Text(self.x, self.y + 45, "Sundown " + self.sunset, 22, anc = 'w')
        line1.drawText(canvas)
        line2.drawText(canvas)
        line3.drawText(canvas)
        line4.drawText(canvas)
        if self.isDayTime(cleanTime(time.strftime("%H:%M")), self.sunrise24, self.sunset24):
            img = self.photo
        else:
            img = self.moon
        canvas.create_image(self.x + 50, self.y - 135, image = img)

class news(object):
    def __init__(self, x, y):
        response = requests.get('https://news.google.com/news/section?cf=all&pz=1&topic=b&siidp=b458d5455b7379bd8193a061024cd11baa97&ict=ln')
        if (response.status_code == 200):
            pagehtml = html.fromstring(response.text)
            news = pagehtml.xpath('//h2[@class="esc-lead-article-title"] \
                          /a/span[@class="titletext"]/text()')
        self.news = news
        self.numArticles = len(news)
        self.article = 0
        self.x, self.y = x, y

    def getArticle(self):
        return self.news[int(self.article)%self.numArticles]

    def draw(self, canvas):
        headline = Text(self.x, self.y, self.getArticle(), 16)
        headline.drawText(canvas)

class TimeDate(object):
    def __init__(self, x, y):
        self.time = Text(x, y - 20, "", 45)
        self.date = Text(x, y + 20, "", 30)
        self.update()

    def update(self):
        self.time.text = cleanTime(time.strftime("%I:%M %p"))
        self.date.text = time.strftime("%A, %B %d")

    def draw(self, canvas):
        self.time.drawText(canvas)
        self.date.drawText(canvas)
     
class Location(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.address = self.getAddress()

    def getAddress(self):
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat, lon = 40.4435, -79.9435 #j['latitude'], j['longitude']
        r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=AIzaSyBzGpoNZw9IE0enxByNgMA5NSat1xB_Ohw" % (lat, lon))
        address = r.json()['results'][0]['formatted_address']
        return self.buildAddress(address)

    def buildAddress(self, address):
        result = address.split(',')[1:]
        result[1] = result[1][:3]
        result = ','.join(result).lstrip()
        return result

    def draw(self, canvas):
        line1 = Text(self.x, self.y, self.address, 30)
        line1.drawText(canvas)

class SmartMirror(object):
    def __init__(self):
        self.bgColor = "black"
    
    def timerFired(self):

        print("Voice function is", self.sf.voice_function)
        if self.sf.voice_function is not None and callable(self.sf.voice_function):
            self.sf.voice_function()

        self.timeDate.update()
        self.news.article += 0.04

    def keyPressed(self, event, root):
        e = event.keysym
        if e == 'q': root.destroy()
        
    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill = self.bgColor)
        self.timeDate.draw(canvas)
        self.weather.draw(canvas)
        self.location.draw(canvas)
        self.news.draw(canvas)

    def getKey(self, weatherId):
        if weatherId == 800: key = 1
        elif weatherId == 801: key = 4
        else: key = weatherId//100
        return key

    def run(self):
        def redrawAllWrapper(canvas, self):
            canvas.delete(ALL)
            self.redrawAll(canvas)
            canvas.update()    

        def keyPressedWrapper(event, canvas, self, root):
            self.keyPressed(event, root)
            redrawAllWrapper(canvas, self)

        def timerFiredWrapper(canvas, self):
            self.timerFired()
            redrawAllWrapper(canvas, self)
            canvas.after(self.timerDelay, timerFiredWrapper, canvas, self)
        
        root = Tk()
        self.width, self.height = root.winfo_screenwidth(), root.winfo_screenheight()

        self.timeDate = TimeDate(self.width/2, 100)
        self.weather = Weather(100, 250)
        self.location = Location(self.width/2, self.height - 120)
        self.news = news(self.width/2, self.height - 175)
        
        key = self.getKey(self.weather.id)
        d = {1: "Sunny.jpg", 2: "Thunderstorm.jpg", 3: "Rain.jpg", 4: "Partly Cloudy.jpg", 5: "Rain.jpg", 6: "Snow.jpg", 7: "Other.jpg", 8: "Clouds.jpg", 9: "Other.jpg"}
        self.weather.photo = ImageTk.PhotoImage(Image.open(join(BASE_PATH, d[key])))
        self.weather.moon = ImageTk.PhotoImage(Image.open(join(BASE_PATH, "Moon.jpg")))

        root.wm_title("SmartMirror")
        root.geometry(str(self.width) + "x" + str(self.height))
        self.timerDelay = 200 # milliseconds
        canvas = Canvas(root, width = self.width, height=self.height)
        canvas.pack()


        # Initialize and start speech to functioner:
        self.sf = SpeechFunctioner()
        self.sf.async_read_microphone();


        root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas, self, root))

        timerFiredWrapper(canvas, self)
        root.mainloop()
        print("bye!")
        
SmartMirror().run()
