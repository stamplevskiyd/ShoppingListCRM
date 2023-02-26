from django.db import models
from datetime import date
from django.shortcuts import reverse


class User(models.Model):
    """Пользователь"""

    first_name = models.CharField(max_length=50, blank=False, verbose_name='Имя')
    second_name = models.CharField(max_length=50, blank=False, verbose_name='Фамилия')
    register_date = models.DateField(default=date.today(), verbose_name='Дата регистрации')

    @property
    def full_name(self):
        """Полное имя пользователя"""
        return ' '.join((self.first_name, self.second_name))


class Store(models.Model):
    """Магазин"""

    name = models.CharField(max_length=100, blank=True, verbose_name='Название магазина')


class Purchase(models.Model):
    """Покупка"""

    name = models.CharField(max_length=100, blank=True, verbose_name='Название предмета')
    price = models.FloatField(verbose_name='Цена')
    payer = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Кто платил')
    shop = models.OneToOneField(Store, null=True, on_delete=models.SET_NULL, verbose_name='Магазин')
