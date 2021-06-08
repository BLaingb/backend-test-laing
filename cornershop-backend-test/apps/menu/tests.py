from datetime import datetime, timedelta
from django.test import TestCase, Client
from .models import Meal, MealOption, Menu
from django.urls import reverse_lazy
import random

# python manage.py test apps.menu.tests
class MealCreateTestCase(TestCase):
    def setUp(self):
        meal_options = MealOption.objects.bulk_create(
            [
                MealOption(name="Corn pie, Salad and Dessert"),
                MealOption(name="Chicken Nugget Rice, Salad and Dessert"),
                MealOption(name="Rice with hamburger, Salad and Dessert"),
                MealOption(name="Premium chicken Salad and Dessert"),
            ]
        )
        today = datetime.now()
        tomorrow = today + timedelta(days=1)

        menu = Menu.objects.create(
            date=today.date()
        )
        menu.meal_options.set(random.sample(meal_options, 2))
        menu.save()
        
        menu = Menu.objects.create(
            date=tomorrow.date()
        )
        menu.meal_options.set(random.sample(meal_options, 2))
        menu.save()

    def test_can_create_meal(self):
        c = Client()
        menu = Menu.objects.all().first()
        option = random.choice(menu.meal_options.all())
        name = 'Bernardo Laing'
        note = 'No pickles'
        data = {
            'menu': menu.id,
            'selected_option': option.id,
            'employee': name,
            'note': note
        }
        response = c.post(reverse_lazy('meal-create', args=[menu.id]), data)
        self.assertEqual(response.status_code, 302)
        meal = Meal.objects.get(menu=menu, employee=name)
        self.assertEquals(meal.note, note)

    def test_cannot_create_duplicate_meal(self):
        c = Client()
        menu = Menu.objects.all().first()
        option = random.choice(menu.meal_options.all())
        name = 'Bernardo Laing'
        note = 'No pickles'
        Meal.objects.create(menu=menu, selected_option=option, employee=name, note=note)

        data = {
            'menu': menu.id,
            'selected_option': option.id,
            'employee': name,
            'note': note
        }
        c.post(reverse_lazy('meal-create', args=[menu.id]), data)
        meals = Meal.objects.filter(menu=menu, employee=name)
        self.assertEqual(len(meals), 1) # There should only be one meal per menu-employee combination

    def test_cannot_create_with_invalid_option(self):
        c = Client()
        menu = Menu.objects.all().first()
        option = random.choice(MealOption.objects.exclude(menus=menu))
        name = 'Bernardo Laing'
        note = 'No pickles'

        data = {
            'menu': menu.id,
            'selected_option': option.id,
            'employee': name,
            'note': note
        }
        c.post(reverse_lazy('meal-create', args=[menu.id]), data)
        meals = Meal.objects.filter(menu=menu, employee=name)
        self.assertEqual(len(meals), 0) # No meals for menu-employee


