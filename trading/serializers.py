from rest_framework import serializers


class InstrumentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    display_name = serializers.CharField(max_length=100)
    maximum_order_units = serializers.IntegerField()
    margin_rate = serializers.CharField(max_length=100)
    minimum_trade_size = serializers.CharField(max_length=100)
    pip_location = serializers.IntegerField()
    type = serializers.CharField(max_length=50)


class PriceSerializer(serializers.Serializer):
    bid_price = serializers.FloatField()
    ask_price = serializers.FloatField()


class MidSerializer(serializers.Serializer):
    o = serializers.FloatField()
    h = serializers.FloatField()
    l = serializers.FloatField()
    c = serializers.FloatField()


class CandleSerializer(serializers.Serializer):
    complete = serializers.BooleanField()
    volume = serializers.IntegerField()
    time = serializers.DateTimeField()
    mid = MidSerializer()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.update({
            'open': representation['mid']['o'],
            'high': representation['mid']['h'],
            'low': representation['mid']['l'],
            'close': representation['mid']['c']
        })
        del representation['mid']  # Remove 'mid' after extracting values
        return representation

