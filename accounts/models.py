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
    realized_pl = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))

    def unrealized_pl(self):
        trades = self.trades.filter(is_open=True)
        unrealized_pl = Decimal(0)
        for trade in trades:
            current_price = trade.instrument.current_price()
            if trade.is_open and current_price:
                pip_value = Decimal(10 ** trade.instrument.pip_location)
                unrealized_pl += (Decimal(current_price) - trade.entry_price) * trade.volume * pip_value
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

    def broadcast_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        from trading.models import Trade

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'account_{self.id}',
            {
                'type': 'account_update',
                'data': {
                    'account_id': str(self.id),
                    'balance': f"{self.balance:.2f}",
                    'equity': f"{self.equity():.2f}",
                    'unrealized_pl': f"{self.unrealized_pl():.2f}",
                    'realized_pl': f"{self.realized_pl:.2f}"
                }
            }
        )



