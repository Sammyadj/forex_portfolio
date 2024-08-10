# Forex Portfolio Management

## Project Overview

## Forex Trading Platform Specifications
### 1. Overview
The Forex Trading Platform is designed to simulate Forex trading using real-time data fetched from the OANDA API. The platform allows users to test trading strategies in a risk-free environment using virtual currency (GBP). Users can engage in trading activities, apply automated trading algorithms (bots), and manually intervene in trades.
### 2. User Capabilities
- **View Real-Time Charts**: Users can view live Forex market data in chart form, similar to the charts on the OANDA practice account dashboard. This feature helps users monitor market trends and make informed trading decisions.

- **Select and Apply Trading Strategies**: Users can choose from a list of predefined trading algorithms or bots. Once a strategy is selected, it can automatically execute trades based on its programming.

- **Manual Trading**: Users have the ability to manually open and close trades, providing flexibility in their trading approach.

- **Intervene in Automated Trades**: Users can stop an automated bot from taking over trading manually, allowing them to end or modify the bot's trades according to current market conditions.

- **Set Take Profits and Stop Losses**: For each trade, whether manual or automated, users can set take profit and stop loss orders to manage risks effectively.

- **Instant Execution of Trades**: All trades are executed instantly based on the user's or bot's command, ensuring timely market entry and exit.

### 3. System Limitations and Boundaries

- **API Key Usage**: Since the app uses a single API key provided by the developer, all data and trading actions are simulated through one OANDA account. This setup is intended for demonstration and learning purposes only, not for real trading.

- **Currency Limitations**: All transactions are currently denominated in GBP only. Multi-currency support is not available at this stage.

- **Trading Actions**: The app does not support complex order types like pending orders. Only instant execution is available.

- **Automated Trading**: When a trading bot is active, users can still manually trade; however, manual trades do not affect the algorithm's operations unless the bot is stopped or paused by the user.

- **Data Latency**: While the app aims to provide real-time data, there might be slight delays or discrepancies due to API limitations or network issues.

### 4. Technical Architecture

- **Trading Execution**: Trades are executed based on live data fetched from the OANDA API. When a user or bot decides to execute a trade, the app sends a request to the OANDA API to open or close a trade with specified conditions (e.g., take profit, stop loss).

- **Bot Activation**: Upon activating a bot, the app schedules and runs the bot's trading logic continuously in the background. The bot checks real-time data and executes trades according to its algorithm.

- **User Interface**: The user interface updates dynamically to reflect changes in the market and the status of trades, providing users with up-to-date visual feedback.


- **Improved Data Accuracy**: Enhancing the data fetching mechanism to reduce latency and improve the accuracy of market data displayed.



