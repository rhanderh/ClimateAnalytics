from climate.models import Location, Temperature, WindSpeed
from django.core.exceptions import ValidationError
from decimal import Decimal
import json
import urllib2
import datetime

class LocationLoader():

    #Capture location data for a particular city by name
    def get_open_weather_city(self, name):
        data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + name))
        return data
    
    def get_open_weather_city_metric(self, name):
        data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + name + '&units=metric'))
        return data
    
    def get_open_weather_city_imperial(self, name):
        data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + name + '&units=imperial'))
        return data  
    
    def save_data_city(self, name):
        
        #Call weather api's to collect data
        data = self.get_open_weather_city(name)
        metric_data = self.get_open_weather_city_metric(name)
        imperial_data = self.get_open_weather_city_imperial(name)
        
        data_save = DataSaverLocation()
        
        data_save.commit_data(data,metric_data,imperial_data)
           
            
class LocationLoaderHist():       
        
        def get_open_weather_city_hist(self, name):
            data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/history/city?q=' + name + '&type=day'))
            return data 
        
        def get_open_weather_city_hist_metric(self, name):
            data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/history/city?q=' + name + '&type=day' + '&units=metric'))
            return data 
        
        def get_open_weather_city_hist_imperial(self, name):
            data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/history/city?q=' + name + '&type=day' + '&units=imperial'))
            return data 
        
        def save_data_city_hist(self, name):
        
        #Call weather api's to collect data
            data = self.get_open_weather_city_hist(name)

            
            data_save = DataSaverLocation()
            
            i=0
            while i < data[u'cnt']:
                data_save.commit_data_hist(data[u'city_id'],data[u'list'][i])
                i = i + 1
            
class DataSaverLocation():           
        def commit_data(self,data,metric_data,imperial_data):
            
        
        #Prep model objects
            loc = Location()
            temp_data = Temperature()
            wind_data = WindSpeed()

        #Assign location fields from collected json data
            loc.longitude = data[u'coord'][u'lon']
            loc.latitude = data[u'coord'][u'lat']
            loc.city_id = data[u'id']
            loc.city_name = data[u'name']
        
        #Insert Location if it does not already exist
        
            try:
                comp = Location.objects.get(city_id = data[u'id'])
            except:
                loc.save()
            else:   
                print "location exists"
        
        
        #Assign temperature fields from collected json data
            temp_data.temp_min = Decimal(data[u'main'][u'temp_min'])
            temp_data.temp_max = Decimal(data[u'main'][u'temp_max'])
            temp_data.temp = Decimal(data[u'main'][u'temp'])
            temp_data.temp_min_imperial = Decimal(imperial_data[u'main'][u'temp_min'])
            temp_data.temp_max_imperial = Decimal(imperial_data[u'main'][u'temp_max'])
            temp_data.temp_imperial = Decimal(imperial_data[u'main'][u'temp'])
            temp_data.temp_min_metric = Decimal(metric_data[u'main'][u'temp_min'])
            temp_data.temp_max_metric = Decimal(metric_data[u'main'][u'temp_max'])
            temp_data.temp_metric = Decimal(metric_data[u'main'][u'temp'])
            temp_data.location = Location.objects.get(city_id = loc.city_id)
        
        #Save temperature data
            temp_data.save()
        
        #Assign windspeed fields from collected json data
            wind_data.location = Location.objects.get(city_id = loc.city_id)
            wind_data.wind_speed = Decimal(data[u'wind'][u'speed'])
            wind_data.degree = Decimal(data[u'wind'][u'deg'])
            wind_data.wind_speed_imperial = Decimal(imperial_data[u'wind'][u'speed'])
            wind_data.degree_imperial = Decimal(imperial_data[u'wind'][u'deg'])
            wind_data.wind_speed_metric = Decimal(metric_data[u'wind'][u'speed'])
            wind_data.degree_metric = Decimal(metric_data[u'wind'][u'deg'])
        
        #Save windspeed data
            wind_data.save()
        
        
        def commit_data_hist(self,city,data):
            
        
        #Prep model objects
            temp_data = Temperature()
            wind_data = WindSpeed()
        
   
        #Assign temperature fields from collected json data
            temp_data.temp_min = Decimal(data[u'main'][u'temp_min'])
            temp_data.temp_max = Decimal(data[u'main'][u'temp_max'])
            temp_data.temp = Decimal(data[u'main'][u'temp'])
            temp_data.temp_min_imperial = Decimal(Decimal(1.8) * (Decimal(data[u'main'][u'temp_min']) - Decimal(273.5000)) + Decimal(32.0000))
            temp_data.temp_max_imperial = Decimal(Decimal(1.8) * (Decimal(data[u'main'][u'temp_min']) - Decimal(273.5000)) + Decimal(32.0000))
            temp_data.temp_imperial = Decimal(Decimal(1.8) * (Decimal(data[u'main'][u'temp_min']) - Decimal(273.5000)) + Decimal(32.0000))
            temp_data.temp_min_metric = (Decimal(data[u'main'][u'temp_min']) - Decimal(273.5000))
            temp_data.temp_max_metric = (Decimal(data[u'main'][u'temp_max']) - Decimal(273.5000))
            temp_data.temp_metric = (Decimal(data[u'main'][u'temp']) - Decimal(273.5000))
            temp_data.location = Location.objects.get(city_id = city)
        
        #Save temperature data
            temp_data.save()
        
        #Assign windspeed fields from collected json data
            wind_data.location = Location.objects.get(city_id = city)
            wind_data.wind_speed = Decimal(data[u'wind'][u'speed'])
            wind_data.degree = Decimal(data[u'wind'][u'deg'])
            wind_data.wind_speed_imperial = Decimal(data[u'wind'][u'speed'])
            wind_data.degree_imperial = Decimal(data[u'wind'][u'deg'])
            wind_data.wind_speed_metric = Decimal(data[u'wind'][u'speed'])
            wind_data.degree_metric = Decimal(data[u'wind'][u'deg'])
        
        #Save windspeed data
            wind_data.save()
            
        def commit_data_loc(self,data):
        
        #Prep model objects
            loc = Location()

        #Assign location fields from collected json data
            loc.longitude = data[u'coord'][u'lon']
            loc.latitude = data[u'coord'][u'lat']
            loc.city_id = data[u'id']
            loc.city_name = data[u'name']
        
        #Insert Location if it does not already exist
        
            try:
                comp = Location.objects.get(city_id = data[u'id'])
            except:
                loc.save()
            else:   
                print "location exists"

        