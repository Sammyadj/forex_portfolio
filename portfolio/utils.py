from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def update_portfolio(user):
    channel_layer = get_channel_layer()
    portfolio_data = {
        'balance': user.profile.portfolio.balance,
        'equity': user.profile.portfolio.equity,
        'trades': user.profile.portfolio.trades.count(),
    }
    async_to_sync(channel_layer.group_send)(
        f'portfolio_{user.id}',
        {
            'type': 'portfolio_update',
            'data': portfolio_data
        }
    )