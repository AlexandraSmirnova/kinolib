# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = u'User profiles'


class Film(models.Model):
    f_name = models.CharField(max_length=100, verbose_name=u'Название')
    f_discription = models.TextField(verbose_name=u'Описание')
    f_pub_date = models.DateTimeField(default=now(), verbose_name=u'Дата публикации')
    f_year_creation = models.IntegerField(verbose_name=u'Год создания', default=2000)
    f_rating = models.IntegerField(verbose_name=u'Рейтинг', default=0)
    f_flag = models.NullBooleanField(default=0)

    def __str__(self):
        return self.f_name


class Score(models.Model):
    value = models.IntegerField(default=0)
    voter = models.ForeignKey(User, related_name='score_voter')
    film = models.ForeignKey(Film, related_name='score_film')


class Comment(models.Model):
    author = models.ForeignKey(User)
    c_text = models.TextField(max_length=400)
    c_pub_date = models.DateTimeField(default=now())
    c_flag = models.NullBooleanField(default=0)
    film = models.ForeignKey(Film)

    def __str__(self):
        return self.c_text
