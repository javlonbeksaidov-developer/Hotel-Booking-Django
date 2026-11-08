from .models import Hotel


def hotel_context(request):
    hotel = Hotel.objects.first()

    return {
        "hotel": hotel,
    }