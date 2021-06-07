import uuid
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.sites.models import Site

class ActiveOnlyManager(models.Manager):
    def get_queryset(self):
        return super(ActiveOnlyManager, self).get_queryset().filter(is_active=True)


class MealOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField(max_length=128, blank=True, default="")
    is_active = models.BooleanField(default=True)

    objects = ActiveOnlyManager()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(
        unique=True, null=False, default=timezone.now, help_text="YYYY-MM-DD"
    )
    meal_options = models.ManyToManyField(MealOption, related_name="menus")
    select_by_time = models.TimeField(
        default=datetime.time(11, 00),
        help_text="Up to what time can employees register their meal choice? (HH:MM:SS)",
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"Menu of {self.date}"

    def create_meal_url(self):
        return f"/menu/{self.id}/"

    def get_message(self):
        url = Site.objects.get_current().domain
        url = f"{url}{self.create_meal_url()}"
        return f"Hello! Please select your meal choice for {self.date} at {url}"



class Meal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=False)
    selected_option = models.ForeignKey(
        MealOption, null=False, on_delete=models.PROTECT
    )
    employee = models.CharField(max_length=64, blank=False)
    note = models.TextField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["menu", "employee"], name="unique_meal")
        ]

    def __str__(self) -> str:
        return f"{self.employee}"
