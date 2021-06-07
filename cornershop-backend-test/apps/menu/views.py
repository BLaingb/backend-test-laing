from backend_test.envtools import getenv
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView, SingleObjectMixin

from .forms import MealForm, MealOptionForm, MenuForm
from .models import Meal, MealOption, Menu


# Create your views here.
class MealOptionCreateView(CreateView):
    model = MealOption
    form_class = MealOptionForm
    success_url = reverse_lazy("meal-option-create")


class MenuListView(ListView):
    model = Menu


class MenuCreateView(CreateView):
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy("menu-list")

    def form_valid(self, form: MenuForm):
        if form.cleaned_data["notify_now"]:
            form.instance.notify(save=False)
        return super().form_valid(form)


class MenuDetailView(DetailView):
    model = Menu


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


class MenuNotify(View):
    model = Menu
    http_method_names = ["post", "options"]

    def post(self, _, pk):
        menu = get_object_or_404(Menu, id=pk)
        if menu.notification_sent_at:
            time_delta = timezone.now() - menu.notification_sent_at
            min_wait = getenv("NOTIFICATION_WAIT_TIME", default="300", coalesce=int)
            if time_delta.total_seconds() < min_wait:
                return JsonResponse(
                    {
                        "success": False,
                        "message": f"Wait at least {min_wait/60} minutes before sending another nothification",
                    }
                )
        menu.notify()
        return JsonResponse({"success": True, "message": "Notification sent!"})
