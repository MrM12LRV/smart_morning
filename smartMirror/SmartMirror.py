from tkinter import *
import time
import datetime

#Will need downloading
from lxml import html           # `python3 -m pip install lxml`
import json
import requests                 # `python3 -m pip install requests`
from requests import get

from speech_wrapper import SpeechFunctioner
from PIL import Image, ImageTk  # `python3 -m pip install pillow`
from os.path import join

#from instagram.client import InstagramAPI
#import httplib2
import sys

BASE_PATH = "images"

##### Write functions for voice commands

def showerWithHearts():
	# get image and display it on canvas
  	# need to display gif of salt bae
    print("IN HERE!!\n\n\n\nYOYOYOY\n\n\n")
    sm.isDrawHearts = True
    return "What is up yo?"

def InstagramToggle():
    if sm.isInstagramToggle:
        sm.isInstagramToggle = False
    else:
        sm.isInstagramToggle = True
    return


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


class InstagramDraw(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imgArray = []
        self.populateImgArray()
        self.likeArray = []
        self.populateLikeArray()

    def populateImgArray(self):
        baseSize = 160
        for i in range(10):
            name = "test" + str(i) + ".jpeg"
            img = Image.open(join(BASE_PATH, name))
            img = self.resize(name, baseSize)
            tkImg = ImageTk.PhotoImage((img))
            self.imgArray.append(tkImg)

    def populateLikeArray(self):
        newPath = join(BASE_PATH,"likes.txt")
        curFile = open(newPath, 'r')
        self.likeArray = curFile.read().split('\n')
        print("The array is", self.likeArray)
        curFile.close()

    def resize(self, name, baseSize):
        img = Image.open(join(BASE_PATH, name))
        wpercent = (baseSize/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((baseSize,hsize), Image.ANTIALIAS)
        return img

    def draw(self, canvas):
        spacing = 180
        for i in range(len(self.imgArray)):
            x, y = self.x - 84, self.y + spacing * i
            canvas.create_image(x, y, image = self.imgArray[i])
        j = 0
        for likeCount in self.likeArray:
            x, y = self.x + 115 - 84, self.y + spacing * j
            likeText = Text(x, y, likeCount, 72)
            likeText.drawText(canvas)
            j += 1



class News(object):
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
        try:
            address = r.json()['results'][0]['formatted_address']
        except:
            address = "Address Error, 123, 456"
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
        self.isDrawHearts = False
        self.isInstagramToggle = False
    
    def __call_voice_command(self):

        if self.sf.voice_function is not None:
            print("Voice function is", self.sf.voice_function)
            try:
                self.sf.voice_function = eval(self.sf.voice_function)

            except Exception as err:
                print("Not a valid voice function", self.sf.voice_function)
                print("Exception: {0}".format(err))
                self.sf.voice_function = None

        if self.sf.voice_function is not None and callable(self.sf.voice_function):
            self.sf.voice_function()
            self.sf.voice_function = None # reset the function

    def timerFired(self):
        self.__call_voice_command()
        
        self.timeDate.update()
        self.news.article += 0.04

    def keyPressed(self, event, root):
        e = event.keysym
        if e == 'q': root.destroy()
        elif e == 'm': self.sf.sync_read_microphone()
        
    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill = self.bgColor)
        self.timeDate.draw(canvas)
        self.weather.draw(canvas)
        self.location.draw(canvas)
        self.news.draw(canvas)
        if self.isDrawHearts:
            canvas.create_image(self.heartimgx, self.heartimgy, image = self.heartimg)
            canvas.create_image(self.thumbsupimgx, self.thumbsupimgy, image = self.thumbsupimg)
            self.heartimgy += 10
            if self.heartimgy >= self.height:
                self.heartimgy = 0
                self.isDrawHearts = False
        if self.isInstagramToggle:
            self.instagramDraw.draw(canvas)

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
        self.instagramDraw = InstagramDraw(self.width * 7. / 8, self.height * 1. / 10)
        self.news = News(self.width/2, self.height - 175)
        #self.insta = Instagram(self.width - 200, 100)
        
        key = self.getKey(self.weather.id)
        d = {1: "Sunny.jpg", 2: "Thunderstorm.jpg", 3: "Rain.jpg", 4: "Partly Cloudy.jpg", 5: "Rain.jpg", 6: "Snow.jpg", 7: "Other.jpg", 8: "Clouds.jpg", 9: "Other.jpg"}
        self.weather.photo = ImageTk.PhotoImage(Image.open(join(BASE_PATH, d[key])))
        self.weather.moon = ImageTk.PhotoImage(Image.open(join(BASE_PATH, "Moon.jpg")))
        self.heartimg = ImageTk.PhotoImage(Image.open(join(BASE_PATH, "heart.gif")))
        self.thumbsupimg = ImageTk.PhotoImage(Image.open(join(BASE_PATH, "thumbsUp.gif")))

        self.heartimgx = self.width / 2.
        self.heartimgy = 0
        self.thumbsupimgx = self.width * 7. / 8
        self.thumbsupimgy = self.height * 1. / 2


        root.wm_title("SmartMirror")
        root.geometry(str(self.width) + "x" + str(self.height))
        self.timerDelay = 200 # milliseconds
        self.canvas = Canvas(root, width = self.width, height=self.height)
        self.canvas.pack()


        # Initialize and start speech to functioner:
        self.sf = SpeechFunctioner()
        # self.sf.async_read_microphone();


        root.bind("<Key>", lambda event: keyPressedWrapper(event, self.canvas, self, root))

        timerFiredWrapper(self.canvas, self)
        root.mainloop()
        print("bye!")

sm = SmartMirror()
sm.run()
