from portfolio.models import AccountHistory, BotSettings, PortfolioInstrument
from trading.models import Trade, Instrument
from trading.api_utils import get_current_price, fetch_candle_data
from django.utils import timezone
from decimal import Decimal


class PortfolioBot:
    def __init__(self, profile):
        self.profile = profile
        self.bot_settings = self.get_bot_settings()
        self.open_trades = self.profile.trades.filter(is_open=True)
        self.total_equity = self.profile.equity()
        self.asset_allocations = {}
        # Hardcoded list of instruments the bot will manage
        self.target_instruments = {
            'EUR/USD': Decimal(0.3),
            'GBP/USD': Decimal(0.2),
            'USD/JPY': Decimal(0.2),
            'GBP/JPY': Decimal(0.1),
            'USD/CAD': Decimal(0.1),
            'AUD/USD': Decimal(0.1),
        }

    def get_bot_settings(self):
        return BotSettings.objects.filter(profile=self.profile, is_active=True).first()

    def calculate_portfolio_state(self):
        # Calculate the current allocation of each asset in the portfolio
        for instrument_name in self.target_instruments.keys():
            try:
                instrument = Instrument.objects.get(display_name=instrument_name)
            except Instrument.DoesNotExist:
                print(f"Instrument {instrument_name} not found.")
                continue
            current_value = self.get_instrument_value(instrument)
            # self.asset_allocations[instrument_name] = current_value / self.total_equity
            allocation_percentage = current_value / self.total_equity
            self.asset_allocations[instrument_name] = float(allocation_percentage)

    def get_instrument_value(self, instrument):
        # Calculate the value of the given instrument in the portfolio
        instrument_trades = self.open_trades.filter(instrument=instrument)
        value = Decimal(0)
        for trade in instrument_trades:
            current_price = trade.instrument.current_price()
            value += (current_price * trade.volume)
        return value

    def rebalance_portfolio(self):
        total_value = self.calculate_portfolio_value()

        current_allocations = {}
        for trade in self.profile.trades.filter(is_open=True):
            instrument_name = trade.instrument.display_name
            current_value = trade.current_value()
            current_allocations[instrument_name] = current_allocations.get(instrument_name, Decimal('0')) + current_value

        # Convert the current allocations to percentages
        for instrument, value in current_allocations.items():
            current_allocations[instrument] = value / total_value

        adjustments = {}
        for instrument_name, target_percentage in self.target_instruments.items():
            current_percentage = current_allocations.get(instrument_name, Decimal('0'))
            difference = target_percentage - current_percentage

            adjustments[instrument_name] = difference

        for instrument_name, adjustment in adjustments.items():
            try:
                instrument = Instrument.objects.get(display_name=instrument_name)
            except Instrument.DoesNotExist:
                print(f"Instrument {instrument_name} not found.")
                continue
            current_price = instrument.current_price()

            if adjustment > 0:
                amount_to_invest = adjustment * total_value
                volume_to_buy = amount_to_invest / current_price
                self.execute_trade(instrument, volume_to_buy, Trade.BUY)
            elif adjustment < 0:
                amount_to_sell = abs(adjustment) * total_value
                volume_to_sell = amount_to_sell / current_price
                self.execute_trade(instrument, volume_to_sell, Trade.SELL)

    def calculate_portfolio_value(self):
        total_value = Decimal(0)
        for trade in self.profile.trades.filter(is_open=True):
            total_value += trade.current_value()
        return total_value

    def execute_strategy(self):
        for instrument_name in self.target_instruments.keys():
            try:
                instrument = Instrument.objects.get(display_name=instrument_name)
            except Instrument.DoesNotExist:
                print(f"Instrument {instrument_name} not found.")
                continue
            self.moving_average_strategy(instrument)

    def moving_average_strategy(self, instrument):
        candles = fetch_candle_data(instrument.name, count=100, granularity=self.bot_settings.granularity)
        close_prices = [float(candle['mid']['c']) for candle in candles['candles']]
        short_ma = sum(close_prices[-self.bot_settings.short_ma_period:]) / self.bot_settings.short_ma_period
        long_ma = sum(close_prices[-self.bot_settings.long_ma_period:]) / self.bot_settings.long_ma_period
        print(f"\nShort MA: {short_ma}\nLong MA: {long_ma}")

        prev_short_ma = self.bot_settings.prev_short_ma
        prev_long_ma = self.bot_settings.prev_long_ma

        # bid_price, ask_price = get_current_price(instrument)

        if prev_short_ma and prev_long_ma:
            if prev_short_ma <= prev_long_ma and short_ma > long_ma:
                print(f"Buy signal for {instrument.name}")
                self.execute_trade(instrument, 10, Trade.BUY)
            elif prev_short_ma >= prev_long_ma and short_ma < long_ma:
                print(f"Sell signal for {instrument.name}")
                self.execute_trade(instrument, 10, Trade.SELL)

        self.bot_settings.prev_short_ma = short_ma
        self.bot_settings.prev_long_ma = long_ma
        self.bot_settings.save()

        self.update_account_history()

    def execute_trade(self, instrument, volume, trade_type):
        entry_price = get_current_price(instrument)[0] if trade_type == Trade.BUY else get_current_price(instrument)[1]

        trade = Trade.objects.create(
            profile=self.profile,
            instrument=instrument,
            currency_pair=instrument.display_name,
            volume=volume,
            entry_price=entry_price,
            open_date=timezone.now(),
            is_open=True,
            bot=True,
            trade_type=trade_type
        )

        take_profit_percentage = 0.002
        stop_loss_percentage = 0.004

        if trade_type == Trade.BUY:
            trade.take_profit = trade.entry_price * (1 + take_profit_percentage)
            trade.stop_loss = trade.entry_price * (1 - stop_loss_percentage)
        elif trade_type == Trade.SELL:
            trade.take_profit = trade.entry_price * (1 - take_profit_percentage)
            trade.stop_loss = trade.entry_price * (1 + stop_loss_percentage)

        trade.save()

    def monitor_and_close_trades(self):
        for trade in self.open_trades:
            if trade.bot:
                current_price = trade.instrument.current_price()

                if trade.trade_type == Trade.BUY:
                    if current_price >= trade.take_profit:
                        trade.close_trade(current_price)
                        print(f"Closed Buy trade at take profit: {current_price}")
                    elif current_price <= trade.stop_loss:
                        trade.close_trade(current_price)
                        print(f"Closed Buy trade at stop loss: {current_price}")

                elif trade.trade_type == Trade.SELL:
                    if current_price <= trade.take_profit:
                        trade.close_trade(current_price)
                        print(f"Closed Sell trade at take profit: {current_price}")
                    elif current_price >= trade.stop_loss:
                        trade.close_trade(current_price)
                        print(f"Closed Sell trade at stop loss: {current_price}")

    def update_account_history(self):
        AccountHistory.objects.create(
            profile=self.profile,
            timestamp=timezone.now(),
            balance=float(self.profile.balance),
            equity=float(self.profile.equity()),
            unrealized_pl=float(self.profile.unrealized_pl()),
            realized_pl=float(self.profile.realized_pl),
            asset_allocation={k: float(v) for k, v in self.asset_allocations.items()}
        )

    def run(self):
        # Main method to run the bot and manage the portfolio
        if not self.bot_settings:
            print("No active bot settings found. No trade has been opened yet!")
            return

        if not self.bot_settings.is_active:
            print("Bot is not active.")
            return

        # Step 1: Calculate the current portfolio state
        self.calculate_portfolio_state()

        # Step 2: Monitor and close existing trades if needed
        self.monitor_and_close_trades()

        # Step 3: Execute trading strategy for each instrument
        self.execute_strategy()

        # Step 4: Rebalance portfolio if necessary
        self.rebalance_portfolio()

        # Step 5: Update account history after all operations
        self.update_account_history()

