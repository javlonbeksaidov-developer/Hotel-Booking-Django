from django.contrib import admin

from .models import Contact, Hotel, Room, RoomImage, RoomVideo, Subscribe

admin.site.register(Hotel)
admin.site.register(Contact)
admin.site.register(Subscribe)


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


class RoomVideoInline(admin.TabularInline):
    model = RoomVideo
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline, RoomVideoInline]  # noqa: RUF012
