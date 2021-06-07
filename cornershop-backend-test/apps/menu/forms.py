from django import forms
from django.forms import widgets
from django.utils import timezone
from .models import MealOption, Menu, Meal


class MealOptionForm(forms.ModelForm):
    class Meta:
        model = MealOption
        fields = ["name", "description"]

    def clean_name(self):
        # Validated here instead of on DB because there could be other instances with the same name, but inactive.
        data = self.cleaned_data["name"]
        if MealOption.objects.filter(name=data).exists():
            raise forms.ValidationError(f"There is already a menu option with name {data}")
        return data


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
