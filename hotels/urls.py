from django.urls import path

from .views import (
    about_page,
    contact_page,
    gallery_page,
    home_page,
    location_page,
    rooms_page,
    services_page,
)

app_name = "hotels"

urlpatterns = [
    path("", home_page, name="home"),
    path("about/", about_page, name="about"),
    path("rooms/", rooms_page, name="rooms"),
    path("services/", services_page, name="services"),
    path("gallery/", gallery_page, name="gallery"),
    path("location/", location_page, name="location"),
    path("contact/", contact_page, name="contact"),
]
