from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from hotels.models import Room

from .services import BookingService


def booking_page(request):
    return render(request, "booking.html")

@login_required
def create_booking(request, room_id):
    room = Room.objects.get(pk=room_id)

    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        BookingService.create_room_booking(
            user=request.user, room_id=room_id, check_in=check_in, check_out=check_out
        )
        return redirect("hotels:rooms")

    return render(request, "booking.html", {"room": room})
