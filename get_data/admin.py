from django.contrib import admin

# Register your models here.
from .models import Hotel, Comment

admin.site.register(Hotel)
admin.site.register(Comment)