from django.contrib.auth.models import User
from django.db import models

from hotels.models import Room


class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        PENDING = "PENDING", "Kutilmoqda"
        CONFIRMED = "CONFIRMED", "Tasdiqlangan"
        CHECKED_IN = "CHECKED_IN", "Joylashgan"
        CHECKED_OUT = "CHECKED_OUT", "Chiqib ketgan"
        CANCELLED = "CANCELLED", "Bekor qilingan"
        REJECTED = "REJECTED", "Rad etilgan"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")

    check_in = models.DateField(verbose_name="Kirish sanasi")
    check_out = models.DateField(verbose_name="Chiqish sanasi")

    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)

    guest_name = models.CharField(max_length=150)
    guest_email = models.EmailField()

    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Umumiy narx"
    )

    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
        verbose_name="Bron holati",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    def __str__(self):
        return f"{self.user.username} - {self.room} ({self.check_in} / {self.check_out}) - {self.get_status_display()}"

    class Meta:
        verbose_name = "Bron"
        verbose_name_plural = "Bronlar"
