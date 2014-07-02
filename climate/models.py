from django.db import models
import json
import urllib2
import datetime


class Location(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    city_id = models.CharField(max_length=50)
    city_name = models.CharField(max_length=200)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.city_name

class Temperature(models.Model):
    temp_min = models.DecimalField(max_digits=9,decimal_places=4)
    temp_max = models.DecimalField(max_digits=9,decimal_places=4)
    temp = models.DecimalField(max_digits=9,decimal_places=4)
    temp_min_imperial = models.DecimalField(max_digits=9,decimal_places=4)
    temp_max_imperial = models.DecimalField(max_digits=9,decimal_places=4)
    temp_imperial = models.DecimalField(max_digits=9,decimal_places=4)
    temp_min_metric = models.DecimalField(max_digits=9,decimal_places=4)
    temp_max_metric = models.DecimalField(max_digits=9,decimal_places=4)
    temp_metric = models.DecimalField(max_digits=9,decimal_places=4)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    location = models.ForeignKey(Location)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.temp_max_imperial)
    
class WindSpeed(models.Model):
    wind_speed = models.DecimalField(max_digits=9,decimal_places=4)
    wind_speed_imperial = models.DecimalField(max_digits=9,decimal_places=4)
    wind_speed_metric = models.DecimalField(max_digits=9,decimal_places=4)
    degree = models.DecimalField(max_digits=9,decimal_places=4)
    degree_imperial = models.DecimalField(max_digits=9,decimal_places=4)
    degree_metric = models.DecimalField(max_digits=9,decimal_places=4)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    location = models.ForeignKey(Location)

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.wind_speed)
    
class Advection(models.Model):
    advection = models.DecimalField(max_digits=9,decimal_places=4)
    advection_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    location = models.ForeignKey(Location)
    