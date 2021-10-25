from django.contrib import admin
from holiday.models import Holiday

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    model = Holiday