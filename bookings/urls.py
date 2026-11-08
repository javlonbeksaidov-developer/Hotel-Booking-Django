from django.urls import path

from .views import booking_page, booking_send_email, update_booking_status

app_name = "bookings"

urlpatterns = [
    path("", booking_page, name="booking"),
    path("send-email/", booking_send_email, name="booking_send_email"),
    path(
        "update-status/<int:booking_id>/",
        update_booking_status,
        name="update_booking_status",
    ),
]
