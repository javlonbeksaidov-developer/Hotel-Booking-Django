from django.urls import path

from .views import booking_page, create_booking

app_name = "bookings"

urlpatterns = [
    path("", booking_page, name="booking"),
    path(
        "create/<int:room_id>/",
        create_booking,
        name="booking_create",
    ),
]