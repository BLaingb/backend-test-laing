from django.contrib import admin
from .models import Meal, Menu, MealOption

# Register your models here.
admin.site.register(MealOption)
admin.site.register(Menu)
admin.site.register(Meal)
