from tkinter import *
import time
import datetime

#Will need downloading
from lxml import html           # `python3 -m pip install lxml`
import json
import requests                 # `python3 -m pip install requests`
from PIL import Image, ImageTk  # `python3 -m pip install pillow`
from os.path import join

BASE_PATH = "images"

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
        lat = j['latitude']
        lon = j['longitude']
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
        self.windDeg = weather['wind']['deg']
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

    def draw(self, canvas, width):
        line1 = Text(self.x, self.y - 35, str(self.temp) + chr(176), 24, anc = 'w')
        line2 = Text(self.x, self.y - 10, self.descript, 16, anc = 'w')
        line3 = Text(self.x, self.y + 10, "Humidity " + str(self.humidity) + "%", 16, anc = 'w')
        line4 = Text(self.x, self.y + 30, "Sundown " + self.sunset, 16, anc = 'w')
        line1.drawText(canvas)
        line2.drawText(canvas)
        line3.drawText(canvas)
        line4.drawText(canvas)
        if self.isDayTime(cleanTime(time.strftime("%H:%M")), self.sunrise24, self.sunset24):
            img = self.photo
        else:
            img = self.moon
        canvas.create_image(width, self.y + 30, image = img)

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
        headline = Text(self.x, self.y, self.getArticle(), 14)
        headline.drawText(canvas)

class TimeDate(object):
    def __init__(self, x, y):
        self.time = Text(x, y - 15, "", 30)
        self.date = Text(x, y + 15, "", 20)
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
        line1 = Text(self.x, self.y, self.address, 20)
        line1.drawText(canvas)

class SmartMirror(object):
    def __init__(self, width = 700, height = 900):
        self.width, self.height = width, height
        self.bgColor = "black"
        self.timeDate = TimeDate(self.width/2, 40)
        self.weather = Weather(20, 110)
        self.location = Location(self.width/2, self.height - 30)
        self.news = news(width/2, height-80)
    
    def timerFired(self):
        self.timeDate.update()
        self.news.article += 0.04
        
    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill = self.bgColor)
        self.timeDate.draw(canvas)
        self.weather.draw(canvas, self.width/2)
        self.location.draw(canvas)
        self.news.draw(canvas)

    def run(self):
        def redrawAllWrapper(canvas, self):
            canvas.delete(ALL)
            self.redrawAll(canvas)
            canvas.update()    

        def timerFiredWrapper(canvas, self):
            self.timerFired()
            redrawAllWrapper(canvas, self)
            canvas.after(self.timerDelay, timerFiredWrapper, canvas, self)
        
        root = Tk()

        if self.weather.id == 800: key = 1
        elif self.weather.id == 801: key = 4
        else: key = self.weather.id//100
        key = 9
        d = {1: "Sunny.jpg", 2: "Thunderstorm.jpg", 3: "Rain.jpg", 4: "Partly Cloudy.jpg", 5: "Rain.jpg", 6: "Snow.jpg", 7: "Other.jpg", 8: "Clouds.jpg", 9: "Other.jpg"}
        self.weather.photo = ImageTk.PhotoImage(Image.open(join(BASE_PATH, d[key])))
        self.weather.moon = ImageTk.PhotoImage(Image.open(join(BASE_PATH, "Moon.jpg")))
        root.wm_title("SmartMirror")
        root.geometry(str(self.width) + "x" + str(self.height))
        self.timerDelay = 200 # milliseconds
        canvas = Canvas(root, width =  self.width, height=self.height)
        canvas.pack()
        timerFiredWrapper(canvas, self)
        root.mainloop()
        print("bye!")
        
SmartMirror().run()
