# from django.contrib import admin
import django.contrib.gis.admin as admin
from .models import User, Profile, Fishingmark

admin.site.register(User)
admin.site.register(Profile)
#admin.site.register(Fishingmark, admin.OSMGeoAdmin)