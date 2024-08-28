from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Portfolio, PortfolioInstrument
from portfolio.consumers import PortfolioConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(post_save, sender=Portfolio)
def broadcast_portfolio_change(sender, instance, **kwargs):
    # Prepare the portfolio data to be sent
    print(f"Signal received for Portfolio ID {instance.id}")
    data = {
        'balance': instance.balance,
        'equity': instance.equity,
        'unrealized_pl': instance.profile.unrealized_pl(),
        'realized_pl': instance.profile.realized_pl,
        'asset_allocations': {
            pi.instrument.display_name: {
                'current_allocation': float(pi.current_allocation),
                'target_allocation': float(pi.target_allocation)
            }
            for pi in PortfolioInstrument.objects.filter(portfolio=instance)
        }
    }

    # Trigger the WebSocket broadcast
    channel_layer = get_channel_layer()
    async_to_sync(PortfolioConsumer.broadcast_portfolio_update)(data)