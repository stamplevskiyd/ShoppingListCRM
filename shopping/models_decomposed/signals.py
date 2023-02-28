from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from shopping.models_decomposed.models import *


@receiver(pre_save, sender=DebtSum)
def check_debt_correctness(sender, instance, **kwargs):
    """Не даст создать долг некорректного формата"""
    if not instance.id:
        if instance.first.id >= instance.second.id:
            raise ValueError("id второго больше чем у первого")
        if DebtSum.objects.filter(first_id=instance.first.id, second_id=instance.second.id).exists():
            raise ValueError("Такой долг уже существует")


@receiver(post_save, sender=Person)
def create_debt(sender, instance, created, **kwargs):
    """Добавить записи долгов новому пользователю"""
    if created:
        persons = Person.objects.filter(id_ne=instance.id)
        for person in persons:
            """Долг новому пользователю от остальных"""
            debt = DebtSum()
            debt.person_to = instance
            debt.person_from = person
            debt.save()

            """Долг этого пользователя другим"""
            debt = DebtSum()
            debt.person_to = person
            debt.person_from = instance
            debt.save()


@receiver(post_save, sender=Payment)
def update_debt(sender, instance, created, **kwargs):
    if created:
        if instance.person_from.id < instance.person_to.id:
            first = instance.person_from
            second = instance.person_to
            amount = instance.amount
        else:
            first = instance.person_to
            second = instance.person_from
            amount = -instance.amount
        debt = DebtSum.objects.get(first=first, second=second)
        debt.amount -= amount
        debt.save()
