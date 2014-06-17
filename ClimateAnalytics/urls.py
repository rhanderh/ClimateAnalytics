from django.conf.urls import patterns, include, url

from django.contrib import admin
from climate import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ClimateAnalytics.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
