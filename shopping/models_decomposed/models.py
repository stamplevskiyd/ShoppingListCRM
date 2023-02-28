from django.db import models
from django.db.models import Q

from datetime import date, datetime


class Person(models.Model):
    """Пользователь"""

    name = models.CharField(max_length=100, blank=False, verbose_name='Имя')
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='Номер телефона')
    register_date = models.DateField(default=date.today(), verbose_name='Дата регистрации')
    profile_url = models.URLField(max_length=250, blank=True, verbose_name='Профиль в ВК')
    profile_picture_url = models.URLField(max_length=250, blank=True, verbose_name='Ссылка на фото профиля')

    def __str__(self):
        return self.name

    @property
    def format_phone_number(self):
        """Номер телефона в более красивом формате"""
        return "+7" + self.phone_number

    @property
    def person_debt_sum(self):
        """Сумма долгов пользователя"""
        first_sum = sum([debt.amount for debt in DebtSum.objects.filter(first=self).filter(amount__gt=0)])
        second_sum = sum([-debt.amount for debt in DebtSum.objects.filter(second=self).filter(amount__lt=0)])
        return first_sum + second_sum

    @property
    def person_debts(self):
        """Список долгов пользователя"""
        first_list = [debt for debt in DebtSum.objects.filter(first=self).filter(amount__gt=0)]

        second_list = [debt for debt in DebtSum.objects.filter(second=self).filter(amount__lt=0)]
        for debt in second_list:
            debt.amount *= -1
        return first_list + second_list

    @property
    def to_person_debt_sum(self):
        """Сумма долгов пользователю"""
        first_sum = sum([-debt.amount for debt in DebtSum.objects.filter(first=self).filter(amount__lt=0)])
        second_sum = sum([debt.amount for debt in DebtSum.objects.filter(second=self).filter(amount__gt=0)])
        return first_sum + second_sum

    @property
    def to_person_debts(self):
        """Список долгов пользователю"""
        first_list = [debt for debt in DebtSum.objects.filter(first=self).filter(amount__lt=0)]
        for debt in first_list:
            debt.amount *= -1

        second_list = [debt for debt in DebtSum.objects.filter(second=self).filter(amount__gt=0)]
        return first_list + second_list


class Payment(models.Model):
    """Оплата покупки/перевод суммы за покупку"""

    amount = models.FloatField(verbose_name='Сумма')
    person_from = models.ForeignKey(Person, related_name='payment_to', verbose_name='Кто перевел', on_delete=models.CASCADE)
    person_to = models.ForeignKey(Person, related_name='payment_from', verbose_name='Кому перевели', on_delete=models.CASCADE)

    def __str__(self):
        return self.person_from.name + '->' + self.person_to.name + ' ' + str(self.amount) + 'р'


class DebtSum(models.Model):
    """Запись про долг одного человека другому"""
    amount = models.FloatField(default=0, verbose_name='Сумма')
    first = models.ForeignKey(Person, related_name='debt_first', verbose_name='Первый пользователь', on_delete=models.CASCADE)
    second = models.ForeignKey(Person, related_name='debt_second', verbose_name='Второй пользователь', on_delete=models.CASCADE)


class Store(models.Model):
    """Магазин"""

    name = models.CharField(max_length=100, blank=True, verbose_name='Название магазина')

    def __str__(self):
        return self.name


class Purchase(models.Model):
    """Покупка"""

    name = models.CharField(max_length=100, blank=True, verbose_name='Название предмета')
    price = models.FloatField(verbose_name='Цена')
    payer = models.ForeignKey(Person, on_delete=models.CASCADE, null=False, verbose_name='Кто платил')
    shop = models.OneToOneField(Store, null=True, on_delete=models.SET_NULL, verbose_name='Магазин')
    added_time = models.DateTimeField(default=datetime.now(), verbose_name='Время добавления')

    def __str__(self):
        return self.name + ' ' + str(self.price)