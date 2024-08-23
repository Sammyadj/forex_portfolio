from decimal import Decimal
from django.db import models
from accounts.models import Profile
from trading.models import Instrument


class AccountHistory(models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    equity = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    unrealized_pl = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    realized_pl = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    asset_allocation = models.JSONField(default=dict)  # Stores allocation like {"EUR/USD": 30.5, "GBP/USD": 20.1, ...}

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.profile.user.username} - {self.timestamp}"


class BotSettings(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    strategy = models.CharField(max_length=50, default='moving_average')
    short_ma_period = models.PositiveIntegerField(default=9)
    long_ma_period = models.PositiveIntegerField(default=26)
    granularity = models.CharField(max_length=10, default='H1')
    prev_short_ma = models.FloatField(null=True, blank=True)
    prev_long_ma = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Bot settings for {self.profile.user.username}"


class Portfolio(models.Model):
    profile = models.OneToOneField(Profile, related_name='portfolio', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    equity = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    instruments = models.ManyToManyField(Instrument, through='PortfolioInstrument')

    def __str__(self):
        return f"Portfolio for {self.profile.user.username}"


class PortfolioInstrument(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='portfolio_instruments', on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    current_allocation = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal(0.00))
    # target_allocation = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('0.00'))
    # min_allocation = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('0.00'))
    # max_allocation = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('1.00'))

    def __str__(self):
        return f"{self.instrument.display_name} in {self.portfolio.profile.user.username}'s Portfolio"
