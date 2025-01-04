from enum import unique

from django.db import models


class Heroes(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hero_id = models.IntegerField(default=0, unique=True)
    icon = models.FileField(upload_to='images/', verbose_name='icon')
    pro_pick = models.IntegerField(default=0, blank=True, null=True,)
    pro_win = models.IntegerField(default=0, blank=True, null=True,)
    pro_lose = models.IntegerField(default=0, blank=True, null=True,)
    base_health = models.FloatField(default=0, blank=True, null=True,)
    base_health_regen = models.FloatField(default=0, blank=True, null=True,)
    base_mana = models.FloatField(default=0, blank=True, null=True,)
    base_mana_regen = models.FloatField(default=0, blank=True, null=True,)
    base_armor = models.FloatField(default=0, blank=True, null=True,)
    base_mr = models.FloatField(default=0, blank=True, null=True,)
    base_attack_min = models.FloatField(default=0, blank=True, null=True,)
    base_attack_max = models.FloatField(default=0, blank=True, null=True,)
    base_str = models.FloatField(default=0, blank=True, null=True,)
    base_agi = models.FloatField(default=0, blank=True, null=True,)
    base_int = models.FloatField(default=0, blank=True, null=True,)
    str_gain = models.FloatField(default=0, blank=True, null=True,)
    agi_gain = models.FloatField(default=0, blank=True, null=True,)
    int_gain = models.FloatField(default=0, blank=True, null=True,)
    attack_range = models.FloatField(default=0, blank=True, null=True,)
    projectile_speed = models.FloatField(default=0, blank=True, null=True,)
    attack_rate = models.FloatField(default=0, blank=True, null=True,)
    base_attack_time = models.FloatField(default=0, blank=True, null=True,)
    attack_point = models.FloatField(default=0, blank=True, null=True,)
    move_speed = models.FloatField(default=0, blank=True, null=True,)
    day_vision = models.FloatField(default=0, blank=True, null=True,)
    night_vision = models.FloatField(default=0, blank=True, null=True,)

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
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='players', blank=True, null=True, default=None)
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Players"








