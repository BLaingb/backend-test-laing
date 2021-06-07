from django import forms
from .models import Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["date", "meal_options", "select_by_time", "notify_now"]

    # TODO: Enable when slack functionality is developed
    notify_now = forms.BooleanField(
        label="Send slack message now?", initial=False, required=False, disabled=True
    )
