from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Mehmonxona nomi")
    description = models.TextField(verbose_name="Tavsif")
    address = models.TextField(verbose_name="Manzili")
    city = models.CharField(max_length=100, verbose_name="Shahar")
    country = models.CharField(
        max_length=100, default="Uzbekistan", verbose_name="Davlat"
    )
    stars = models.PositiveSmallIntegerField(default=3, verbose_name="Yulduzlar soni")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Veb-sayt")
    image = models.ImageField(
        upload_to="hotels/", blank=True, null=True, verbose_name="Mehmonxona rasmi"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mehmonxona"
        verbose_name_plural = "Mehmonxonalar"


class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = "SINGLE ROOM", "Bir kishilik xona"
        DOUBLE = "DOUBLE ROOM", "Ikki kishilik xona"
        FAMILY = "FAMILY ROOM", "Family Room"

    class BedType(models.TextChoices):
        SINGLE = "SINGLE BED", "Single Bed"
        DOUBLE = "DOUBLE BED", "Double Bed"
        TWIN = "TWIN BED", "Twin Beds"

    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="rooms", verbose_name="Mehmonxona"
    )
    room_number = models.CharField(max_length=20, verbose_name="Xona raqami")
    name = models.CharField(max_length=150, verbose_name="Xona nomi")
    room_type = models.CharField(
        max_length=20,
        choices=RoomType.choices,
        default=RoomType.DOUBLE,
        verbose_name="Xona turi",
    )
    description = models.TextField(blank=True, verbose_name="Tavsif")
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Bir kechalik narxi"
    )
    capacity = models.PositiveSmallIntegerField(
        default=2, verbose_name="Mehmonlar soni"
    )
    bed_type = models.CharField(
        max_length=20,
        choices=BedType.choices,
        default=BedType.DOUBLE,
        verbose_name="Karavot turi",
    )
    size = models.PositiveSmallIntegerField(
        default=25, verbose_name="Xona maydoni (m²)"
    )
    floor = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Qavat"
    )
    is_available = models.BooleanField(default=True, verbose_name="Mavjudmi?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_number}"

    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"


from django.db import models


class RoomImage(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Xona",
    )

    image = models.ImageField(
        upload_to="rooms/images/",
        verbose_name="Xona rasmi",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} - Image"

    class Meta:
        verbose_name = "Xona rasmi"
        verbose_name_plural = "Xona rasmlari"


class RoomVideo(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name="Xona",
    )

    video = models.FileField(
        upload_to="rooms/videos/",
        verbose_name="Xona videosi",
    )

    title = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Video nomi",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} - Video"

    class Meta:
        verbose_name = "Xona videosi"
        verbose_name_plural = "Xona videolari"


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.subject}."

class Subscribe(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.created_at}."