#Django Imports
from django.test import TestCase
import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

#Application Imports
from climate.ETL import LocationLoader
from climate.models import Location,Temperature

class LocationLoaderTest(TestCase):
    
    
    def test_get_open_weather_city(self):
        print('Validate successful call of weather data by city')
        loc_loader = LocationLoader()
        data = loc_loader.get_open_weather_city('Los Angeles,ca')
        print('Data Received from API Call')
        print(data)
        self.assertEqual(data[u'name'], u'Los Angeles')
        
    
    def test_get_open_weather_city_metric(self):
        print('Validate successful call of METRIC weather data by city')
        loc_loader = LocationLoader()
        data = loc_loader.get_open_weather_city_metric('Los Angeles,ca')
        print('Data Received from API Call')
        print(data)
        self.assertEqual(data[u'name'], u'Los Angeles')
        
   
    def test_get_open_weather_city_imperial(self):
        print('Validate successful call of IMPERIAL weather data by city')
        loc_loader = LocationLoader()
        data = loc_loader.get_open_weather_city_metric('Los Angeles,ca')
        print('Data Received from API Call')
        print(data)
        self.assertEqual(data[u'name'], u'Los Angeles')
        
 
    def test_save_data_city(self):
        print('Validate what is saved to the database matches what is received by JSON')
        #Current count of location and temp set for that location
        if Location.objects.filter(city_name='Pittsburgh').exists():
            Pitt = Location.objects.filter(city_name='Pittsburgh')
            Temp = Temperature.objects.get(location=Pitt)
            Orig_count = Temp.count()
        else:
            Orig_count = 0
        
        #Save a new entry
        loc_loader = LocationLoader()
        loc_loader.save_data_city('Pittsburgh,pa')
        
        #Assert location and tempset have been entered
        Pitt = Location.objects.get(city_name='Pittsburgh')
        Temp_count = Pitt.temperature_set.all().count()
        self.assertTrue(Location.objects.filter(city_name='Pittsburgh').exists())
        self.assertTrue(Temp_count == Orig_count + 1)
       
        
        
    
        