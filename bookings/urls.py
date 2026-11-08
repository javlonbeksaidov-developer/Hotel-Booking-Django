from django.urls import path

from .views import booking_page

app_name = "bookings"

urlpatterns = [
    path("", booking_page, name="booking"),
]