from django.views.generic import ListView
from apps.menu.models import Menu

# Create your views here.
class MenuListView(ListView):
    model = Menu
