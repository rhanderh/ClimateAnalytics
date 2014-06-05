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
    def test_get_open_weather_city_call(self):
        loc_loader = LocationLoader()
        data = loc_loader.get_open_weather_city('Los Angeles,ca')
        self.assertEqual(data[u'name'], u'Los Angeles')