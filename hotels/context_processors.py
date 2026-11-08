from .models import Hotel


def hotel_context(request=None):
    hotel = Hotel.objects.first()

    return {
        "hotel": hotel,
    }
