from django.contrib import admin
from .models import Hotel, Comment

# Register your models here.
from .models import Hotel, Comment


class HotelAdmin(admin.ModelAdmin):
    list_display = ['city', 'name', 'hid', 'page', 'points', 'points_count']
    search_fields = ['name', 'hid', 'city']


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Comment)
