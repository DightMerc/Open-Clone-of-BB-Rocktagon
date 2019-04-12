from django.db import models
from .fields import IntegerRangeField

class TelegramUser(models.Model):
    telegram_id = models.PositiveIntegerField("Telegram ID", default=0, unique=True, null=False)
    full_name = models.CharField("Name", max_length=255, default="", null=False)
    username = models.CharField("Username", max_length=255, default="", null=True)
    phone = models.PositiveIntegerField("Номер телефона", default=0, null=False)

    def __str__(self):
        return str(self.telegram_id)


class Book(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    author = models.CharField("Автор", max_length=511, default="", unique=False, null=False)
    description = models.TextField("Описание")
    published_date = models.PositiveIntegerField(blank=True, null=True)
    rating = IntegerRangeField("Рейтинг",min_value=0, max_value=5)
    
    def __str__(self):
        return str(self.title)