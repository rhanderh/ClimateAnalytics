from django.db import models


class Location(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    city_id = models.CharField(max_length=50)
    city_name = models.CharField(max_length=200)
    population = models.IntegerField()

class Temperature(models.Model):
    temp_min = models.DecimalField(max_digits=9,decimal_places=4)
    temp_max = models.DecimalField(max_digits=9,decimal_places=4)
    temp = models.DecimalField(max_digits=9,decimal_places=4)
    timestamp = models.DateTimeField(auto_now_add=False)
    location = models.ForeignKey(Location)
    

    