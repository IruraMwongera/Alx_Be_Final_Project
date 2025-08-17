from django.contrib import admin
from .models import Town, Area, ParkingSection, Vehicle, ParkingTicket

# Inline parking sections inside Area
class ParkingSectionInline(admin.TabularInline):
    model = ParkingSection
    extra = 1  # number of empty rows for quick creation

@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("name", "town")
    list_filter = ("town",)
    search_fields = ("name",)
    inlines = [ParkingSectionInline]  # Admin can create parking sections directly under each area

@admin.register(ParkingSection)
class ParkingSectionAdmin(admin.ModelAdmin):
    list_display = ("name", "area", "capacity", "is_custom")
    list_filter = ("area", "is_custom")
    search_fields = ("name",)
