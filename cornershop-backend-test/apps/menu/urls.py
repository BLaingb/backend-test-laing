from django.urls import path
from apps.menu.views import (
    MealCreateView,
    MealOptionCreateView,
    MealSuccessView,
    MenuDetailView,
    MenuListView,
    MenuCreateView,
)

urlpatterns = [
    path("", MenuListView.as_view(), name="menu-list"),
    path("create/", MenuCreateView.as_view(), name="menu-create"),
    path("option/create/", MealOptionCreateView.as_view(), name="meal-option-create"),
    path("<uuid:menu>/", MealCreateView.as_view(), name="meal-create"),
    path("<uuid:pk>/detail/", MenuDetailView.as_view(), name="menu-detail"),
    path("meal/success/", MealSuccessView.as_view(), name="meal-success"),
]
