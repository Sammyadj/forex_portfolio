from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(max_digits=9, decimal_places=2, validators=[MaxValueValidator(100000)], default=0.00)

    def __str__(self):
        return f"{self.user.username}'s profile - Balance: GBP {self.balance}"

