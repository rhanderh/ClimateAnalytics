from climate.models import Location, Temperature
import json
import urllib2

class LocationLoader():

    #Capture and store data location data for a particular city by name
    def get_open_weather_city(self, name):
        data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + name))
        return data
    