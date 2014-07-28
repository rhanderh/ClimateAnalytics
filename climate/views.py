from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.core.urlresolvers import reverse
from django.core import serializers
import json
from django.http import Http404
from django.views import generic
from django.db.models import Max, Min, Avg

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

from climate.models import Temperature, Location, WindSpeed, Advection
from climate.Forms import CityHistForm, CityForm, ForecastForm

import datetime
from datetime import date
from decimal import *
import pytz

#json encoder for dictionary objects
class MyEncoder1(json.JSONEncoder):
    def default(self, obj):
        
        obj['timestamp'] = datetime.datetime.combine(obj['timestamp'],datetime.datetime.min.time())
        obj['timestamp'] = obj['timestamp'].strftime('%Y-%m-%dT00:00:00')
        obj['temp_max'] = str(obj['temp_max'])
        

        return super(MyEncoder1, self).encode(obj)
    
# Create your views here.

def CityCompareGraphs(request):
    try:
        #load the cities for the graph
        NY = Location.objects.get(city_name='New York')
        CHI = Location.objects.get(city_name='Chicago')
        LA = Location.objects.get(city_name='Los Angeles')
        HOU = Location.objects.get(city_name='Houston')
        MIA = Location.objects.get(city_name='Miami')
        BOS = Location.objects.get(city_name='Boston')
        SEA = Location.objects.get(city_name='Seattle')
        SF = Location.objects.get(city_name='San Francisco')
        DNV = Location.objects.get(city_name='Denver')
        PIT = Location.objects.get(city_name='Pittsburgh')
        
        #get the max times for each
        NY_max_time = NY.temperature_set.all().aggregate(Max('timestamp'))
        CHI_max_time = CHI.temperature_set.all().aggregate(Max('timestamp'))
        LA_max_time = LA.temperature_set.all().aggregate(Max('timestamp'))
        
        #Last 30 for each
        NY_last_30 = NY_max_time['timestamp__max'] - datetime.timedelta(days=30)
        CHI_last_30 = CHI_max_time['timestamp__max'] - datetime.timedelta(days=30)
        LA_last_30 = LA_max_time['timestamp__max'] - datetime.timedelta(days=30)
        
        #calculate the last 30 days temps for each
        NY_30 = NY.temperature_set.filter(timestamp__gte=NY_last_30).order_by('timestamp')
        CHI_30 = CHI.temperature_set.filter(timestamp__gte=CHI_last_30).order_by('timestamp')
        LA_30 = LA.temperature_set.filter(timestamp__gte=LA_last_30).order_by('timestamp')
        HOU_30 = HOU.temperature_set.filter(timestamp__gte=LA_last_30).order_by('timestamp')
        MIA_30 = MIA.temperature_set.filter(timestamp__gte=LA_last_30).order_by('timestamp')
        BOS_30 = BOS.temperature_set.filter(timestamp__gte=LA_last_30).order_by('timestamp')
        SEA_30 = SEA.temperature_set.filter(timestamp__gte=LA_last_30).order_by('timestamp')
        SF_30 = SF.temperature_set.filter(timestamp__gte=LA_last_30).order_by('timestamp')
        DNV_30 = DNV.temperature_set.filter(timestamp__gte=LA_last_30).order_by('timestamp')
        PIT_30 = PIT.temperature_set.filter(timestamp__gte=LA_last_30).order_by('timestamp')
        
        #Calculate the 30 day avg for each
        NY_avg_pre = NY_30.aggregate(Avg('temp_max_imperial'))
        NY_avg = "{:.4f}".format(NY_avg_pre['temp_max_imperial__avg'])
        
        CHI_avg_pre = CHI_30.aggregate(Avg('temp_max_imperial'))
        CHI_avg = "{:.4f}".format(CHI_avg_pre['temp_max_imperial__avg'])
        
        LA_avg_pre = LA_30.aggregate(Avg('temp_max_imperial'))
        LA_avg = "{:.4f}".format(LA_avg_pre['temp_max_imperial__avg'])
        
        HOU_avg_pre = HOU_30.aggregate(Avg('temp_max_imperial'))
        HOU_avg = "{:.4f}".format(HOU_avg_pre['temp_max_imperial__avg'])
        
        MIA_avg_pre = MIA_30.aggregate(Avg('temp_max_imperial'))
        MIA_avg = "{:.4f}".format(MIA_avg_pre['temp_max_imperial__avg'])
        
        BOS_avg_pre = BOS_30.aggregate(Avg('temp_max_imperial'))
        BOS_avg = "{:.4f}".format(BOS_avg_pre['temp_max_imperial__avg'])
        
        SEA_avg_pre = SEA_30.aggregate(Avg('temp_max_imperial'))
        SEA_avg = "{:.4f}".format(SEA_avg_pre['temp_max_imperial__avg'])
        
        SF_avg_pre = SF_30.aggregate(Avg('temp_max_imperial'))
        SF_avg = "{:.4f}".format(SF_avg_pre['temp_max_imperial__avg']) 
        
        DNV_avg_pre = DNV_30.aggregate(Avg('temp_max_imperial'))
        DNV_avg = "{:.4f}".format(DNV_avg_pre['temp_max_imperial__avg'])
        
        PIT_avg_pre = PIT_30.aggregate(Avg('temp_max_imperial'))
        PIT_avg = "{:.4f}".format(PIT_avg_pre['temp_max_imperial__avg'])
        
    except Location.DoesNotExist:
        raise Http404
    return render(request, 'climate/compare.html', {'NY_avg' : NY_avg, 'LA_avg' : LA_avg, 'CHI_avg' : CHI_avg, 'HOU_avg' : HOU_avg,
                                                    'MIA_avg' : MIA_avg, 'BOS_avg' : BOS_avg, 'SEA_avg' : SEA_avg, 'SF_avg' : SF_avg,
                                                    'DNV_avg' : DNV_avg, 'PIT_avg' : PIT_avg})
        

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
        
        #Set to high temp, imperial units
        high_low = '2'
        units = '2'
        
        #Location for user selection
        location = Location.objects.get(pk=id)
        
        #Get the latest temperature
        max_temp_time = location.temperature_set.all().aggregate(Max('timestamp'))
        latest_temp = location.temperature_set.get(timestamp=max_temp_time['timestamp__max'])
        
        #Get the latest reference city temperature - Currently SF is always the ref city
        sf = Location.objects.get(city_name='San Francisco')

        sf_max_time = sf.temperature_set.all().aggregate(Max('timestamp'))

        sf_temp = sf.temperature_set.get(timestamp=sf_max_time['timestamp__max'])
        
        #Get the latest windspeed
        max_wind_time = location.windspeed_set.all().aggregate(Max('timestamp'))
        latest_wind = location.windspeed_set.get(timestamp=max_wind_time['timestamp__max'])
        
        #Get the 5 day avg high temperature
        last_5_days = max_temp_time['timestamp__max'] - datetime.timedelta(days=5)
        avg_5_temp = location.temperature_set.filter(timestamp__gte=last_5_days).aggregate(Avg('temp_max_imperial'))
        avg_5_temp_final = "{:.4f}".format(avg_5_temp['temp_max_imperial__avg'])
        
        #Calculate the Gradient (Temp2-Temp1/Distance)
        gradient = -((sf_temp.temp_max_imperial - latest_temp.temp_max_imperial) / 500)
        gradient = "{:.4f}".format(gradient)
        
        print(gradient)

        #Calculate the Advection
        getcontext().prec=4
        advection = (latest_wind.wind_speed_imperial * Decimal(gradient) * Decimal(24))
      
        print ('initial advection is :')
        print (advection) 
 
        #Tomorrow's forecast based on the above
        tomorrow = (latest_temp.temp_max_imperial + advection)
        print(latest_temp.temp_max_imperial)
        print(tomorrow)


        #Future Prediction - Modify when we add a user variable to select range
        y = 2
        temperature_f = tomorrow
        advection_f = advection
        #prep_list = []
        temp_list = []
        temp_dict = {}
        
        temp_dict['temp_max_imperial'] = "{:.4f}".format(temperature_f)
        advection_f = (latest_wind.wind_speed_imperial * Decimal(gradient) * Decimal(24 * y)) + 6  
        print ('advection is:')
        print (advection_f)
        temperature_f = temperature_f + advection_f + 6 
        print ('temperature_f is:')
        print (temperature_f)  
        temp_list.append(temp_dict.copy())
            
        temp_dict['temp_max_imperial'] = "{:.4f}".format(temperature_f)
        advection_f = (latest_wind.wind_speed_imperial * Decimal(gradient) * Decimal(24 * 1)) + 5 
        print ('advection is:')
        print (advection_f)
        temperature_f = temperature_f + advection_f  + 5 
        print ('temperature_f is:')
        print (temperature_f) 
        temp_list.append(temp_dict.copy())

        temp_dict['temp_max_imperial'] = "{:.4f}".format(temperature_f)
        advection_f = (latest_wind.wind_speed_imperial * Decimal(gradient) * Decimal(24 * 1)) + 4    
        print ('advection is:')
        print (advection_f)
        temperature_f = temperature_f + advection_f + 4   
        print ('temperature_f is:')
        print (temperature_f)    
        temp_list.append(temp_dict.copy())

        temp_dict['temp_max_imperial'] = "{:.4f}".format(temperature_f)
        advection_f = (latest_wind.wind_speed_imperial * Decimal(gradient) * Decimal(24 * 1)) + 3 
        print ('advection is:')
        print (advection_f)
        temperature_f = temperature_f + advection_f + 3
        print ('temperature_f is:')
        print (temperature_f)
        temp_list.append(temp_dict.copy())

        temp_dict['temp_max_imperial'] = "{:.4f}".format(temperature_f)
        advection_f = (latest_wind.wind_speed_imperial * Decimal(gradient) * Decimal(24 * 1)) + 2 
        print ('advection is:')
        print (advection_f)
        temperature_f = temperature_f + advection_f + 2
        print ('temperature_f is:')
        print (temperature_f)
        temp_list.append(temp_dict.copy())

        temp_dict['temp_max_imperial'] = "{:.4f}".format(temperature_f)
        advection_f = (latest_wind.wind_speed_imperial * Decimal(gradient) * Decimal(24 * 1)) + 1 
        print ('advection is:')
        print (advection_f)
        temperature_f = temperature_f + advection_f + 1
        print ('temperature_f is:')
        print (temperature_f)
        temp_list.append(temp_dict.copy())

        temp_dict['temp_max_imperial'] = "{:.4f}".format(temperature_f)
        advection_f = (latest_wind.wind_speed_imperial * Decimal(gradient) * Decimal(24 * 1)) 
        print ('advection is:')
        print (advection_f)
        temperature_f = temperature_f + advection_f 
        print ('temperature_f is:')
        print (temperature_f)
        temp_list.append(temp_dict.copy())

            
        keys = ('temp_max_imperial')
            
        print(temp_list)
        
        #5 Day Historical Graph for the Location Data
        five_temp = location.temperature_set.filter(timestamp__gte=last_5_days).order_by('timestamp')
        json_temp = serializers.serialize("json", five_temp)
        
        #5 Day Forecast Data
        json_forecast = json.dumps(temp_list, default=float)
        max_json_time = json.dumps(max_temp_time['timestamp__max'], default=str)
      
 
        print(max_json_time) 
        print(json_forecast) 
        print(temp_list)    
   
        print('hello')
        print(json_forecast)
 
    except Location.DoesNotExist:
        raise Http404
    return render(request,'climate/forecastdetail.html',{'location': location, 'latest_temp' : latest_temp, 'latest_wind' : latest_wind,
                                                          'avg_5_temp_final' : avg_5_temp_final, 'gradient' : gradient, 'advection' : advection,
                                                          'tomorrow' : tomorrow, 'json_temp' : json_temp, 'high_low' : high_low, 'units' : units,
                                                           'json_forecast': json_forecast, 'max_temp_time' : max_json_time   })

    
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




