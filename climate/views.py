from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.core.urlresolvers import reverse
from django.core import serializers
import json
from django.http import Http404
from django.views import generic
from django.db.models import Max, Min
from django.db.models import Max

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

from climate.models import Temperature, Location, WindSpeed, Advection
from climate.Forms import CityHistForm, CityForm, ForecastForm

import datetime
from datetime import date
from decimal import Decimal
import pytz

#json encoder for dictionary objects
class MyEncoder1(json.JSONEncoder):
    def default(self, obj):
        
        obj['timestamp'] = datetime.datetime.combine(obj['timestamp'],datetime.datetime.min.time())
        obj['timestamp'] = obj['timestamp'].strftime('%Y-%m-%dT00:00:00')
        obj['temp_max'] = str(obj['temp_max'])
        

        return super(MyEncoder1, self).encode(obj)
    
# Create your views here.

def CityHistoryGraphs(request, id, units, high_low, start_date, end_date):
    try:
        location = Location.objects.get(pk=id)
        print('I am the ' + start_date)
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        #Validate start and end date to ensure within range of data.  If not, set to max/min.
        max_dict = location.temperature_set.all().aggregate(Max('timestamp'))
        min_dict = location.temperature_set.all().aggregate(Min('timestamp'))
        
        max_time = max_dict['timestamp__max']
        min_time = min_dict['timestamp__min']
        
        max_time = max_time.replace(tzinfo=pytz.UTC)
        min_time = min_time.replace(tzinfo=pytz.UTC)
        
        start = start.replace(tzinfo=pytz.UTC)
        end = end.replace(tzinfo=pytz.UTC)

        if (start - min_time) >= datetime.timedelta(days = 0):
            start = start
        else:
            start =  min_time
        
        if (max_time - end) >= datetime.timedelta(days = 0):
            end = end
        else:
            end - max_time
        
        main_set = location.temperature_set.filter(timestamp__range=[start,end]).order_by('timestamp')
        
       # if aggregation == 1: 
        json_temp = serializers.serialize("json", main_set)
        #else:
         #   main_set = main_set.extra({'timestamp':"date(timestamp)"}).values('timestamp').annotate(temp_max=Max('temp_max'), 
          #                                                                                          temp_min=Min('temp_min'), 
           #                                                                                         temp_max_metric=Max('temp_max_metric', 
            #                                                                                        temp_min_metric=Min('temp_min_metric'), 
             #                                                                                       temp_max_imperial=Max('temp_max_imperial'), 
              #                                                                                      temp_min_imperial=Min('temp_min_imperial')))
            #json_temp = json.dumps(main_set, default=str)
        
        units = str(units)
        
    except Location.DoesNotExist:
        raise Http404
    return render(request, 'climate/citydetail.html', {'location': location, 'json_temp' : json_temp, 'units': units, 'high_low': high_low})


def CityHistoryGraphsWind(request, id, units, start_date, end_date):
    try:
        location = Location.objects.get(pk=id)
        print('I am the ' + start_date)
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        #Validate start and end date to ensure within range of data.  If not, set to max/min.
        max_dict = location.windspeed_set.all().aggregate(Max('timestamp'))
        min_dict = location.windspeed_set.all().aggregate(Min('timestamp'))
        
        max_time = max_dict['timestamp__max']
        min_time = min_dict['timestamp__min']
        
        max_time = max_time.replace(tzinfo=pytz.UTC)
        min_time = min_time.replace(tzinfo=pytz.UTC)
        
        start = start.replace(tzinfo=pytz.UTC)
        end = end.replace(tzinfo=pytz.UTC)

        if (start - min_time) >= datetime.timedelta(days = 0):
            start = start
        else:
            start =  min_time
        
        if (max_time - end) >= datetime.timedelta(days = 0):
            end = end
        else:
            end - max_time
        
        main_set = location.windspeed_set.filter(timestamp__range=[start,end]).order_by('timestamp')
              
        json_wind = serializers.serialize("json", main_set)
        units = str(units)
        
    except Location.DoesNotExist:
        raise Http404
    return render(request, 'climate/citydetail_wind.html', {'location': location, 'json_wind' : json_wind, 'units': units})



def ForecastGraphs(request, id):
    
      
    try:
        #Location for user selection
        location = Location.objects.get(pk=id)
       
        max_time = location.temperature_set.all().aggregate(Max('timestamp'))
        temp = location.temperature_set.get(timestamp=max_time['timestamp__max'])
        
        #Locations for current temps in other cities
        NY = Location.objects.get(city_name='New York')
        LA = Location.objects.get(city_name='Los Angeles')
        MIA = Location.objects.get(city_name='Miami')
        PHI = Location.objects.get(city_name='Philadelphia')
        BOS = Location.objects.get(city_name='Boston')
        SEA = Location.objects.get(city_name='Seattle')
        DEN = Location.objects.get(city_name='Denver')
        SF = Location.objects.get(city_name='San Francisco')
        HOU = Location.objects.get(city_name='Houston')        
        windspeed = WindSpeed.objects.get(pk=id)
        advection = Advection.objects.get(pk=id)
        
        #Serialization of the json temperature set
        #Do Math on Python object first before converting to JSON
        
        json_temp = serializers.serialize("json", location.temperature_set.all())
                
               
        #Don't grab the full temperature sets here - just grab the latest temp for today from the DB

        
        json_ctemp = serializers.serialize("json", location.temperature_set.all())

        
        try:
           json_gradient = (float(json_temp[259:266])-float(5.000))/100
        except ValueError:
           json_gradient = (float(json_temp[256:262])-float(5.000))/100 
  
        json_wind = serializers.serialize("json", WindSpeed.objects.filter(location_id=id), fields=('wind_speed'), indent =3)
        json_advection = serializers.serialize("json", Advection.objects.filter(location_id=id), fields=('advection'), indent =2)
        try:
           json_temp = float(json_temp[259:266])+float(json_advection[81:85])
        except ValueError:
           json_temp = float(json_temp[256:262])+float(json_advection[81:85])
    except Location.DoesNotExist:
        raise Http404
    return render(request,'climate/forecastdetail.html',{'location': location, 'json_temp': json_temp ,'temp':temp, 'windspeed': json_wind[87:92],'advection': json_advection[81:85], 'json_ctemp' : json_ctemp[256:262],'json_gradient' : json_gradient, })

    
def HistoryGraph(id):
    c = get_object_or_404(Location, pk=id)
    return HttpResponseRedirect(reverse('CityHistoryGraphs', args=(c.id,)))

class IndexView(generic.ListView):
    template_name = 'climate/index.html'
    context_object_name = 'all_locations_list'

    def get_queryset(self):
        return Location.objects.all()
    
class AboutView(generic.ListView):
    template_name = 'climate/about.html'
    context_object_name = 'all_locations_list'

    def get_queryset(self):
        return Location.objects.all()
    

def HistoryCityInput(request):
       # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CityForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            
            content = form.cleaned_data['topic']
            print(content)
            
            if content == '2':
                return HttpResponseRedirect('/' + form.cleaned_data['city_name'] + '/' + form.cleaned_data['units'] + '/' 
                                            + str(form.cleaned_data['start_date']) + '/' + str(form.cleaned_data['end_date']) + '/citydetailwind/')                
            else:
                # redirect to a new URL:
                return HttpResponseRedirect('/' + form.cleaned_data['city_name'] + '/' + form.cleaned_data['units'] + '/' + str(form.cleaned_data['high_low'])
                                           + '/' + str(form.cleaned_data['start_date']) + '/' + str(form.cleaned_data['end_date']) + '/citydetail/')
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CityForm()

    return render(request, 'climate/history.html', {'form': form})
    

def forecastInput(request):
       # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ForecastForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/' + form.cleaned_data['city_name'] + '/forecastdetail/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ForecastForm()

    return render(request, 'climate/forecast.html', {'form': form})



