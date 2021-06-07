from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.base import TemplateView
from .models import Meal, Menu
from .forms import MealForm, MenuForm
from backend_test.utils.slack import send_menu_slack

# Create your views here.
class MenuListView(ListView):
    model = Menu


class MenuCreateView(CreateView):
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy("menu-list")

    def form_valid(self, form: MenuForm):
        if form.cleaned_data["notify_now"]:
            send_menu_slack.delay(form.instance.get_message())
            form.instance.notification_sent_at = timezone.now()
        return super().form_valid(form)


class MealCreateView(CreateView):
    model = Meal
    form_class = MealForm
    success_url = reverse_lazy("meal-success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu = get_object_or_404(Menu, id=self.kwargs["menu"])
        context["date"] = menu.date
        context["form"]["selected_option"].queryset = menu.meal_options
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial["menu"] = get_object_or_404(Menu, id=self.kwargs["menu"])
        return initial


class MealSuccessView(TemplateView):
    template_name = "menu/meal_success.html"
