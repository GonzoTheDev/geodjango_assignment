from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from userlocation.views import update_location, map_view, chatbot_response 

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("map/", map_view, name="map"),
    path("updatedb/", update_location, name="update_location"),
    path("", include("pwa.urls")),
    path("chatbot/", chatbot_response, name="chatbot_response"),
]
