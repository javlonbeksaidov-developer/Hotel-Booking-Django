from django.urls import path

from .views import (
    contact_page,
    gallery_page,
    home_page,
    room_detail,
    rooms_page,
)

app_name = "hotels"

urlpatterns = [
    path("", home_page, name="home"),
    path("rooms/", rooms_page, name="rooms"),
    path("room/<int:pk>/", room_detail, name="room_detail"),
    path("gallery/", gallery_page, name="gallery"),
    path("contact/", contact_page, name="contact"),
]
