from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2,
                                  validators=[MinValueValidator(Decimal(100.00)),
                                              MaxValueValidator(Decimal(1000.00))],
                                  default=Decimal(100.00))

    def __str__(self):
        return f"{self.user.username}'s profile - Balance: GBP {self.balance}"
