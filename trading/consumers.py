from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import requests
from .api_utils import OANDA_STREAM_URL, ACCOUNT_ID, API_KEY


class PriceStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.heartbeat_task = asyncio.create_task(self.send_heartbeat())
        await self.channel_layer.group_add("pricing_groups", self.channel_name)

    async def disconnect(self, close_code):
        print(".........disconnecting from group pricing_groups......")
        await self.channel_layer.group_discard("pricing_groups", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print('Text data recieved: ', text_data_json)
        instruments_received = text_data_json.get('instruments', [])
        if instruments_received:  # Validate or check the instruments list
            print('Instruments received...', instruments_received)
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
                    print('_______________________________________________')

                    await self.channel_layer.group_send(
                        "pricing_groups",
                        {
                            "type": "price.update",
                            "message": decoded_line
                        }
                    )

    # Method for sending messages to WebSocket
    async def price_update(self, event):
        print('Price update received.....')
        message = event['message']
        await self.send(text_data=json.dumps(message))
        print('Price update sent')

