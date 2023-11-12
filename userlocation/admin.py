# from django.contrib import admin
from django.contrib.gis import admin
from .models import User, Profile, Fishingmark

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Fishingmark, admin.OSMGeoAdmin)