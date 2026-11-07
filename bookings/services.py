from django.shortcuts import get_object_or_404

from hotels.models import Room

from .models import Booking


class BookingService:
    @staticmethod
    def create_room_booking(user, room_id, check_in, check_out):
        room = get_object_or_404(Room, pk=room_id)

        nights = (check_out - check_in).days
        total_price = room.price_per_night * nights

        booking = Booking.objects.create(
            user=user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
        )

        return booking
