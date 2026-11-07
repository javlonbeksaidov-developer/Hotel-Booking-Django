from django.urls import path

from .views import home_page

app_name = "hotels"

urlpatterns = [path("home/", home_page, name="home")]
