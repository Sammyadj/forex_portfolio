from rest_framework.views import APIView
from rest_framework.response import Response
from .api_utils import get_account_instruments, get_current_price, fetch_candle_data
from .serializers import InstrumentSerializer, PriceSerializer, CandleSerializer
from django.utils.dateparse import parse_datetime

class APIRootView(APIView):
    def get(self, request, format=None):
        api_endpoints = {
            'instruments': request.build_absolute_uri('instruments/'),
            'current prices': request.build_absolute_uri('pricing/{instrument_name}/'),
            'candle data': request.build_absolute_uri('candles/{instrument_name}/')
        }
        return Response(api_endpoints)


class InstrumentListView(APIView):
    def get(self, request, instrument_name=None):
        # instrument_query = request.query_params.get('instruments', None)
        data = get_account_instruments(instrument_name)
        instruments_data = data.get('instruments', [])
        # Filter out only the necessary fields:
        filtered_instruments = [
            {
                'name': inst['name'],
                'display_name': inst['displayName'],
                'maximum_order_units': inst['maximumOrderUnits'],
                'margin_rate': inst['marginRate'],
                'minimum_trade_size': inst['minimumTradeSize'],
                'pip_location': inst['pipLocation'],
                'type': inst['type']
            } for inst in instruments_data
        ]
        serializer = InstrumentSerializer(data=filtered_instruments, many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class CurrentPriceView(APIView):
    def get(self, request, instrument_name):
        bid_price, ask_price = get_current_price(instrument_name)
        if bid_price and ask_price:
            serializer = PriceSerializer(data={'bid_price': bid_price, 'ask_price': ask_price})
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response({'error': 'Failed to fetch prices'}, status=404)


class CandleDataView(APIView):
    def get(self, request, instrument_name):
        count = request.query_params.get('count', '100')
        granularity = request.query_params.get('granularity', 'H1')
        candles = fetch_candle_data(instrument_name, count=count, granularity=granularity)
        if 'candles' in candles:
            serializer = CandleSerializer(data=candles['candles'], many=True)
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response({'error': 'Failed to fetch data'}, status=404)


# class TradeViewSet(viewsets.ModelViewSet):
#     queryset = Trade.objects.all()
#     serializer_class = TradeSerializer
#
#
# class InstrumentViewSet(viewsets.ModelViewSet):
#     queryset = Instrument.objects.all()
#     serializer_class = InstrumentSerializer
