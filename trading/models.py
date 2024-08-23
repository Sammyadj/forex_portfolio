from decimal import Decimal
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from trading.api_utils import get_current_price


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
        return self.name

    def current_price(self):
        bid_price, ask_price = get_current_price(self.name)
        current_price = Decimal(bid_price + ask_price) / 2
        # print(current_price)
        return current_price


class Trade(models.Model):
    BUY = 'buy'
    SELL = 'sell'
    TRADE_TYPE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]
    profile = models.ForeignKey(Profile, related_name='trades', on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, related_name='trades', on_delete=models.SET_NULL, null=True)
    instrument = models.ForeignKey(Instrument, related_name='trades', on_delete=models.CASCADE)
    currency_pair = models.CharField(max_length=10)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    entry_price = models.DecimalField(max_digits=10, decimal_places=4)
    exit_price = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    open_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True, blank=True)
    is_open = models.BooleanField(default=True)
    bot = models.BooleanField(default=False)
    take_profit = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPE_CHOICES, null=True, blank=True)

    def close_trade(self, exit_price):
        # Calculate the realized P/L
        exit_price = Decimal(exit_price)
        pip_value = Decimal(10 ** self.instrument.pip_location)
        if self.trade_type == 'buy':
            realized_pl = (exit_price - self.entry_price) * self.volume * pip_value
        elif self.trade_type == 'sell':
            realized_pl = (self.entry_price - exit_price) * self.volume * pip_value
        else:
            return Decimal(0)

        # Update the trade details
        self.exit_price = exit_price
        self.close_date = timezone.now()
        self.is_open = False
        self.save()

        # Update the profile's balance and realized P/L
        self.profile.balance += realized_pl
        self.profile.realized_pl += realized_pl
        self.profile.save()

    def current_value(self):
        """
        Calculate the current market value of the trade based on the current price of the instrument
        and the trade's volume.
        """
        # Get the current price of the instrument
        current_price = self.instrument.current_price()

        # Calculate the market value of the trade
        pip_value = Decimal(10 ** self.instrument.pip_location)
        if self.trade_type == self.BUY:
            value = (current_price - self.entry_price) * self.volume * pip_value
        elif self.trade_type == self.SELL:
            value = (self.entry_price - current_price) * self.volume * pip_value
        else:
            value = Decimal(0)

        return value

    def __str__(self):
        return f'{self.currency_pair} - {self.volume} at {self.entry_price}'
