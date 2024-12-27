from enum import unique

from django.db import models


class Heroes(models.Model):
    name = models.CharField(max_length=100)
    hero_id = models.IntegerField(default=0)
    icon = models.FileField(upload_to='images/', verbose_name='icon')
    pro_pick = models.IntegerField(default=0)
    pro_win = models.IntegerField(default=0)
    pro_lose = models.IntegerField(default=0)
    base_health = models.IntegerField(default=0)
    base_health_regen = models.IntegerField(default=0)
    base_mana = models.IntegerField(default=0)
    base_mana_regen = models.IntegerField(default=0)
    base_armor = models.IntegerField(default=0)
    base_mr = models.IntegerField(default=0)
    base_attack_min = models.IntegerField(default=0)
    base_attack_max = models.IntegerField(default=0)
    base_str = models.IntegerField(default=0)
    base_agi = models.IntegerField(default=0)
    base_int = models.IntegerField(default=0)
    str_gain = models.IntegerField(default=0)
    agi_gain = models.IntegerField(default=0)
    int_gain = models.IntegerField(default=0)
    attack_range = models.IntegerField(default=0)
    projectile_speed = models.IntegerField(default=0)
    attack_rate = models.IntegerField(default=0)
    base_attack_time = models.IntegerField(default=0)
    attack_point = models.IntegerField(default=0)
    move_speed = models.IntegerField(default=0)
    day_vision = models.IntegerField(default=0)
    night_vision = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Heroes"


class Teams(models.Model):
    logo = models.FileField(upload_to='images/', verbose_name='logo', blank=True)
    name = models.CharField(max_length=100, unique=True)
    team_id = models.IntegerField(default=0, unique=True)
    rating = models.FloatField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_players(self):
        return self.players.all()

    class Meta:
        verbose_name_plural = "Teams"


class Players(models.Model):
    name = models.CharField(max_length=100, unique=True)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='players', blank=True, null=True, default=None) # Связь один-ко-многим
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Players"








