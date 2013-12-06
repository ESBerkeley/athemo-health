__author__ = 'ericxiao'
#from django.db import models
from django.contrib import admin
from models import HealthcarePlan, GeographicArea, Provider

'''class ItemForSaleAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_created', 'owner', 'price', 'category')
    list_filter = ['time_created', 'pending_flag', 'sold', 'deleted', 'approved', 'category__name', 'price']
    readonly_fields = ['time_created', 'pending_buyer']
    search_fields = ['title', 'body', 'category__name', 'owner__first_name', 'owner__last_name']
    date_hierarchy = 'time_created'
'''
class GeographicAreaAdmin(admin.ModelAdmin):
    list_display = ('zip_code', 'state', 'county', 'rating_area')
    search_fields = ('zip_code', 'state', 'county', 'rating_area')

class HealthcarePlanAdmin(admin.ModelAdmin):
    list_display = ('medal', 'price', 'age')
    search_fields = ('medal', 'price', 'age')

admin.site.register(HealthcarePlan, HealthcarePlanAdmin)
admin.site.register(GeographicArea, GeographicAreaAdmin)
admin.site.register(Provider)