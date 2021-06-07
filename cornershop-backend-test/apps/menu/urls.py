from django.urls import path
from apps.menu.views import MenuListView, MenuCreateView

urlpatterns = [
    path('', MenuListView.as_view(), name='menu-list'),
    path('create/', MenuCreateView.as_view(), name='menu-create'),
]
