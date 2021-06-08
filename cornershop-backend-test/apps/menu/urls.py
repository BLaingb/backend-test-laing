from django.urls import path
from django.contrib.auth.decorators import permission_required
from apps.menu.views import (
    MealCreateView,
    MealOptionCreateView,
    MealSuccessView,
    MenuDetailView,
    MenuListView,
    MenuCreateView,
    MenuNotify,
)

urlpatterns = [
    path("", permission_required('menu.view')(MenuListView.as_view()), name="menu-list"),
    path("create/", permission_required('menu.add')(MenuCreateView.as_view()), name="menu-create"),
    path("option/create/", permission_required('mealoption.add')(MealOptionCreateView.as_view()), name="meal-option-create"),
    path("<uuid:menu>/", MealCreateView.as_view(), name="meal-create"),
    path("<uuid:pk>/detail/", permission_required('menu.view')(MenuDetailView.as_view()), name="menu-detail"),
    path("<uuid:pk>/notify/", permission_required('menu.change')(MenuNotify.as_view()), name="menu-notify"),
    path("meal/success/", MealSuccessView.as_view(), name="meal-success"),
]
