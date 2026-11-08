from django.contrib.auth.models import User
from django.test import TestCase

from hotels.models import Hotel, Room

from .models import Booking

# =====================================================
# 1. BOOKING MODEL TESTLARI
# =====================================================


class BookingModelTest(TestCase):
    def setUp(self):
        # Test uchun foydalanuvchi yaratamiz
        self.user = User.objects.create_user(
            username="javlonbek", email="javlonbek@gmail.com", password="test12345"
        )

        # Test uchun mehmonxona yaratamiz
        self.hotel = Hotel.objects.create(
            name="Grand Samarkand Hotel",
            description="Zamonaviy mehmonxona",
            address="Registon ko'chasi",
            city="Samarqand",
        )

        # Test uchun xona yaratamiz
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="101",
            name="Deluxe Room",
            price_per_night=250.00,
            capacity=3,
        )

        # Test uchun bron yaratamiz
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in="2026-12-10",
            check_out="2026-12-15",
            adults=2,
            children=1,
            guest_name="Javlonbek Saidov",
            guest_email="javlonbek@gmail.com",
            total_price=1250.00,
        )

    def test_booking_creation(self):
        # Bron bazaga muvaffaqiyatli qo'shilganini tekshiramiz
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_user(self):
        # Bron tegishli foydalanuvchi bilan bog'langanini tekshiramiz
        self.assertEqual(self.booking.user, self.user)

    def test_booking_room(self):
        # Bron tegishli xona bilan bog'langanini tekshiramiz
        self.assertEqual(self.booking.room, self.room)

    def test_booking_check_in(self):
        # Kirish sanasi to'g'ri saqlanganini tekshiramiz
        self.assertEqual(str(self.booking.check_in), "2026-12-10")

    def test_booking_check_out(self):
        # Chiqish sanasi to'g'ri saqlanganini tekshiramiz
        self.assertEqual(str(self.booking.check_out), "2026-12-15")

    def test_booking_adults(self):
        # Kattalar soni to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.booking.adults, 2)

    def test_booking_children(self):
        # Bolalar soni to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.booking.children, 1)

    def test_booking_guest_name(self):
        # Mehmonning ismi to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.booking.guest_name, "Javlonbek Saidov")

    def test_booking_guest_email(self):
        # Mehmonning email manzilini tekshiramiz
        self.assertEqual(self.booking.guest_email, "javlonbek@gmail.com")

    def test_booking_total_price(self):
        # Umumiy bron narxi to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.booking.total_price, 1250.00)

    def test_booking_default_status(self):
        # Yangi bronning standart holati PENDING ekanini tekshiramiz
        self.assertEqual(self.booking.status, Booking.BookingStatus.PENDING)

    def test_booking_created_at(self):
        # Bron yaratilgan vaqt avtomatik shakllanganini tekshiramiz
        self.assertIsNotNone(self.booking.created_at)

    def test_booking_updated_at(self):
        # Bron yangilangan vaqt avtomatik shakllanganini tekshiramiz
        self.assertIsNotNone(self.booking.updated_at)


# =====================================================
# 2. BOOKING STATUS TESTLARI
# =====================================================


class BookingStatusTest(TestCase):
    def setUp(self):
        # Test uchun foydalanuvchi yaratamiz
        self.user = User.objects.create_user(username="testuser", password="test12345")

        # Test uchun mehmonxona yaratamiz
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="Test description",
            address="Test address",
            city="Tashkent",
        )

        # Test uchun xona yaratamiz
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="201",
            name="Standard Room",
            price_per_night=150.00,
        )

        # Test uchun bron yaratamiz
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in="2026-12-10",
            check_out="2026-12-12",
            guest_name="Test User",
            guest_email="test@gmail.com",
            total_price=300.00,
        )

    def test_pending_status(self):
        # Kutilayotgan bron holatini tekshiramiz
        self.assertEqual(self.booking.status, Booking.BookingStatus.PENDING)

    def test_confirmed_status(self):
        # Bron tasdiqlangan holatga o'tishini tekshiramiz
        self.booking.status = Booking.BookingStatus.CONFIRMED
        self.booking.save()

        self.booking.refresh_from_db()

        self.assertEqual(self.booking.status, Booking.BookingStatus.CONFIRMED)

    def test_checked_in_status(self):
        # Mehmon joylashgan holatni tekshiramiz
        self.booking.status = Booking.BookingStatus.CHECKED_IN
        self.booking.save()

        self.assertEqual(self.booking.get_status_display(), "Joylashgan")

    def test_checked_out_status(self):
        # Mehmon chiqib ketgan holatni tekshiramiz
        self.booking.status = Booking.BookingStatus.CHECKED_OUT
        self.booking.save()

        self.assertEqual(self.booking.get_status_display(), "Chiqib ketgan")

    def test_cancelled_status(self):
        # Bron bekor qilingan holatni tekshiramiz
        self.booking.status = Booking.BookingStatus.CANCELLED
        self.booking.save()

        self.assertEqual(self.booking.get_status_display(), "Bekor qilingan")

    def test_rejected_status(self):
        # Bron rad etilgan holatni tekshiramiz
        self.booking.status = Booking.BookingStatus.REJECTED
        self.booking.save()

        self.assertEqual(self.booking.get_status_display(), "Rad etilgan")

    def test_all_booking_statuses(self):
        # Barcha bron holatlari mavjudligini tekshiramiz
        expected_statuses = [
            "PENDING",
            "CONFIRMED",
            "CHECKED_IN",
            "CHECKED_OUT",
            "CANCELLED",
            "REJECTED",
        ]

        actual_statuses = [status[0] for status in Booking.BookingStatus.choices]

        self.assertEqual(actual_statuses, expected_statuses)


# =====================================================
# 3. BOOKING RELATION TESTLARI
# =====================================================


class BookingRelationTest(TestCase):
    def setUp(self):
        # Test uchun foydalanuvchi yaratamiz
        self.user = User.objects.create_user(
            username="relationuser", password="test12345"
        )

        # Test uchun mehmonxona yaratamiz
        self.hotel = Hotel.objects.create(
            name="Relation Hotel",
            description="Description",
            address="Address",
            city="Samarqand",
        )

        # Test uchun xona yaratamiz
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="301",
            name="Family Room",
            price_per_night=300.00,
        )

        # Test uchun bron yaratamiz
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in="2026-12-10",
            check_out="2026-12-12",
            guest_name="Relation User",
            guest_email="relation@gmail.com",
            total_price=600.00,
        )

    def test_user_bookings_relation(self):
        # User orqali uning barcha bronlarini olishni tekshiramiz
        self.assertEqual(self.user.bookings.count(), 1)

    def test_room_bookings_relation(self):
        # Room orqali unga tegishli bronlarni olishni tekshiramiz
        self.assertEqual(self.room.bookings.count(), 1)

    def test_delete_user_deletes_bookings(self):
        # Foydalanuvchi o'chirilganda uning bronlari ham o'chishini tekshiramiz
        self.user.delete()

        self.assertEqual(Booking.objects.count(), 0)

    def test_delete_room_deletes_bookings(self):
        # Xona o'chirilganda unga tegishli bronlar ham o'chishini tekshiramiz
        self.room.delete()

        self.assertEqual(Booking.objects.count(), 0)


# =====================================================
# 4. BOOKING UPDATE TESTLARI
# =====================================================


class BookingUpdateTest(TestCase):
    def setUp(self):
        # Test uchun foydalanuvchi yaratamiz
        self.user = User.objects.create_user(
            username="updateuser", password="test12345"
        )

        # Test uchun mehmonxona yaratamiz
        self.hotel = Hotel.objects.create(
            name="Update Hotel",
            description="Description",
            address="Address",
            city="Tashkent",
        )

        # Test uchun xona yaratamiz
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="401",
            name="Deluxe Room",
            price_per_night=200.00,
        )

        # Test uchun bron yaratamiz
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in="2026-12-10",
            check_out="2026-12-12",
            guest_name="Old Name",
            guest_email="old@gmail.com",
            total_price=400.00,
        )

    def test_update_guest_name(self):
        # Mehmon ismini yangilaymiz
        self.booking.guest_name = "New Name"
        self.booking.save()

        self.booking.refresh_from_db()

        # Yangi ism saqlanganini tekshiramiz
        self.assertEqual(self.booking.guest_name, "New Name")

    def test_update_guest_email(self):
        # Mehmon emailini yangilaymiz
        self.booking.guest_email = "new@gmail.com"
        self.booking.save()

        self.booking.refresh_from_db()

        # Yangi email saqlanganini tekshiramiz
        self.assertEqual(self.booking.guest_email, "new@gmail.com")

    def test_update_booking_price(self):
        # Bron narxini yangilaymiz
        self.booking.total_price = 600.00
        self.booking.save()

        self.booking.refresh_from_db()

        # Yangi narx saqlanganini tekshiramiz
        self.assertEqual(self.booking.total_price, 600.00)

    def test_update_booking_status(self):
        # Bron holatini tasdiqlangan holatga o'tkazamiz
        self.booking.status = Booking.BookingStatus.CONFIRMED
        self.booking.save()

        self.booking.refresh_from_db()

        # Yangi holat saqlanganini tekshiramiz
        self.assertEqual(self.booking.status, Booking.BookingStatus.CONFIRMED)


# =====================================================
# 5. BOOKING STR VA META TESTLARI
# =====================================================


class BookingMetaTest(TestCase):
    def setUp(self):
        # Test uchun foydalanuvchi yaratamiz
        self.user = User.objects.create_user(username="metauser", password="test12345")

        # Test uchun mehmonxona yaratamiz
        self.hotel = Hotel.objects.create(
            name="Meta Hotel",
            description="Description",
            address="Address",
            city="Tashkent",
        )

        # Test uchun xona yaratamiz
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="501",
            name="Single Room",
            price_per_night=100.00,
        )

        # Test uchun bron yaratamiz
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in="2026-12-10",
            check_out="2026-12-12",
            guest_name="Meta User",
            guest_email="meta@gmail.com",
            total_price=200.00,
        )

    def test_booking_str(self):
        # __str__ metodi kerakli ma'lumotlarni qaytarishini tekshiramiz
        expected = f"metauser - {self.room} (2026-12-10 / 2026-12-12) - Kutilmoqda"

        self.assertEqual(str(self.booking), expected)

    def test_booking_meta(self):
        # Booking modelining verbose_name qiymatlarini tekshiramiz
        self.assertEqual(Booking._meta.verbose_name, "Bron")

        self.assertEqual(Booking._meta.verbose_name_plural, "Bronlar")
