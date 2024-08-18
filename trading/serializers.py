from rest_framework import serializers

from trading.models import Trade


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


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['id', 'profile', 'strategy', 'instrument', 'currency_pair', 'volume', 'entry_price', 'exit_price',
                  'open_date', 'close_date', 'is_open']
        read_only_fields = ['id', 'open_date', 'close_date']  # Ensures that these fields are not editable via API

    def create(self, validated_data):
        return Trade.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.exit_price = validated_data.get('exit_price', instance.exit_price)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        if not instance.is_open:
            instance.close_date = timezone.now()
        instance.save()
        return instance
