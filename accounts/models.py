# from django.db import models
# from django.conf import settings
# from django.core.validators import MaxValueValidator, MinValueValidator
# from decimal import Decimal

from django.db import models
from django.conf import settings
from decimal import Decimal


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(10000.00))  # Starting balance
    realized_pl = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))  # Realized profit/loss from closed trades

    def unrealized_pl(self):
        from trading.models import Trade
        """Calculate the unrealized profit/loss based on open trades."""
        trades = self.trades.filter(is_open=True)
        unrealized_pl = Decimal(0.00)
        for trade in trades:
            current_price = trade.instrument.current_price()
            pip_value = Decimal(10 ** trade.instrument.pip_location)
            if trade.trade_type == Trade.BUY:
                unrealized_pl += (current_price - trade.entry_price) * trade.volume * pip_value
                # print(f"Unrealized pl for buy {trade.instrument}: {unrealized_pl}")
            elif trade.trade_type == Trade.SELL:
                unrealized_pl += (trade.entry_price - current_price) * trade.volume * pip_value
                # print(f"Unrealized pl for sell {trade.instrument}: {unrealized_pl}")
        return unrealized_pl

    def equity(self):
        """Calculate the total equity, which is the balance plus unrealized P/L."""
        return self.balance + self.unrealized_pl()

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def update_balance(self, amount):
        """Method to update the balance by a specific amount."""
        self.balance += amount
        self.save()

    def update_realized_pl(self, amount):
        """Method to update the realized P/L by a specific amount."""
        self.realized_pl += amount
        self.save()



