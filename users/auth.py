from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import UserProfile


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request=request, username=username, password=password)
        if user is None:
            messages.error(request, message="Username or password is wrong !")
            return redirect("users:login")

        login(request=request, user=user)
        return redirect("users:profile")

    return render(request, "auth/login.html")


def logout_page(request):
    logout(request)
    return redirect("users:login")


def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        user.save()

        if user:
            return redirect("users:login")

    return render(request, "auth/register.html")


@login_required
def profile_page(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)  # noqa: RUF059

    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name", "").strip()
        request.user.last_name = request.POST.get("last_name", "").strip()
        request.user.email = request.POST.get("email", "").strip()

        request.user.save()

        profile.phone_number = request.POST.get("phone_number", "").strip()
        profile.country = request.POST.get("country", "").strip()
        profile.city = request.POST.get("city", "").strip()
        profile.bio = request.POST.get("bio", "").strip()

        date_of_birth = request.POST.get("date_of_birth")

        profile.date_of_birth = date_of_birth or None

        if request.FILES.get("avatar"):
            profile.avatar = request.FILES["avatar"]

        profile.save()

        messages.success(request, "Profil muvaffaqiyatli yangilandi!")

        return redirect("users:profile")

    return render(
        request,
        "auth/profile.html",
        {
            "user": request.user,
            "profile": profile,
        },
    )
