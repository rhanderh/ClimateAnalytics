from climate.models import Location, Temperature
from django.core.exceptions import ValidationError
from decimal import Decimal
import json
import urllib2

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
        
        #Prep model objects
        loc = Location()
        temp_data = Temperature()

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
        
        
 
        
        
            
            
            
            
            
            