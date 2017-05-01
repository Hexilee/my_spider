from django.db import models


# Create your models here.
class Hotel(models.Model):
    city = models.CharField(max_length=20)
    hid = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    page = models.IntegerField()
    points = models.FloatField()
    start_price = models.IntegerField()
    comments_count = models.IntegerField()
    noise = models.IntegerField(default=0)
    air_quality = models.IntegerField(default=0)
    light = models.IntegerField(default=0)
    temperature = models.IntegerField(default=0)
    traffic = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __str__(self):
        return '[%s]%s' % (self.city, self.name)


class Comment(models.Model):
    hotel = models.CharField(max_length=10)
    page = models.IntegerField()
    name = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20)
    points = models.FloatField()
    content = models.CharField(max_length=1000)

