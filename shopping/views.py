from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from shopping import models

import requests
from bs4 import BeautifulSoup


def index_view(request):
    """Главная страница"""

    persons = models.Person.objects.all()
    stores = models.Store.objects.all()

    return render(request, "base.html", context={
        'persons': persons,
        'stores': stores
    })


def user_page_view(request, id):
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
        try:
            url = request.POST["profile_url"]
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')

            """Поиск аватарки пользователя"""
            avatars = soup.findAll('div', class_='Avatar__image Avatar__image-1')
            avatar_url = avatars[0]["style"].split('\'')[1]

            """Поиск имени пользователя"""
            name = soup.title.string.split('|')[0].strip()

            return render(request, "shopping/person_registration/confirm_data.html", context={
                'name': name,
                'picture_url': avatar_url,
                'profile_url': url,
                'found': 'true',
            })
        except:
            #TODO: Это костыль, нужна страница ошибки
            return render(request, "shopping/person_registration/confirm_data.html", context={
                'name': '',
                'picture_url': '',
                'profile_url': '',
                'found': 'false'
            })


def save_person_view(request):
    """Сохранить пользователя после подтверждения данных"""

    person = models.Person()
    person.name = request.POST["name"]
    person.phone_number = request.POST["phone_number"][-10:]
    person.profile_url = request.POST["profile_url"]
    person.profile_picture_url = request.POST["picture_url"]
    person.save()

    return redirect('/')
