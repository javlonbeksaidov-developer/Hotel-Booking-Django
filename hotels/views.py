from django.shortcuts import render


def home_page(request):
    return render(request, "index.html")


def about_page(request):
    return render(request, "about.html")


def rooms_page(request):
    return render(request, "rooms.html")


def services_page(request):
    return render(request, "services.html")


def gallery_page(request):
    return render(request, "gallery.html")


def location_page(request):
    return render(request, "location.html")


def contact_page(request):
    return render(request, "contact.html")

