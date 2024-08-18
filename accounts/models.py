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

    def unrealized_pl(self):
        trades = self.trades.filter(is_open=True)
        unrealized_pl = Decimal(0)
        for trade in trades:
            current_price = trade.instrument.current_price()
            if trade.is_open and current_price:
                pip_value = Decimal(10 ** trade.instrument.pip_location)
                unrealized_pl += (current_price - trade.entry_price) * trade.volume * pip_value
        return unrealized_pl

    def realized_pl(self):
        trades = self.trades.filter(is_open=False)
        realized_pl = Decimal(0)
        for trade in trades:
            if trade.exit_price:
                pip_value = Decimal(10 ** trade.instrument.pip_location)
                realized_pl += (trade.exit_price - trade.entry_price) * trade.volume * pip_value
        return realized_pl

    def equity(self):
        return self.balance + self.unrealized_pl()

    def __str__(self):
        return f"{self.user.username}'s profile - Balance: GBP {self.balance}"
