from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone  # noqa: F401

from .models import (
    Contact,
    Hotel,
    Room,
    RoomImage,
    RoomVideo,
    Subscribe,
)

# =====================================================
# 1. HOTEL MODEL TESTLARI
# =====================================================


class HotelModelTest(TestCase):
    def setUp(self):
        # Har bir test uchun mehmonxona obyektini yaratamiz
        self.hotel = Hotel.objects.create(
            name="Grand Samarkand Hotel",
            description="Zamonaviy va qulay mehmonxona",
            address="Registon ko'chasi, 1",
            city="Samarqand",
            country="Uzbekistan",
            stars=5,
            phone_number="+998901234567",
            email="grandhotel@gmail.com",
            website="https://example.com",
        )

    def test_hotel_creation(self):
        # Mehmonxona bazaga muvaffaqiyatli saqlanganini tekshiramiz
        self.assertEqual(Hotel.objects.count(), 1)

    def test_hotel_name(self):
        # Mehmonxona nomi to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.hotel.name, "Grand Samarkand Hotel")

    def test_hotel_city(self):
        # Shahar nomi to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.hotel.city, "Samarqand")

    def test_hotel_default_country(self):
        # Davlat ko'rsatilmasa, default qiymat Uzbekistan bo'lishini tekshiramiz
        hotel = Hotel.objects.create(
            name="Test Hotel",
            description="Test description",
            address="Test address",
            city="Toshkent",
        )

        self.assertEqual(hotel.country, "Uzbekistan")

    def test_hotel_stars(self):
        # Mehmonxona yulduzlar soni to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.hotel.stars, 5)

    def test_hotel_str(self):
        # __str__ metodi mehmonxona nomini qaytarishini tekshiramiz
        self.assertEqual(str(self.hotel), "Grand Samarkand Hotel")

    def test_hotel_email(self):
        # Email maydoni to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.hotel.email, "grandhotel@gmail.com")

    def test_hotel_created_at(self):
        # Yaratilgan vaqt avtomatik shakllanganini tekshiramiz
        self.assertIsNotNone(self.hotel.created_at)

    def test_hotel_updated_at(self):
        # Yangilangan vaqt avtomatik shakllanganini tekshiramiz
        self.assertIsNotNone(self.hotel.updated_at)

    def test_hotel_meta(self):
        # Modelning verbose_name qiymatlarini tekshiramiz
        self.assertEqual(Hotel._meta.verbose_name, "Mehmonxona")
        self.assertEqual(Hotel._meta.verbose_name_plural, "Mehmonxonalar")


# =====================================================
# 2. ROOM MODEL TESTLARI
# =====================================================


class RoomModelTest(TestCase):
    def setUp(self):
        # Test uchun mehmonxona yaratamiz
        self.hotel = Hotel.objects.create(
            name="Grand Hotel",
            description="Hotel description",
            address="Toshkent",
            city="Toshkent",
        )

        # Test uchun xona yaratamiz
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="101",
            name="Deluxe Room",
            room_type=Room.RoomType.DOUBLE,
            description="Qulay ikki kishilik xona",
            price_per_night=250.00,
            capacity=2,
            bed_type=Room.BedType.DOUBLE,
            size=35,
            floor=2,
            is_available=True,
        )

    def test_room_creation(self):
        # Xona bazaga muvaffaqiyatli qo'shilganini tekshiramiz
        self.assertEqual(Room.objects.count(), 1)

    def test_room_name(self):
        # Xona nomi to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.room.name, "Deluxe Room")

    def test_room_number(self):
        # Xona raqami to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.room.room_number, "101")

    def test_room_price(self):
        # Xonaning bir kechalik narxini tekshiramiz
        self.assertEqual(self.room.price_per_night, 250.00)

    def test_room_capacity(self):
        # Xonadagi maksimal mehmonlar sonini tekshiramiz
        self.assertEqual(self.room.capacity, 2)

    def test_room_type(self):
        # Xona turini tekshiramiz
        self.assertEqual(self.room.room_type, Room.RoomType.DOUBLE)

    def test_room_bed_type(self):
        # Karavot turini tekshiramiz
        self.assertEqual(self.room.bed_type, Room.BedType.DOUBLE)

    def test_room_size(self):
        # Xona maydonini tekshiramiz
        self.assertEqual(self.room.size, 35)

    def test_room_floor(self):
        # Xona joylashgan qavatni tekshiramiz
        self.assertEqual(self.room.floor, 2)

    def test_room_availability(self):
        # Xona mavjudligini tekshiramiz
        self.assertTrue(self.room.is_available)

    def test_room_str(self):
        # __str__ mehmonxona nomi va xona raqamini qaytarishini tekshiramiz
        self.assertEqual(str(self.room), "Grand Hotel - 101")

    def test_room_hotel_relation(self):
        # Xona tegishli mehmonxona bilan bog'langanini tekshiramiz
        self.assertEqual(self.room.hotel, self.hotel)

    def test_hotel_rooms_relation(self):
        # Hotel orqali unga tegishli xonalarni olishni tekshiramiz
        self.assertEqual(self.hotel.rooms.count(), 1)

    def test_room_created_at(self):
        # Xona yaratilgan vaqtini tekshiramiz
        self.assertIsNotNone(self.room.created_at)

    def test_room_updated_at(self):
        # Xona yangilangan vaqtini tekshiramiz
        self.assertIsNotNone(self.room.updated_at)

    def test_room_meta(self):
        # Room modelining nomlarini tekshiramiz
        self.assertEqual(Room._meta.verbose_name, "Xona")
        self.assertEqual(Room._meta.verbose_name_plural, "Xonalar")

    def test_delete_hotel_deletes_rooms(self):
        # Mehmonxona o'chirilganda unga tegishli xonalar ham o'chishini tekshiramiz
        self.hotel.delete()

        self.assertEqual(Room.objects.count(), 0)


# =====================================================
# 3. ROOM IMAGE MODEL TESTLARI
# =====================================================


class RoomImageModelTest(TestCase):
    def setUp(self):
        # Test uchun mehmonxona yaratamiz
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="Description",
            address="Address",
            city="Samarkand",
        )

        # Test uchun xona yaratamiz
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="201",
            name="Standard Room",
            price_per_night=150.00,
        )

        # Test uchun rasm faylini yaratamiz
        self.image = SimpleUploadedFile(
            name="room.jpg",
            content=b"fake-image-content",
            content_type="image/jpeg",
        )

        # Xonaga rasm biriktiramiz
        self.room_image = RoomImage.objects.create(
            room=self.room,
            image=self.image,
        )

    def test_room_image_creation(self):
        # Rasm bazaga muvaffaqiyatli qo'shilganini tekshiramiz
        self.assertEqual(RoomImage.objects.count(), 1)

    def test_room_image_relation(self):
        # Rasm tegishli xona bilan bog'langanini tekshiramiz
        self.assertEqual(self.room_image.room, self.room)

    def test_room_images_reverse_relation(self):
        # Room orqali rasmlarni olish imkoniyatini tekshiramiz
        self.assertEqual(self.room.images.count(), 1)

    def test_room_image_str(self):
        # __str__ metodining natijasini tekshiramiz
        self.assertEqual(str(self.room_image), "Test Hotel - 201 - Image")

    def test_room_image_created_at(self):
        # Rasm yaratilgan vaqtini tekshiramiz
        self.assertIsNotNone(self.room_image.created_at)

    def test_room_image_meta(self):
        # RoomImage modelining nomlarini tekshiramiz
        self.assertEqual(RoomImage._meta.verbose_name, "Xona rasmi")
        self.assertEqual(RoomImage._meta.verbose_name_plural, "Xona rasmlari")

    def test_delete_room_deletes_images(self):
        # Xona o'chirilganda unga tegishli rasmlar ham o'chishini tekshiramiz
        self.room.delete()

        self.assertEqual(RoomImage.objects.count(), 0)


# =====================================================
# 4. ROOM VIDEO MODEL TESTLARI
# =====================================================


class RoomVideoModelTest(TestCase):
    def setUp(self):
        # Test uchun mehmonxona yaratamiz
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="Description",
            address="Address",
            city="Samarkand",
        )

        # Test uchun xona yaratamiz
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="301",
            name="Family Room",
            price_per_night=300.00,
        )

        # Test uchun video faylini yaratamiz
        self.video = SimpleUploadedFile(
            name="room.mp4",
            content=b"fake-video-content",
            content_type="video/mp4",
        )

        # Xonaga video biriktiramiz
        self.room_video = RoomVideo.objects.create(
            room=self.room,
            video=self.video,
            title="Family Room Video",
        )

    def test_room_video_creation(self):
        # Video bazaga muvaffaqiyatli qo'shilganini tekshiramiz
        self.assertEqual(RoomVideo.objects.count(), 1)

    def test_room_video_title(self):
        # Video nomi to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.room_video.title, "Family Room Video")

    def test_room_video_relation(self):
        # Video tegishli xona bilan bog'langanini tekshiramiz
        self.assertEqual(self.room_video.room, self.room)

    def test_room_videos_reverse_relation(self):
        # Room orqali videolarni olish imkoniyatini tekshiramiz
        self.assertEqual(self.room.videos.count(), 1)

    def test_room_video_str(self):
        # __str__ metodining natijasini tekshiramiz
        self.assertEqual(str(self.room_video), "Test Hotel - 301 - Video")

    def test_room_video_created_at(self):
        # Video yaratilgan vaqtini tekshiramiz
        self.assertIsNotNone(self.room_video.created_at)

    def test_room_video_meta(self):
        # RoomVideo modelining nomlarini tekshiramiz
        self.assertEqual(RoomVideo._meta.verbose_name, "Xona videosi")
        self.assertEqual(RoomVideo._meta.verbose_name_plural, "Xona videolari")

    def test_delete_room_deletes_videos(self):
        # Xona o'chirilganda unga tegishli videolar ham o'chishini tekshiramiz
        self.room.delete()

        self.assertEqual(RoomVideo.objects.count(), 0)


# =====================================================
# 5. CONTACT MODEL TESTLARI
# =====================================================


class ContactModelTest(TestCase):
    def setUp(self):
        # Test uchun murojaat obyektini yaratamiz
        self.contact = Contact.objects.create(
            name="Javlonbek",
            email="javlonbek@gmail.com",
            subject="Booking",
            message="I want to book a room.",
        )

    def test_contact_creation(self):
        # Murojaat bazaga muvaffaqiyatli saqlanganini tekshiramiz
        self.assertEqual(Contact.objects.count(), 1)

    def test_contact_name(self):
        # Murojaatchi ismini tekshiramiz
        self.assertEqual(self.contact.name, "Javlonbek")

    def test_contact_email(self):
        # Murojaatchi emailini tekshiramiz
        self.assertEqual(self.contact.email, "javlonbek@gmail.com")

    def test_contact_subject(self):
        # Murojaat mavzusini tekshiramiz
        self.assertEqual(self.contact.subject, "Booking")

    def test_contact_message(self):
        # Murojaat matnini tekshiramiz
        self.assertEqual(self.contact.message, "I want to book a room.")

    def test_contact_str(self):
        # __str__ email va mavzuni qaytarishini tekshiramiz
        self.assertEqual(str(self.contact), "javlonbek@gmail.com - Booking.")

    def test_contact_created_at(self):
        # Murojaat yaratilgan vaqtini tekshiramiz
        self.assertIsNotNone(self.contact.created_at)


# =====================================================
# 6. SUBSCRIBE MODEL TESTLARI
# =====================================================


class SubscribeModelTest(TestCase):
    def setUp(self):
        # Test uchun obuna obyektini yaratamiz
        self.subscribe = Subscribe.objects.create(
            email="subscriber@gmail.com",
        )

    def test_subscribe_creation(self):
        # Obuna bazaga muvaffaqiyatli saqlanganini tekshiramiz
        self.assertEqual(Subscribe.objects.count(), 1)

    def test_subscribe_email(self):
        # Obuna emaili to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.subscribe.email, "subscriber@gmail.com")

    def test_subscribe_str(self):
        # __str__ email va yaratilgan vaqtni qaytarishini tekshiramiz
        expected = f"{self.subscribe.email} - {self.subscribe.created_at}."

        self.assertEqual(str(self.subscribe), expected)

    def test_subscribe_created_at(self):
        # Obuna yaratilgan vaqt avtomatik shakllanganini tekshiramiz
        self.assertIsNotNone(self.subscribe.created_at)

    def test_multiple_subscribers(self):
        # Bir nechta foydalanuvchi obuna bo'lishi mumkinligini tekshiramiz
        Subscribe.objects.create(email="user2@gmail.com")
        Subscribe.objects.create(email="user3@gmail.com")

        self.assertEqual(Subscribe.objects.count(), 3)
