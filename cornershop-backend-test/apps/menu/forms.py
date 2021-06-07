from django import forms
from django.forms import widgets
from django.utils import timezone
from .models import Menu, Meal


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["date", "meal_options", "select_by_time", "notify_now"]

    notify_now = forms.BooleanField(
        label="Send slack message now?", initial=False, required=False
    )

    def clean_date(self):
        data = self.cleaned_data["date"]
        if data < timezone.now().date():
            raise forms.ValidationError("Date cannot be in the past!")
        return data


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["employee", "menu", "selected_option", "note"]
        widgets = {"menu": widgets.HiddenInput()}

    def clean_selected_option(self):
        menu = self.cleaned_data["menu"]
        selected_option = self.cleaned_data["selected_option"]
        if selected_option not in menu.meal_options:
            raise forms.ValidationError("This option is not available!")
        return selected_option
