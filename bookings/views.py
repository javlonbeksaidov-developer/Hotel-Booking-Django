from django.shortcuts import get_object_or_404, redirect, render

from hotels.models import Room

from .forms import BookingForm
from .models import Booking
from .services import BookingService


def booking_page(request):
    if request.method == "POST":
        room = request.POST.get("room")
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")

        new_booking = Booking.objects.create(
            user = request.user,
            room = room,
            check_in = checkin,
            check_out = checkout
        )
        new_booking.save()

        return redirect("hotels:home")

    return render(request, "booking.html")


def create_booking(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            BookingService.create_room_booking(
                user=request.user,
                room_id=room_id,
                check_in=form.cleaned_data["check_in"],
                check_out=form.cleaned_data["check_out"],
            )

            return redirect("hotels:rooms")

    else:
        form = BookingForm()

    return render(
        request,
        "booking.html",
        {
            "room": room,
            "form": form,
        },
    )