#Django Imports
from django.test import TestCase
import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

#Application Imports
from climate.ETL import LocationLoader

class LocationLoaderTest(TestCase):
    
    #Validate successful call of weather data by city
    def test_get_open_weather_city(self):
        loc_loader = LocationLoader()
        data = loc_loader.get_open_weather_city('Los Angeles,ca')
        print('Data Received from API Call')
        print(data)
        self.assertEqual(data[u'name'], u'Los Angeles')
        
    #Validate successful call of METRIC weather data by city
    def test_get_open_weather_city_metric(self):
        loc_loader = LocationLoader()
        data = loc_loader.get_open_weather_city_metric('Los Angeles,ca')
        print('Data Received from API Call')
        print(data)
        self.assertEqual(data[u'name'], u'Los Angeles')
        
    #Validate successful call of IMPERIAL weather data by city
    def test_get_open_weather_city_imperial(self):
        loc_loader = LocationLoader()
        data = loc_loader.get_open_weather_city_metric('Los Angeles,ca')
        print('Data Received from API Call')
        print(data)
        self.assertEqual(data[u'name'], u'Los Angeles')
        
    #Validate what is saved to the database matches what is received by JSON
    
        