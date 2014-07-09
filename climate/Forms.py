'''
Created on Jun 28, 2014

@author: Ryan
'''

from django import forms
from django.forms import ModelForm

from climate.models import Temperature, Location, WindSpeed, Advection



class CityHistForm(forms.Form):
    city_name = forms.CharField(label='City name', max_length=100)
    
class CityForm(ModelForm):
    
    UNIT_CHOICE=(('1','Metric'),('2','Imperial'),('3','Standard'))
    
    city_name = forms.ChoiceField(choices=[(location.id, location.city_name) for location in Location.objects.all()])
    units = forms.ChoiceField(choices=UNIT_CHOICE)
    
    class Meta:
        model=Location
        fields = ['city_name']


