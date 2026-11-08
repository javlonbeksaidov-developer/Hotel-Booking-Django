from django.contrib import messages
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from bookings.models import Booking

from .models import Contact, Room, RoomImage, RoomVideo, Subscribe


def home_page(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()

        if email:
            if Subscribe.objects.filter(email=email).exists():
                messages.warning(request, "Siz allaqachon obuna bo'lgansiz.")
            else:
                Subscribe.objects.create(email=email)
                messages.success(request, "Obunangiz muvaffaqiyatli amalga oshirildi!")

        return redirect("hotels:home")

    return render(request, "index.html")


def about_page(request):
    return render(request, "about.html")


def rooms_page(request):

    today = timezone.localdate()

    active_bookings = Booking.objects.filter(
        room=OuterRef("pk"),
        check_in__lte=today,
        check_out__gt=today,
        status__in=[
            Booking.BookingStatus.CONFIRMED,
            Booking.BookingStatus.CHECKED_IN,
        ],
    )

    rooms = (
        Room.objects.filter(is_available=True)
        .annotate(is_booked_today=Exists(active_bookings))
        .prefetch_related("images")
    )

    room_types = Room.objects.values_list("room_type", flat=True).distinct()

    return render(
        request,
        "rooms.html",
        {
            "rooms": rooms,
            "room_types": room_types,
        },
    )


def room_list(request):
    rooms = Room.objects.prefetch_related("images").all()

    room_types = Room.objects.values_list("room_type", flat=True).distinct()

    return render(
        request,
        "room_list.html",
        {
            "rooms": rooms,
            "room_types": room_types,
        },
    )


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)

    return render(request, "room_detail.html", {"room": room})


def services_page(request):
    return render(request, "services.html")


def gallery_page(request):
    images = RoomImage.objects.select_related("room").all()
    videos = RoomVideo.objects.select_related("room").all()

    context = {
        "images": images,
        "videos": videos,
    }

    return render(request, "gallery.html", context)


def location_page(request):
    return render(request, "location.html")


def contact_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        new_contact = Contact.objects.create(
            name=name, email=email, subject=subject, message=message
        )
        new_contact.save()

        return redirect("hotels:contact")

    return render(request, "contact.html")
