from django.contrib import admin

from .models import Package, Hotel


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category", "location", "price", "active", "created_at")
    list_filter = ("category", "active", "created_at")
    search_fields = ("title", "location", "category", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "location", "rating", "price_per_night", "active", "created_at")
    list_filter = ("rating", "active", "created_at")
    search_fields = ("name", "location", "slug")
    prepopulated_fields = {"slug": ("name",)}
