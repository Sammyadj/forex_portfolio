# from trading.api_utils import get_current_price, fetch_candle_data
# from trading.models import Trade, Instrument
# from .models import AccountHistory, BotSettings
# from django.utils import timezone
# from .bot_portfolio import PortfolioBot
#
#
# def run_bot(profile_id):
#     bot_settings = BotSettings.objects.get(profile_id=profile_id)
#     if bot_settings.is_active:
#         portfolio_bot = PortfolioBot(bot_settings.profile)
#         portfolio_bot.rebalance_portfolio()
#         moving_average_strategy(profile_id)
#
#
# def moving_average_strategy(profile_id):
#     bot_settings = BotSettings.objects.get(profile_id=profile_id)
#
#     if bot_settings.is_active:
#         profile = bot_settings.profile
#         monitor_and_close_trades(profile)
#
#         instrument = bot_settings.instrument
#         try:
#             instrument_obj = Instrument.objects.get(name=instrument)
#         except Instrument.DoesNotExist:
#             print(f"Instrument {instrument} not found.")
#             return
#
#         candles = fetch_candle_data(instrument_obj.name, count=100, granularity=bot_settings.granularity)
#
#         close_prices = [float(candle['mid']['c']) for candle in candles['candles']]
#         short_ma = sum(close_prices[-bot_settings.short_ma_period:]) / bot_settings.short_ma_period
#         long_ma = sum(close_prices[-bot_settings.long_ma_period:]) / bot_settings.long_ma_period
#
#         print(f"\nShort MA: {short_ma}\nLong MA: {long_ma}")
#
#         prev_short_ma = bot_settings.prev_short_ma
#         prev_long_ma = bot_settings.prev_long_ma
#
#         bid_price, ask_price = get_current_price(instrument_obj)
#
#         if prev_short_ma and prev_long_ma:
#             if prev_short_ma <= prev_long_ma and short_ma > long_ma:
#                 print("\nCross found: BUY signal")
#                 execute_trade(profile, instrument_obj, instrument_obj.display_name, ask_price, Trade.BUY)
#             elif prev_short_ma >= prev_long_ma and short_ma < long_ma:
#                 print("\nCross found: SELL signal")
#                 execute_trade(profile, instrument_obj, instrument_obj.display_name, bid_price, Trade.SELL)
#
#         bot_settings.prev_short_ma = short_ma
#         bot_settings.prev_long_ma = long_ma
#         bot_settings.save()
#
#         AccountHistory.objects.create(
#             profile=profile,
#             timestamp=timezone.now(),
#             balance=profile.balance,
#             equity=profile.equity(),
#             unrealized_pl=profile.unrealized_pl(),
#             realized_pl=profile.realized_pl(),
#         )
#
#
# def execute_trade(profile, instrument, currency_pair, price, trade_type):
#     trade = Trade.objects.create(
#         profile=profile,
#         instrument=instrument,
#         currency_pair=currency_pair,
#         volume=1.0,
#         entry_price=price,
#         open_date=timezone.now(),
#         is_open=True,
#         bot=True,
#         trade_type=trade_type
#     )
#
#     # Define your take profit and stop loss percentages
#     take_profit_percentage = 0.05  # 5.0% profit target
#     stop_loss_percentage = 0.05  # 5.0% loss limit
#
#     if trade_type == Trade.BUY:
#         trade.take_profit = trade.entry_price * (1 + take_profit_percentage)
#         trade.stop_loss = trade.entry_price * (1 - stop_loss_percentage)
#     elif trade_type == Trade.SELL:
#         trade.take_profit = trade.entry_price * (1 - take_profit_percentage)
#         trade.stop_loss = trade.entry_price * (1 + stop_loss_percentage)
#
#     trade.save()
#
#
# def monitor_and_close_trades(profile):
#     open_trades = profile.trades.filter(is_open=True)
#
#     # if open_trades:
#     for trade in open_trades:
#         if trade.bot:
#             current_price = trade.instrument.current_price()
#
#             if trade.trade_type == Trade.BUY:
#                 if current_price >= trade.take_profit:
#                     trade.close_trade(current_price)
#                     print(f"Closed Buy trade at take profit: {current_price}")
#                 elif current_price <= trade.stop_loss:
#                     trade.close_trade(current_price)
#                     print(f"Closed Buy trade at stop loss: {current_price}")
#
#             elif trade.trade_type == Trade.SELL:
#                 if current_price <= trade.take_profit:
#                     trade.close_trade(current_price)
#                     print(f"Closed Sell trade at take profit: {current_price}")
#                 elif current_price >= trade.stop_loss:
#                     trade.close_trade(current_price)
#                     print(f"Closed Sell trade at stop loss: {current_price}")