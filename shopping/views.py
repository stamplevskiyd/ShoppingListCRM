from django.shortcuts import render
from django.http import HttpResponse

from shopping import models


def index(request):
    """Главная страница"""

    users = models.User.objects.all()
    stores = models.Store.objects.all()

    print(users)

    return render(request, "base.html", context={
        'users': users,
        'stores': stores
    })


def user_page(request, id):
    """Личный кабинет пользователя"""

    user = models.User.objects.get(id=id)
    return render(request, "shopping/user_profile.html", context={
        'user': user
    })

