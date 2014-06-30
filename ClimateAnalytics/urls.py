from django.conf.urls import patterns, include, url

from django.contrib import admin
from climate import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ClimateAnalytics.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^index/', views.IndexView.as_view(), name='index'),
    url(r'^history/', views.HistoryCityInput, name='history'),
    url(r'^name/', views.get_name, name='name'),
    url(r'^your-name/', views.get_name, name='your-name'),
    url(r'^thanks/', views.get_thanks, name='thanks'),
    url(r'^(?P<location_id>[0-9]+)/history_graph/$', views.HistoryGraph, name='history_graph'),
    url(r'^(?P<id>[0-9]+)/citydetail/$', views.CityHistoryGraphs, name='citydetail'),
    url(r'^admin/', include(admin.site.urls)),
)
