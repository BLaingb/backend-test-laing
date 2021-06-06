from django.urls import path
from apps.menu.views import MenuListView

urlpatterns = [
    path('', MenuListView.as_view())
]
