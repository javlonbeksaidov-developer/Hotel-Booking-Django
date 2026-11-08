from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date

from hotels.models import Room

from .email import send_html_email
from .models import Booking


@login_required
def booking_page(request):
    rooms = Room.objects.filter(is_available=True)

    # Detail sahifasidan kelgan xona ID
    selected_room_id = request.GET.get("room", "")

    if request.method == "POST":
        room_id = request.POST.get("room")
        selected_room_id = room_id

        check_in = parse_date(request.POST.get("checkin", ""))
        check_out = parse_date(request.POST.get("checkout", ""))

        try:
            adults = int(request.POST.get("adults", 1))
            children = int(request.POST.get("children", 0))
        except (ValueError, TypeError):
            messages.error(request, "Mehmonlar sonini to'g'ri kiriting.")
            return render(
                request,
                "booking.html",
                {
                    "rooms": rooms,
                    "selected_room_id": selected_room_id,
                },
            )

        guest_name = request.POST.get("name", "").strip()
        guest_email = request.POST.get("email", "").strip()

        # Xonani tekshirish
        try:
            room = Room.objects.get(id=room_id, is_available=True)
        except (Room.DoesNotExist, ValueError, TypeError):
            messages.error(request, "Tanlangan xona mavjud emas.")
            return render(
                request,
                "booking.html",
                {
                    "rooms": rooms,
                    "selected_room_id": selected_room_id,
                },
            )

        # Sanalarni tekshirish
        if not check_in or not check_out:
            messages.error(request, "Sanalarni to'g'ri kiriting.")

        elif check_in < timezone.localdate():
            messages.error(
                request, "Check-in sanasi bugundan oldin bo'lishi mumkin emas."
            )

        elif check_out <= check_in:
            messages.error(
                request, "Check-out sanasi Check-in sanasidan keyin bo'lishi kerak."
            )

        # Mehmonlar sonini tekshirish
        elif adults < 1 or children < 0:
            messages.error(request, "Mehmonlar soni noto'g'ri.")

        elif adults + children > room.capacity:
            messages.error(request, "Xona mehmonlar soniga mos emas.")

        elif not guest_name or not guest_email:
            messages.error(request, "Ism va email manzilini kiriting.")

        else:
            # Bandlikni tekshirish
            already_booked = Booking.objects.filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in,
                status__in=[
                    Booking.BookingStatus.CONFIRMED,
                    Booking.BookingStatus.CHECKED_IN,
                ],
            ).exists()

            if already_booked:
                messages.error(request, "Ushbu xona tanlangan sanalarda bron qilingan.")

            else:
                nights = (check_out - check_in).days
                total_price = room.price_per_night * nights

                Booking.objects.create(
                    user=request.user,
                    room=room,
                    check_in=check_in,
                    check_out=check_out,
                    adults=adults,
                    children=children,
                    guest_name=guest_name,
                    guest_email=guest_email,
                    total_price=total_price,
                    status=Booking.BookingStatus.PENDING,
                )

                messages.success(
                    request,
                    "Bron so'rovingiz muvaffaqiyatli yuborildi. Tasdiqlanishini kuting.",
                )

                return redirect("bookings:booking")

    context = {
        "rooms": rooms,
        "selected_room_id": selected_room_id,
    }

    return render(request, "booking.html", context)


@staff_member_required
def booking_send_email(request):
    bookings = Booking.objects.all().order_by("-id")

    context = {
        "bookings": bookings,
        "status_choices": Booking.BookingStatus.choices,
    }

    return render(
        request,
        "email/booking_send_email.html",
        context
    )


@staff_member_required
def update_booking_status(request, booking_id):
    if request.method != "POST":
        return redirect("bookings:booking_send_email")

    booking = get_object_or_404(Booking, id=booking_id)

    new_status = request.POST.get("status")

    # Status qiymatini tekshirish
    if new_status not in Booking.BookingStatus.values:
        messages.error(request, "Noto'g'ri bron holati.")
        return redirect("bookings:booking_send_email")

    # Holat o'zgarmagan bo'lsa, email yubormaymiz
    if booking.status == new_status:
        messages.info(request, "Bron holati o'zgarmagan.")
        return redirect("bookings:booking_send_email")

    # Eski holatni saqlab qolamiz
    old_status = booking.status

    # Yangi holatni saqlash
    booking.status = new_status
    booking.save(update_fields=["status"])

    # Mijozga email yuborish
    email_sent = send_html_email({
        "title": f"Booking #{booking.id} - {booking.get_status_display()}",
        "email": booking.guest_email,
        "booking": booking,
    })

    if email_sent:
        messages.success(
            request,
            f"Bron holati o'zgartirildi: "
            f"{booking.get_status_display()}. Email yuborildi."
        )
    else:
        messages.warning(
            request,
            f"Bron holati o'zgartirildi, lekin email yuborilmadi. "
            f"Eski holat: {old_status}."
        )

    return redirect("bookings:booking_send_email")