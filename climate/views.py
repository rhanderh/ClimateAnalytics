from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import Http404
from django.views import generic

from climate.models import Temperature, Location, WindSpeed, Advection
from climate.Forms import CityHistForm, CityForm

import datetime

# Create your views here.

def CityHistoryGraphs(request, id):
    try:
        location = Location.objects.get(pk=id)
        json_temp = serializers.serialize("json", location.temperature_set.all().order_by('timestamp'))
    except Location.DoesNotExist:
        raise Http404
    return render(request, 'climate/citydetail.html', {'location': location, 'json_temp' : json_temp})

def ForecastGraphs(request, id):
    try:
        location = Location.objects.get(pk=id)
        NY = Location.objects.get(city_name='New York')
        LA = Location.objects.get(city_name='Los Angeles')
        HOU = Location.objects.get(city_name='Houston')
        MIA = Location.objects.get(city_name='Miami')
        PHI = Location.objects.get(city_name='Philadelphia')
        BOS = Location.objects.get(city_name='Boston')
        SEA = Location.objects.get(city_name='Seattle')
        DEN = Location.objects.get(city_name='Denver')
        SF = Location.objects.get(city_name='San Francisco')
        windspeed = WindSpeed.objects.get(pk=id)
        advection = Advection.objects.get(pk=id)
        json_temp = serializers.serialize("json", location.temperature_set.all())
        jsonNY    = serializers.serialize("json", NY.temperature_set.all())        
        jsonLA    = serializers.serialize("json", LA.temperature_set.all())
        jsonHOU    = serializers.serialize("json", HOU.temperature_set.all())
        jsonMIA    = serializers.serialize("json", MIA.temperature_set.all())
        jsonPHI    = serializers.serialize("json", PHI.temperature_set.all())
        jsonBOS    = serializers.serialize("json", BOS.temperature_set.all())
        jsonSEA    = serializers.serialize("json", SEA.temperature_set.all())
        jsonDEN    = serializers.serialize("json", DEN.temperature_set.all())
        jsonSF    = serializers.serialize("json",  SF.temperature_set.all())
        json_ctemp = serializers.serialize("json", location.temperature_set.all())

        jsonNYct = serializers.serialize("json", NY.temperature_set.all())
        jsonLAct = serializers.serialize("json", LA.temperature_set.all())
        jsonHOUct = serializers.serialize("json", HOU.temperature_set.all())
        jsonMIAct = serializers.serialize("json", MIA.temperature_set.all())
        jsonPHIct = serializers.serialize("json", PHI.temperature_set.all())
        jsonBOSct = serializers.serialize("json", BOS.temperature_set.all())
        jsonSEAct = serializers.serialize("json", SEA.temperature_set.all())
        jsonDENct = serializers.serialize("json", DEN.temperature_set.all())
        jsonSFct = serializers.serialize("json", SF.temperature_set.all())
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
    return render(request,'climate/forecastdetail.html',{'location': location, 'json_temp': json_temp , 'windspeed': json_wind[87:92],'advection': json_advection[81:85], 'json_ctemp' : json_ctemp[256:262],
                                                          'json_gradient' : json_gradient, 'jsonNYct': jsonNYct[259:266],'jsonLAct': jsonLAct[256:262], 
                                                           'jsonHOUct': jsonHOUct[256:262], 'jsonMIAct': jsonMIAct[255:262],'jsonPHIct': jsonPHIct[256:262],
                                                           'jsonBOSct': jsonBOSct[256:262], 'jsonSEAct': jsonSEAct[256:262], 'jsonDENct': jsonDENct[255:262], 
                                                             })

    
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
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/' + form.cleaned_data['city_name'] + '/citydetail/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CityForm()

    return render(request, 'climate/history.html', {'form': form})
    

def forecastInput(request):
       # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CityForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/' + form.cleaned_data['city_name'] + '/forecastdetail/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CityForm()

    return render(request, 'climate/forecast.html', {'form': form})


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CityHistForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CityHistForm()

    return render(request, 'climate/name.html', {'form': form})

def get_thanks(request):
    return render(request, 'climate/thankyou.html')


   # def get_temperature(self,location):
   #     return Temperature.objects.get(location=location)
