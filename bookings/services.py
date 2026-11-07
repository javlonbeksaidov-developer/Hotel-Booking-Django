from django.db import transaction
from django.shortcuts import get_object_or_404

from hotels.models import Room

from .models import Booking


class BookingService:
    """
    Mehmonxona xonalarini bron qilish va tegishli biznes-mantiq amallarini
    boshqarish uchun mo'ljallangan xizmatlar qatlami (Service Layer).
    """

    @staticmethod
    @transaction.atomic     # Tranzaksiyalar atomiyligini ta'minlash dekoratori
    def create_room_booking(user, room_id, check_in, check_out):
        """
        Berilgan foydalanuvchi va xona ma'lumotlari asosida yangi bron yaratadi
        hamda xona holatini band qilib yangilaydi.

        Texnik tavsif:
            - Metod turi: Static method
            - Transaksiya: Xona mavjudligi tekshiriladi va bron yaratilib, xona band qilinadi.

        Args:
            user (User): Bronni amalga oshirayotgan foydalanuvchi obyekti.
            room_id (int): Bron qilinayotgan xonaning unikal identifikatori (ID).
            check_in (str/date): Mehmonxonaga kirish sanasi (Check-in).
            check_out (str/date): Mehmonxonadan chiqish sanasi (Check-out).

        Returns:
            Booking: Muvaffaqiyatli yaratilgan bron (*Booking*) ma'lumotlar bazasi obyekti.

        Raises:
            Http404: Agar ko'rsatilgan ID bo'yicha xona topilmasa.
        """
        room = get_object_or_404(Room, pk=room_id)

        nights = (check_out - check_in).days
        total_price = room.price_per_night * nights

        # Bron obyektini yaratish
        booking = Booking.objects.create(
            user=user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
        )

        # Xona holatini band qilishga o'zgartirish
        room.is_available = False
        room.save()

        return booking
