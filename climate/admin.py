from django.contrib import admin
from climate.models import Temperature, Location, WindSpeed


# Register your models here.
admin.site.register(Temperature)
admin.site.register(Location)
admin.site.register(WindSpeed)