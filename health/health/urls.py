from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'insuranceapp.views.home', name='home'),
    url(r'^household_info', 'insuranceapp.views.household_info', name='household_info'),
    url(r'^about', 'insuranceapp.views.about', name='about'),
    url(r'^contact', 'insuranceapp.views.contact', name='contact'),
    url(r'^team', 'insuranceapp.views.team', name='team'),
    url(r'^plans', 'insuranceapp.views.plans'),
    url(r'^ajax/get_plans', 'insuranceapp.views.ajax_get_plans'),
    #url(r'^metal_tiers', 'insuranceapp.views.metal', name='metal'),
    # url(r'^health/', include('health.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
