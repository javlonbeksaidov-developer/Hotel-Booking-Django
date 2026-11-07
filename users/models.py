from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="Foydalanuvchi")

    avatar = models.ImageField(upload_to="profiles/avatars/", blank=True, null=True, verbose_name="Profil rasmi")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Telefon raqami")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Tug'ilgan sana")
    country = models.CharField(max_length=100, blank=True, verbose_name="Davlat")
    city = models.CharField(max_length=100, blank=True, verbose_name="Shahar")
    bio = models.TextField(blank=True, verbose_name="O'zi haqida")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Foydalanuvchi profili"
        verbose_name_plural = "Foydalanuvchi profillari"
