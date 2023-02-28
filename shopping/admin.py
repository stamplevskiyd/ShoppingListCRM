from django.contrib import admin
from .models import *

admin.site.register(Person)
admin.site.register(Store)
admin.site.register(Purchase)

admin.site.register(Payment)
admin.site.register(DebtSum)
