from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Menu
from .forms import MenuForm

# Create your views here.
class MenuListView(ListView):
    model = Menu


class MenuCreateView(CreateView):
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy('menu-list')
