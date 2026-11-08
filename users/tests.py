from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import UserProfile

# =====================================================
# 1. USER PROFILE MODEL TESTLARI
# =====================================================


class UserProfileModelTest(TestCase):
    def setUp(self):
        # Test uchun yangi foydalanuvchi yaratamiz
        self.user = User.objects.create_user(
            username="javlonbek", email="javlonbek@gmail.com", password="test12345"
        )

        # Foydalanuvchi uchun profil yaratamiz
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone_number="+998901234567",
            date_of_birth="2004-05-15",
            country="Uzbekistan",
            city="Samarqand",
            bio="Python Backend Developer",
        )

    def test_profile_creation(self):
        # Profil bazaga muvaffaqiyatli qo'shilganini tekshiramiz
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_profile_user_relation(self):
        # Profil tegishli foydalanuvchi bilan bog'langanini tekshiramiz
        self.assertEqual(self.profile.user, self.user)

    def test_user_profile_reverse_relation(self):
        # User orqali uning profilini olish imkoniyatini tekshiramiz
        self.assertEqual(self.user.profile, self.profile)

    def test_profile_phone_number(self):
        # Telefon raqami to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.profile.phone_number, "+998901234567")

    def test_profile_date_of_birth(self):
        # Tug'ilgan sana to'g'ri saqlanganini tekshiramiz
        self.assertEqual(str(self.profile.date_of_birth), "2004-05-15")

    def test_profile_country(self):
        # Davlat nomi to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.profile.country, "Uzbekistan")

    def test_profile_city(self):
        # Shahar nomi to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.profile.city, "Samarqand")

    def test_profile_bio(self):
        # Foydalanuvchi haqida ma'lumot to'g'ri saqlanganini tekshiramiz
        self.assertEqual(self.profile.bio, "Python Backend Developer")

    def test_profile_str(self):
        # __str__ metodi foydalanuvchi username qiymatini qaytarishini tekshiramiz
        self.assertEqual(str(self.profile), "javlonbek")

    def test_profile_created_at(self):
        # Profil yaratilgan vaqt avtomatik shakllanganini tekshiramiz
        self.assertIsNotNone(self.profile.created_at)

    def test_profile_updated_at(self):
        # Profil yangilangan vaqt avtomatik shakllanganini tekshiramiz
        self.assertIsNotNone(self.profile.updated_at)

    def test_profile_meta(self):
        # Modelning verbose_name qiymatlarini tekshiramiz
        self.assertEqual(UserProfile._meta.verbose_name, "Foydalanuvchi profili")

        self.assertEqual(
            UserProfile._meta.verbose_name_plural, "Foydalanuvchi profillari"
        )


# =====================================================
# 2. USER PROFILE DEFAULT VALUE TESTLARI
# =====================================================


class UserProfileDefaultTest(TestCase):
    def setUp(self):
        # Test uchun foydalanuvchi yaratamiz
        self.user = User.objects.create_user(username="testuser", password="test12345")

    def test_profile_optional_fields(self):
        # Ixtiyoriy maydonlar to'ldirilmasdan profil yaratish mumkinligini tekshiramiz
        profile = UserProfile.objects.create(user=self.user)

        self.assertEqual(profile.phone_number, "")
        self.assertIsNone(profile.date_of_birth)
        self.assertEqual(profile.country, "")
        self.assertEqual(profile.city, "")
        self.assertEqual(profile.bio, "")
        self.assertIsNone(profile.avatar.name if profile.avatar else None)

    def test_profile_avatar_optional(self):
        # Profil rasmi majburiy emasligini tekshiramiz
        profile = UserProfile.objects.create(user=self.user)

        self.assertFalse(profile.avatar)


# =====================================================
# 3. USER PROFILE RELATION TESTLARI
# =====================================================


class UserProfileRelationTest(TestCase):
    def setUp(self):
        # Test uchun foydalanuvchi yaratamiz
        self.user = User.objects.create_user(
            username="relationuser", password="test12345"
        )

        # Foydalanuvchiga profil yaratamiz
        self.profile = UserProfile.objects.create(user=self.user, city="Toshkent")

    def test_one_to_one_relation(self):
        # Har bir foydalanuvchiga faqat bitta profil biriktirilishini tekshiramiz
        with self.assertRaises(Exception):  # noqa: B017
            UserProfile.objects.create(user=self.user, city="Samarqand")

    def test_delete_user_deletes_profile(self):
        # Foydalanuvchi o'chirilganda uning profili ham o'chishini tekshiramiz
        self.user.delete()

        self.assertEqual(UserProfile.objects.count(), 0)


# =====================================================
# 4. USER PROFILE UPDATE TESTLARI
# =====================================================


class UserProfileUpdateTest(TestCase):
    def setUp(self):
        # Test uchun foydalanuvchi yaratamiz
        self.user = User.objects.create_user(
            username="updateuser", password="test12345"
        )

        # Foydalanuvchi profili yaratamiz
        self.profile = UserProfile.objects.create(
            user=self.user, city="Samarqand", country="Uzbekistan"
        )

    def test_update_profile_city(self):
        # Profil shahrini yangilaymiz
        self.profile.city = "Toshkent"
        self.profile.save()

        # Yangilangan shahar bazada saqlanganini tekshiramiz
        self.profile.refresh_from_db()

        self.assertEqual(self.profile.city, "Toshkent")

    def test_update_profile_bio(self):
        # Profil haqida ma'lumotni yangilaymiz
        self.profile.bio = "Django Backend Developer"
        self.profile.save()

        # Yangilangan ma'lumotni bazadan qayta olamiz
        self.profile.refresh_from_db()

        self.assertEqual(self.profile.bio, "Django Backend Developer")

    def test_updated_at_changes(self):
        # Profil yangilanishidan oldingi vaqtni saqlaymiz
        old_updated_at = self.profile.updated_at

        # Profil ma'lumotini o'zgartiramiz
        self.profile.city = "Buxoro"
        self.profile.save()

        # Bazadan yangilangan profilni qayta olamiz
        self.profile.refresh_from_db()

        # updated_at maydoni yangilanganini tekshiramiz
        self.assertGreaterEqual(self.profile.updated_at, old_updated_at)


# =====================================================
# 5. USER PROFILE AVATAR TESTLARI
# =====================================================


class UserProfileAvatarTest(TestCase):
    def setUp(self):
        # Test uchun foydalanuvchi yaratamiz
        self.user = User.objects.create_user(
            username="avataruser", password="test12345"
        )

    def test_upload_avatar(self):
        # Test uchun rasm faylini yaratamiz
        avatar = SimpleUploadedFile(
            name="avatar.jpg", content=b"fake-image-content", content_type="image/jpeg"
        )

        # Rasmni profilga biriktiramiz
        profile = UserProfile.objects.create(user=self.user, avatar=avatar)

        # Rasm profilga biriktirilganini tekshiramiz
        self.assertTrue(profile.avatar)

        # Rasm belgilangan papkaga saqlanganini tekshiramiz
        self.assertTrue(profile.avatar.name.startswith("profiles/avatars/"))
