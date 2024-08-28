import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer


class PortfolioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                "portfolio_group",
                self.channel_name
            )
            await self.accept()

            portfolio_data = await self.get_portfolio_data()
            if portfolio_data is None:
                await self.send(json.dumps({'type': 'portfolio.initial', 'error': 'No portfolio data available'}))
            else:
                await self.send(json.dumps({
                    'type': 'portfolio.initial',
                    'data': portfolio_data
                }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                "portfolio_group",
                self.channel_name
            )
        print(f"WebSocket disconnected: {close_code}")

    async def receive(self, text_data):
        # Handle incoming WebSocket messages from clients here if needed
        pass

    async def portfolio_update(self, event):
        # This method handles messages sent to the "portfolio_group"
        print(f"Portfolio update received: {event}")
        await self.send(text_data=json.dumps({
            'type': 'portfolio.update',
            'data': event['data']
        }))

    @database_sync_to_async
    def get_portfolio_data(self):
        from portfolio.models import Portfolio, PortfolioInstrument
        try:
            portfolio = Portfolio.objects.get(profile__user=self.user)
            portfolio_value = float(portfolio.equity)
            balance = float(portfolio.balance)
            equity = float(portfolio.equity)
            unrealized_pl = float(portfolio.profile.unrealized_pl())
            realized_pl = float(portfolio.profile.realized_pl)

            asset_allocations = {}
            portfolio_instruments = PortfolioInstrument.objects.filter(portfolio=portfolio)
            for pi in portfolio_instruments:
                asset_allocations[pi.instrument.display_name] = {
                    'current_allocation': float(pi.current_allocation),
                    'target_allocation': float(pi.target_allocation)
                }

            return {
                'balance': balance,
                'equity': equity,
                'unrealized_pl': unrealized_pl,
                'realized_pl': realized_pl,
                'asset_allocations': asset_allocations,
            }
        except Portfolio.DoesNotExist:
            return None

    @classmethod
    async def broadcast_portfolio_update(cls, data):
        print("Broadcasting update to portfolio_group")
        # This method sends updates to all WebSocket clients in the group
        await get_channel_layer().group_send(
            "portfolio_group",
            {
                'type': 'portfolio_update',
                'data': data
            }
        )

