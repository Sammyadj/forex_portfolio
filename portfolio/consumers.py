import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class PortfolioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.portfolio_group_name = f'portfolio_{self.user.id}'
            await self.channel_layer.group_add(
                self.portfolio_group_name,
                self.channel_name
            )
            await self.accept()

            # Send initial portfolio data
            portfolio_data = await self.get_portfolio_data()
            if not portfolio_data:
                await self.send(json.dumps({'error': 'No portfolio data available'}))

            await self.send(json.dumps({
                'type': 'portfolio.initial',
                'data': portfolio_data
            }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.portfolio_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        pass

    async def portfolio_update(self, event):
        # Send updated portfolio data to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'portfolio.update',
            'data': event['data']
        }))

    @database_sync_to_async
    def get_portfolio_data(self):
        from portfolio.models import Portfolio, PortfolioInstrument
        try:
            portfolio = Portfolio.objects.get(profile__user=self.user)
            portfolio_value = float(portfolio.equity)  # Convert to float
            balance = float(portfolio.balance)
            equity = float(portfolio.equity)
            unrealized_pl = float(portfolio.profile.unrealized_pl())
            realized_pl = float(portfolio.profile.realized_pl)

        # Calculate current asset allocation
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
