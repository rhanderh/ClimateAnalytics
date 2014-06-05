from django.contrib import admin
from climate.models import Temperature, Location


# Register your models here.
admin.site.register(Temperature)
admin.site.register(Location)