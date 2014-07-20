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
    url(r'^about/', views.AboutView.as_view(), name='about'),
    url(r'^history/', views.HistoryCityInput, name='history'),
    url(r'^forecast/', views.forecastInput, name='forecast'),
    url(r'^(?P<location_id>[0-9]+)/history_graph/$', views.HistoryGraph, name='history_graph'),
    url(r'^(?P<id>[0-9]+)/(?P<units>[0-9])/(?P<high_low>[0-9])/(?P<start_date>(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]))/(?P<end_date>(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]))/citydetail/$', views.CityHistoryGraphs, name='citydetail'),
    url(r'^(?P<id>[0-9]+)/(?P<units>[0-9])/(?P<start_date>(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]))/(?P<end_date>(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]))/citydetailwind/$', views.CityHistoryGraphsWind, name='citydetail_wind'),
    url(r'^(?P<id>[0-9]+)/forecastdetail/$', views.ForecastGraphs, name='forecastdetail'),
    url(r'^admin/', include(admin.site.urls)),
)
