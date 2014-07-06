#Django Imports
from django.test import TestCase
import datetime
import pytz
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db.models import Max

#Application Imports
from climate.ETL import LocationLoader, LocationLoaderHist
from climate.models import Location,Temperature, WindSpeed
from climate import views

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
        data = loc_loader.get_open_weather_city_imperial('Los Angeles,ca')
        print('Data Received from API Call')
        print(data)
        self.assertEqual(data[u'name'], u'Los Angeles')
        
 
    def test_save_data_city(self):
        print('Validate what is saved to the database matches what is received by JSON')
        #Current count of location and temp set for that location
        if Location.objects.filter(city_name='Pittsburgh').exists():
            Pitt = Location.objects.filter(city_name='Pittsburgh')
            Temp = Temperature.objects.get(location=Pitt)
            Wind = WindSpeed.objects.get(location=Pitt)
            Orig_count = Temp.count()
            Orig_wind = Wind.count()
        else:
            Orig_count = 0
            Orig_wind = 0
        
        #Save a new entry
        loc_loader = LocationLoader()
        loc_loader.save_data_city('Pittsburgh,pa')
        
        #Assert location and tempset have been entered
        Pitt = Location.objects.get(city_name='Pittsburgh')
        Temp_count = Pitt.temperature_set.all().count()
        Wind_count = Pitt.windspeed_set.all().count()
        self.assertTrue(Location.objects.filter(city_name='Pittsburgh').exists())
        self.assertTrue(Temp_count == Orig_count + 1)
        self.assertTrue(Wind_count == Orig_wind + 1)
       

class LocationLoaderHistTest(TestCase):

    def test_get_open_weather_city_hist(self):
        print('Validate successful history call of weather data by city')
        loc_loader = LocationLoaderHist()
        start_date_test = datetime.datetime.now() + datetime.timedelta(-30)
        end_date_test = datetime.datetime.now()
        data = loc_loader.get_open_weather_city_hist('5367929', start_date_test, end_date_test)
        print('Data Received from API Call-------------------')
        print(data)
        self.assertEqual(len(data[u'list']), data[u'cnt'])

    
    def test_get_open_weather_city_hist_metric(self):
        print('Validate successful call of METRIC weather data by city')
        loc_loader = LocationLoaderHist()
        start_date_test = datetime.datetime.now() + datetime.timedelta(-30)
        data = loc_loader.get_open_weather_city_hist_metric('5367929', start_date_test)
        print('Data Received from API Call-------------------')
        print(data)
        self.assertEqual(len(data[u'list']), data[u'cnt'])
        
   
    def test_get_open_weather_city_hist_imperial(self):
        print('Validate successful call of IMPERIAL weather data by city')
        loc_loader = LocationLoaderHist()
        start_date_test = datetime.datetime.now() + datetime.timedelta(-30)
        data = loc_loader.get_open_weather_city_hist_imperial('5367929', start_date_test)
        print('Data Received from API Call-------------------')
        print(data)
        self.assertEqual(len(data[u'list']), data[u'cnt'])
        
    def test_save_data_city_hist(self):
        
        loc_loader = LocationLoader()
        loc_loader.save_data_city('Pittsburgh,pa')
        
        
        print('Validate what is saved to the database matches what is received by JSON')
        #Current count of location and temp set for that location
        if Location.objects.filter(city_name='Pittsburgh').exists():
            Pitt = Location.objects.filter(city_name='Pittsburgh')
            Temp = Temperature.objects.get(location=Pitt)
            Wind = WindSpeed.objects.get(location=Pitt)
            Orig_count = 0
            Orig_wind = 0
        else:
            Orig_count = 0
            Orig_wind = 0
        
        pitt = Location.objects.get(city_name='Pittsburgh')
        id = pitt.city_id
        start_date_test = datetime.datetime.now() + datetime.timedelta(-30)
        end_date_test = datetime.datetime.now()
        
        #Save a new entry
        loc_loader = LocationLoaderHist()
        loc_loader.save_data_city_hist(id, start_date_test, end_date_test)
        
        #Assert location and tempset have been entered
        Pitt = Location.objects.get(city_name='Pittsburgh')
        Temp_count = Pitt.temperature_set.all().count()
        Wind_count = Pitt.windspeed_set.all().count()
        self.assertTrue(Location.objects.filter(city_name='Pittsburgh').exists())
        print Temp_count
        print Wind_count
        self.assertTrue(Temp_count >= Orig_count + 30)
        self.assertTrue(Wind_count >= Orig_wind + 30)
        
    def test_loop_all_hist(self):
        
        #Prep the DB for Pittsburgh
        loc_loader = LocationLoader()
        loc_loader.save_data_city('Pittsburgh,pa')
        
        #prep timeframe variables
        load  = LocationLoaderHist()
        pitt = Location.objects.get(city_name='Pittsburgh')
        startb = datetime.datetime.now() + datetime.timedelta(-30)
        
        end_unaware = datetime.datetime.now() + datetime.timedelta(-1)
        end = end_unaware.replace(tzinfo=pytz.UTC)
        
        #clear out conflicting data
        pitt.temperature_set.all().delete()
        pitt.windspeed_set.all().delete()
        
        load.loop_all_hist('Pittsburgh',startb)
        
        #validate
        wind_max_dict = pitt.windspeed_set.all().aggregate(Max('timestamp'))
        temp_max_dict = pitt.temperature_set.all().aggregate(Max('timestamp')) 
        
        wind_max = wind_max_dict['timestamp__max']
        temp_max = temp_max_dict['timestamp__max']
        
        
        self.assertTrue( (wind_max - end) <= datetime.timedelta(days = 1))
        self.assertTrue( (temp_max - end) <= datetime.timedelta(days = 1))
    
        