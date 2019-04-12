from django.contrib import admin

# Register your models here.
from .models import TelegramUser
from .models import Book


admin.site.register(TelegramUser)
admin.site.register(Book)
