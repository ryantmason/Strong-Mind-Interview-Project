from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.db import models


class AvailableToppings(models.Model):
    topping_name = models.CharField(max_length=255, default="", null=True)


class PizzaMasterPieces(models.Model):
    pizza_name = models.CharField()
    toppings = ArrayField(
        models.CharField(max_length=50, blank=False),
        size=50,
    ),
