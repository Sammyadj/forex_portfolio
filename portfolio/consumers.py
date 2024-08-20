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
            if portfolio_data:
                await self.send(json.dumps({
                    'type': 'portfolio.initial',
                    'data': portfolio_data
                }))
            else:
                await self.send(json.dumps({'error': 'No portfolio data available'}))
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
        # Send the updated portfolio data to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'portfolio.update',
            'data': event['data']
        }))

    @database_sync_to_async
    def get_portfolio_data(self):
        from accounts.models import Profile
        from .models import Portfolio
        from trading.models import Trade

        profile = Profile.objects.get(user=self.user)
        try:
            portfolio = Portfolio.objects.get(profile=profile)

            # Calculate the allocation of each asset
            trades = Trade.objects.filter(profile=profile, is_open=True)
            total_equity = portfolio.equity
            allocations = []

            if total_equity > 0:
                asset_summary = {}

                for trade in trades:
                    asset = trade.currency_pair
                    if asset not in asset_summary:
                        asset_summary[asset] = {
                            'volume': 0,
                            'total_value': 0
                        }

                    current_value = trade.volume * trade.instrument.current_price()
                    asset_summary[asset]['volume'] += trade.volume
                    asset_summary[asset]['total_value'] += current_value

                for asset, data in asset_summary.items():
                    allocation_percentage = (data['total_value'] / total_equity) * 100
                    allocations.append({
                        'name': asset,
                        'allocation': allocation_percentage
                    })

            return {
                'balance': float(f"{portfolio.balance:.2f}"),
                'equity': float(f"{total_equity:.2f}"),
                'allocations': allocations  # List of assets with their allocations
            }

        except Portfolio.DoesNotExist:
            print(f"No portfolio found for profile {profile.id}")
            return None
