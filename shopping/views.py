from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from shopping import models

import requests
import re
from bs4 import BeautifulSoup


def index_view(request):
    """Главная страница"""
    persons = models.Person.objects.all()
    stores = models.Store.objects.all()

    return render(request, "base.html", context={
        'persons': persons,
        'stores': stores
    })


def person_page_view(request, id):
    """Личный кабинет пользователя"""
    person = models.Person.objects.get(id=id)
    return render(request, "shopping/person_info.html", context={
        'person': person
    })


def register_person_view(request):
    """Получить данные пользователя из ВК"""
    if request.method == 'GET':
        return render(request, "shopping/person_registration/register.html")
    else:
        url = request.POST["profile_url"]
        data = {
            'name': '',
            'profile_url': url,
            'picture_url': '',
            'found': 'false'
        }
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')

            """Поиск аватарки пользователя"""
            pictures = soup.findAll('div', class_='Avatar__image Avatar__image-1')
            picture_url = pictures[0]["style"].split('\'')[1]
            data['picture_url'] = picture_url

            """Поиск имени пользователя"""
            name = soup.title.string.split('|')[0].strip()
            data['name'] = name
            data['found'] = 'true'
        except:
            pass

        """Возвращаем найденные данные"""
        return render(request, "shopping/person_registration/confirm_data.html", context=data)


def save_person_view(request):
    """Сохранить пользователя после подтверждения данных"""
    phone_number = request.POST["phone_number"][-10:]
    if models.Person.objects.filter(phone_number=phone_number).exists():
        return redirect('/')

    person = models.Person()
    person.name = request.POST["name"]
    person.phone_number = phone_number
    person.profile_url = request.POST["profile_url"]
    person.profile_picture_url = request.POST["picture_url"]
    person.save()

    return redirect('/')


def pay_debts_view(request, id):
    """Оплата долгов"""
    if request.method == 'GET':
        person = models.Person.objects.get(id=id)
        return render(request, "shopping/pay_debts.html", context={
            'debts': person.person_debts
        })
    else:
        person = models.Person.objects.get(id=id)
        debt_ids = [re.sub('debt_payment_', '', elem) for elem in request.POST.keys() if elem.startswith('debt_payment')]
        debts = models.DebtSum.objects.filter(id__in=debt_ids)
        for debt in debts:
            debt.amount = 0
            debt.save()

        return render(request, "shopping/person_info.html", context={
            'person': person
        })


@csrf_exempt
def add_purchase_view(request):
    """Добавить покупки"""
    if request.method == 'GET':
        persons = models.Person.objects.all()
        stores = models.Store.objects.all()

        return render(request, "shopping/add_purchase.html", context={
            'persons': persons,
            'stores': stores
        })

    else:
        print(request.POST)
