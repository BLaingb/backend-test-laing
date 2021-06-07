from django.urls import path
from apps.menu.views import MealCreateView, MealSuccessView, MenuListView, MenuCreateView

urlpatterns = [
    path('', MenuListView.as_view(), name='menu-list'),
    path('create/', MenuCreateView.as_view(), name='menu-create'),
    path('<uuid:menu>/', MealCreateView.as_view(), name='meal-create'),
    path('meal/success/', MealSuccessView.as_view(), name='meal-success'),
]
