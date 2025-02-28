from django.db import models


# class PizzaSizes(Enum):
    # SMALL = 'small'
    # MEDIUM = 'medium'
    #

class AvailableToppings(models.Model):
    topping_name = models.CharField(unique=True, max_length=255, default="", null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.topping_name


class PizzaMasterPieces(models.Model):
    pizza_name = models.CharField(unique=True, max_length=255, default="", null=True)
    toppings = models.ManyToManyField(AvailableToppings)

    def __str__(self):
        return self.pizza_name
