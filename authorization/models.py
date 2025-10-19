from django.db import models

from apis.models import App


# Create your models here.
class User(models.Model):
    open_id = models.CharField(max_length=32, unique=True)
    nickName = models.CharField(max_length=256)
    focused_cities = models.TextField(default=[])
    focused_constellations = models.TextField(default=[])
    focused_stocks = models.TextField(default=[])
    menu = models.ManyToManyField(App)

    def __str__(self):
        return '%s' % (self.nickName)

    class Meta:
        indexes = [
            models.Index(fields=['nickName']),
            models.Index(fields=['open_id', 'nickName'])
        ]
