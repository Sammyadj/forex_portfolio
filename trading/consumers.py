from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import requests
from .api_utils import OANDA_STREAM_URL, ACCOUNT_ID, SECURE_HEADER, API_KEY


# import logging
#
# logger = logging.getLogger(__name__)


# class PriceStreamConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add("pricing_group", self.channel_name)
#         await self.accept()
#         print("Connected and added to group, starting price stream...")
#         asyncio.create_task(self.stream_prices())
#
#     async def disconnect(self, close_code):
#         print("........Disconnected from group.......")
#         await self.channel_layer.group_discard("pricing_group", self.channel_name)
#
#     async def receive(self, text_data=None, bytes_data=None):
#         print(f"Received data: {text_data}")
#
#     async def stream_prices(self):
#         url = f"{OANDA_STREAM_URL}/accounts/{ACCOUNT_ID}/pricing/stream"
#         params = {'instruments': 'GBP_USD'}
#         # headers = SECURE_HEADER
#         headers = {'Content-type': "application/octet-stream",
#                    'Accept-Datetime-Format': "RFC3339",
#                    'Authorization': f"Bearer {API_KEY}"}
#         with requests.Session() as session:
#             response = session.get(url, headers=headers, params=params, stream=True)
#             for line in response.iter_lines():
#                 if line:
#                     decoded_line = json.loads(line.decode('utf-8'))
#                     print('_______________________________________________')
#                     print(decoded_line.get('time'))
#                     # print('decoded line type: ', type(decoded_line))
#                     # print('_______________________________________________')
#                     await self.channel_layer.group_send(
#                         "pricing_group",
#                         {
#                             "type": "price_update",
#                             "message": decoded_line
#                         }
#                     )
#
#     # Method for sending messages to WebSocket
#     async def price_update(self, event):
#         print('Sending price update.....')
#         message = event['message']
#         # print(f'Sending message: {message}')
#         await self.send(text_data=json.dumps(message))

# class PriceStreamConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add("pricing_group", self.channel_name)
#         await self.accept()
#         print(self.channel_name, "...group added")
#
#         # asyncio.create_task(self.stream_prices())
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("pricing_group", self.channel_name)
#
#     async def receive(self, text_data=None, bytes_data=None):
#         text_data_json = json.loads(text_data)
#         instruments = text_data_json['instruments']
#
#         await self.stream_prices(instruments)
#
#     async def stream_prices(self, instruments):
#         url = f"{OANDA_STREAM_URL}/accounts/{ACCOUNT_ID}/pricing/stream"
#         params = {'instruments': ','.join(instruments)}
#         # params = {'instruments': 'GBP_USD'}
#         # headers = SECURE_HEADER
#         headers = {'Content-type': "application/octet-stream",
#                    'Accept-Datetime-Format': "RFC3339",
#                    'Authorization': f"Bearer {API_KEY}"}
#         with requests.Session() as session:
#             response = session.get(url, headers=headers, params=params, stream=True)
#             for line in response.iter_lines():
#                 if line:
#                     decoded_line = json.loads(line.decode('utf-8'))
#                     # print('_______________________________________________')
#                     print(decoded_line)
#                     # print('decoded line type: ', type(decoded_line))
#                     # print('_______________________________________________')
#                     await self.channel_layer.group_send(
#                         "pricing_group",
#                         {
#                             "type": "update_price",
#                             "message": decoded_line
#                         }
#                     )
#                     await self.send(text_data=json.dumps({'message': 'your message has been sent'}))
#
#     # Method for sending messages to WebSocket
#     async def update_price(self, event):
#         print('update_price hit to broadcast to subscibers')
#         message = event['message']
#         await self.send(text_data=json.dumps(message))


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
        # params = {'instruments': 'GBP_USD'}
        # headers = SECURE_HEADER
        headers = {'Content-type': "application/octet-stream",
                   'Accept-Datetime-Format': "RFC3339",
                   'Authorization': f"Bearer {API_KEY}"}
        with requests.Session() as session:
            response = session.get(url, headers=headers, params=params, stream=True)
            for line in response.iter_lines():
                if line:
                    decoded_line = json.loads(line.decode('utf-8'))
                    print('_______________________________________________')
                    # print('decoded line type: ', type(decoded_line))
                    # print('_______________________________________________')
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

