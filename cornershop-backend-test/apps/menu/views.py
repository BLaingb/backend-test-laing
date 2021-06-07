from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Menu
from .forms import MenuForm
from backend_test.utils.slack import send_menu_slack

# Create your views here.
class MenuListView(ListView):
    model = Menu


class MenuCreateView(CreateView):
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy('menu-list')

    def form_valid(self, form: MenuForm):
        if form.cleaned_data['notify_now']:
            send_menu_slack.delay(form.instance.get_message())
        return super().form_valid(form)
