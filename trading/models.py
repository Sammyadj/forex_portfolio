from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

from accounts.models import Profile


class Strategy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Instrument(models.Model):
    name = models.CharField(max_length=20, unique=True)
    display_name = models.CharField(max_length=50)
    maximum_order_units = models.BigIntegerField()
    margin_rate = models.CharField(max_length=20)
    minimum_trade_size = models.CharField(max_length=20)
    pip_location = models.IntegerField()
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.display_name


class Trade(models.Model):
    profile = models.ForeignKey(Profile, related_name='trades', on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, related_name='trades', on_delete=models.SET_NULL, null=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)  # Add this line
    currency_pair = models.CharField(max_length=10)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    entry_price = models.DecimalField(max_digits=10, decimal_places=4)
    exit_price = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    open_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True, blank=True)
    is_open = models.BooleanField(default=True)

    def close_trade(self, exit_price):
        self.exit_price = exit_price
        self.close_date = timezone.now()
        self.is_open = False
        self.save()
