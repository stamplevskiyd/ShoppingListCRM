from django.db import models

import random
import requests
from datetime import date
from bs4 import BeautifulSoup


class Person(models.Model):
    """Пользователь"""

    name = models.CharField(max_length=100, blank=False, verbose_name='Имя')
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона')
    register_date = models.DateField(default=date.today(), verbose_name='Дата регистрации')
    profile_url = models.URLField(max_length=250, blank=True, verbose_name='Профиль в ВК')
    profile_picture_url = models.URLField(max_length=250, blank=True, verbose_name='Ссылка на фото профиля')

    @property
    def format_phone_number(self):
        """Номер телефона в более красивом формате"""
        return self.phone_number


class Store(models.Model):
    """Магазин"""

    name = models.CharField(max_length=100, blank=True, verbose_name='Название магазина')


class Purchase(models.Model):
    """Покупка"""

    name = models.CharField(max_length=100, blank=True, verbose_name='Название предмета')
    price = models.FloatField(verbose_name='Цена')
    payer = models.OneToOneField(Person, on_delete=models.CASCADE, verbose_name='Кто платил')
    shop = models.OneToOneField(Store, null=True, on_delete=models.SET_NULL, verbose_name='Магазин')
