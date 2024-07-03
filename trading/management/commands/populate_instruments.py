from django.core.management.base import BaseCommand
from trading.models import Instrument
from trading.api_utils import get_account_instruments


class Command(BaseCommand):
    help = 'Populates the database with instrument data from OANDA'

    def handle(self, *args, **options):
        data = get_account_instruments()
        for item in data['instruments']:
            Instrument.objects.update_or_create(
                name=item['name'],
                defaults={
                    'display_name': item['displayName'],
                    'maximum_order_units': item['maximumOrderUnits'],
                    'margin_rate': item['marginRate'],
                    'minimum_trade_size': item['minimumTradeSize'],
                    'pip_location': item['pipLocation'],
                    'type': item['type'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully populated instrument data'))
