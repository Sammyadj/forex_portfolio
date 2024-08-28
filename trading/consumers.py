from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import json
import asyncio
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
OANDA_STREAM_URL = os.getenv("OANDA_STREAM_URL")


class PriceStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            await self.accept()
            self.heartbeat_task = asyncio.create_task(self.send_heartbeat())
            await self.channel_layer.group_add("pricing_groups", self.channel_name)

    async def disconnect(self, close_code):
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
        await self.channel_layer.group_discard("pricing_groups", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        # print('Text data received: ', text_data_json)
        instruments_received = text_data_json.get('instruments', [])
        if instruments_received:
            asyncio.get_event_loop().create_task(self.stream_prices(instruments_received))

    async def send_heartbeat(self):
        while True:
            try:
                await self.send(json.dumps({'type': 'heartbeat'}))
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                break

    async def stream_prices(self, instruments):
        url = f"{OANDA_STREAM_URL}/accounts/{ACCOUNT_ID}/pricing/stream"
        params = {'instruments': ','.join(instruments)}
        headers = {'Content-type': "application/octet-stream",
                   'Accept-Datetime-Format': "RFC3339",
                   'Authorization': f"Bearer {API_KEY}"}
        with requests.Session() as session:
            response = session.get(url, headers=headers, params=params, stream=True)
            for line in response.iter_lines():
                if line:
                    decoded_line = json.loads(line.decode('utf-8'))
                    await self.channel_layer.group_send(
                        "pricing_groups",
                        {
                            "type": "price.update",
                            "message": decoded_line
                        }
                    )
                    # print(decoded_line)

    async def price_update(self, event):
        # print('Price update received...')
        message = event['message']
        await self.send(text_data=json.dumps(message))


# CONSUMER FOR STREAMING ACCOUNTS INFORMATION
class AccountInfoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.profile = await self.get_profile(self.scope["user"].id)
            self.account_group_name = f'account_{self.profile.id}'

            # Join the group for account updates
            await self.channel_layer.group_add(
                self.account_group_name,
                self.channel_name
            )

            await self.accept()

            # Send the initial account info when the connection is established
            await self.send_account_info()
        else:
            print(f"Connection refused: User is not authenticated. User ID: {self.scope['user'].id}")
            await self.close()

    async def disconnect(self, close_code):
        # Leave the group on disconnect
        print(f"WebSocket disconnected with close code: {close_code}")
        await self.channel_layer.group_discard(
            self.account_group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        if content.get('command') == 'get_account_info':
            await self.send_account_info()

    @database_sync_to_async
    def get_profile(self, user_id):
        from accounts.models import Profile
        return Profile.objects.get(user__id=user_id)

    async def send_account_info(self):
        account_info = await self.get_account_info()

        account_info['balance'] = float(account_info['balance'])
        account_info['equity'] = float(account_info['equity'])
        account_info['unrealized_pl'] = float(account_info['unrealized_pl'])
        account_info['realized_pl'] = float(account_info['realized_pl'])
        await self.send_json(account_info)

    @database_sync_to_async
    def get_account_info(self):
        return {
            'account_id': str(self.profile.id),
            'balance': float(f"{self.profile.balance}"),
            'equity': float(f"{self.profile.equity():4f}"),
            'unrealized_pl': float(f"{self.profile.unrealized_pl():4f}"),
            'realized_pl': float(f"{self.profile.realized_pl}")
        }

    async def broadcast_account_update(self):
        # Fetch the updated account information
        account_info = await self.get_account_info()
        # Send the updated information to all clients in the group
        await self.channel_layer.group_send(
            self.account_group_name,
            {
                'type': 'account.update',
                'data': account_info
            }
        )

    async def account_update(self, event):
        # Send updated account information to WebSocket
        await self.send_json(event['data'])


# CONSUMER FOR STREAMING TRADE UPDATES
class TradeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.profile = await self.get_profile(self.scope["user"].id)
            # self.heartbeat_task = asyncio.create_task(self.send_heartbeat())
            await self.accept()

            # Fetch existing trades asynchronously
            trades = await self.get_trades(self.profile.id)
            if trades:
                for trade in trades:
                    await self.send_trade_update(trade)

            # Now that the connection is established, you can subscribe to future trade updates
            await self.channel_layer.group_add("trade_updates", self.channel_name)
        else:
            print("User is not authenticated.")
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("trade_updates", self.channel_name)

    async def receive_json(self, content):
        command = content.get("command", "")
        print('command received: ', command)
        try:
            if command == "execute_trade":
                trade_data = content.get("trade")
                await self.handle_execute_trade(trade_data)
            elif command == "close_trade":
                trade_data = content.get("trade")
                await self.handle_close_trade(trade_data)
        except Exception as e:
            print(f"Error processing {command}: {e}")
            await self.send_json({'error': str(e)})

    # async def send_heartbeat(self):
    #     while True:
    #         try:
    #             await self.send(json.dumps({'type': 'heartbeat'}))
    #             await asyncio.sleep(30)
    #         except asyncio.CancelledError:
    #             break

    async def handle_execute_trade(self, trade_data):
        profile = await self.get_profile(trade_data['profile_id'])
        instrument = await self.get_instrument(trade_data['instrument'])

        trade = await self.create_trade(
            profile=profile,
            instrument=instrument,
            currency_pair=trade_data['instrument'],
            volume=trade_data.get('volume', 1),
            entry_price=trade_data['price'],
            trade_type=trade_data['type']
        )

        await self.channel_layer.group_send(
            "trade_updates",
            {"type": "trade.update", "trade": self.trade_to_dict(trade)}
        )

        # Broadcast the account update after the trade is executed
        await self.broadcast_account_update(profile.id)

    async def handle_close_trade(self, trade_data):
        trade = await self.get_trade(trade_data['trade_id'])
        await self.close_trade(trade, trade_data['exit_price'])

        await self.channel_layer.group_send(
            "trade_updates",
            {"type": "trade.update", "trade": self.trade_to_dict(trade)}
        )

        await self.broadcast_account_update(trade.profile.id)

    async def broadcast_account_update(self, profile_id):
        channel_layer = get_channel_layer()
        account_group_name = f'account_{profile_id}'

        # Send an account update to the specific account group
        await channel_layer.group_send(
            account_group_name,
            {
                'type': 'account.update',
                'data': await self.get_account_info(profile_id)
            }
        )

    @sync_to_async
    def get_profile(self, user_id):
        from accounts.models import Profile
        return Profile.objects.get(user__id=user_id)

    @sync_to_async
    def get_trades(self, profile_id):
        from .models import Trade
        return list(Trade.objects.filter(profile_id=profile_id))

    @sync_to_async
    def get_instrument(self, instrument_name):
        from .models import Instrument
        return Instrument.objects.get(display_name=instrument_name)

    @sync_to_async
    def get_trade(self, trade_id):
        from .models import Trade
        return Trade.objects.get(id=trade_id)

    @sync_to_async
    def create_trade(self, profile, instrument, currency_pair, volume, entry_price, trade_type):
        from .models import Trade
        return Trade.objects.create(
            profile=profile,
            instrument=instrument,
            currency_pair=currency_pair,
            volume=volume,
            entry_price=entry_price,
            trade_type=trade_type.lower()
        )

    @sync_to_async
    def close_trade(self, trade, exit_price):
        trade.close_trade(exit_price)

    @sync_to_async
    def get_account_info(self, profile_id):
        from accounts.models import Profile
        profile = Profile.objects.get(id=profile_id)
        return {
            'account_id': str(profile.id),
            'balance': f"{profile.balance}",
            'equity': f"{profile.equity()}",
            'unrealized_pl': f"{profile.unrealized_pl()}",
            'realized_pl': f"{profile.realized_pl()}"
        }

    def trade_to_dict(self, trade):
        return {
            'id': trade.id,
            'currency_pair': trade.currency_pair,
            'volume': str(trade.volume),
            'entry_price': str(trade.entry_price),
            'exit_price': str(trade.exit_price) if trade.exit_price else None,
            'open_date': trade.open_date.isoformat(),
            'close_date': trade.close_date.isoformat() if trade.close_date else None,
            'is_open': trade.is_open,
            'trade_type': trade.trade_type
        }

    async def trade_update(self, event):
        await self.send_json(event)

    async def send_trade_update(self, trade):
        await self.send_json({
            "type": "trade.update",
            "trade": self.trade_to_dict(trade)
        })

