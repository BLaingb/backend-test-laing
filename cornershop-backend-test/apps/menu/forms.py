from django import forms
from django.utils import timezone
from .models import Menu


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
