from django.db import models


class Heroes(models.Model):
    name = models.CharField(max_length=100)
    hero_id = models.IntegerField(default=0)
    icon = models.FileField(upload_to='images/', verbose_name='icon')
    pro_pick = models.IntegerField(default=0)
    pro_win = models.IntegerField(default=0)
    pro_lose = models.IntegerField(default=0)


    def __str__(self):
        return self.name
