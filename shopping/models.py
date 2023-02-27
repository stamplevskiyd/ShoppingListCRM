from django.db import models

import random
import requests
from datetime import date
from bs4 import BeautifulSoup


class User(models.Model):
    """Пользователь"""

    first_name = models.CharField(max_length=50, blank=False, verbose_name='Имя')
    second_name = models.CharField(max_length=50, blank=False, verbose_name='Фамилия')
    register_date = models.DateField(default=date.today(), verbose_name='Дата регистрации')
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона')
    vk_profile_link = models.URLField(max_length=200, blank=True, verbose_name='Профиль в ВК')

    @property
    def full_name(self):
        """Полное имя пользователя"""
        return ' '.join((self.first_name, self.second_name))

    @property
    def format_phone_number(self):
        """Номер телефона в более красивом формате"""
        return self.phone_number

    @property
    def profile_picture_url(self):
        """Парсит страничку ВК и находит ссылку на аватарку"""

        #TODO: Переделать, пока находит только картинки шакального качества

        r = requests.get(self.vk_profile_link)
        soup = BeautifulSoup(r.content, 'html.parser')
        avatars = soup.findAll('div', class_='Avatar__image Avatar__image-1')

        url = avatars[0]["style"].split('\'')[1]
        return url




class Store(models.Model):
    """Магазин"""

    name = models.CharField(max_length=100, blank=True, verbose_name='Название магазина')


class Purchase(models.Model):
    """Покупка"""

    name = models.CharField(max_length=100, blank=True, verbose_name='Название предмета')
    price = models.FloatField(verbose_name='Цена')
    payer = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Кто платил')
    shop = models.OneToOneField(Store, null=True, on_delete=models.SET_NULL, verbose_name='Магазин')
