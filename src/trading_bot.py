import numpy as np
import random
from crypto_market_data import CryptoMarketData


class MovingAverageTradingBot:
    def __init__(self, budget):
        """
        Initialize the trading bot with a total budget and no open trades.
        :param budget: The total amount of money available for trading.
        """
        self.budget = budget
        self.total_profit = 0.0
        self.current_position = None  # Track if there is an open position (None if no trade is open)
        self.entry_price = 0.0  # Price at which the current position was opened
        self.prices = []  # Store the prices for moving average calculation
        self.short_window = 20  # Short-term moving average window (20-day)
        self.long_window = 50   # Long-term moving average window (50-day)

    def process_price(self, price):
        """
        Process a new price, calculate moving averages, and make trading decisions.
        :param price: The current price of the stock.
        """
        self.prices.append(price)

        # Only start checking for trades after we have enough data points
        if len(self.prices) >= self.long_window:
            short_ma = np.mean(self.prices[-self.short_window:])  # 20-day moving average
            long_ma = np.mean(self.prices[-self.long_window:])    # 50-day moving average

            self.execute_trade(price, short_ma, long_ma)

    def execute_trade(self, price, short_ma, long_ma):
        """
        Execute the trade based on the moving average strategy (buy/sell).
        :param price: The current price of the stock.
        :param short_ma: Short-term moving average (20-day).
        :param long_ma: Long-term moving average (50-day).
        """
        # Golden cross: Short MA crosses above Long MA -> Buy
        if short_ma > long_ma and self.current_position is None:
            self.open_position(price)

        # Death cross: Short MA crosses below Long MA -> Sell
        elif short_ma < long_ma and self.current_position is not None:
            self.close_position(price)

    def open_position(self, price):
        """
        Open a new trade (buy position).
        :param price: The price at which the stock is bought.
        """
        if self.current_position is None:
            self.current_position = "Stock"  # Assume trading a generic stock
            self.entry_price = price
            print(f"Opened position at {price}")

    def close_position(self, price):
        """
        Close the current trade (sell position).
        :param price: The price at which the stock is sold.
        """
        if self.current_position is not None:
            profit = price - self.entry_price
            self.update_profit(profit)
            print(f"Closed position at {price} with profit: {profit}")
            self.current_position = None  # Reset after selling

    def update_profit(self, profit):
        """
        Update the total profit after a trade is closed.
        :param profit: The profit from the completed trade.
        """
        self.total_profit += profit
        print(f"Total Profit: {self.total_profit}")

# Example usage
data_source = CryptoMarketData(symbol="ETH-USD", historical=True, historical_day_range=365 * 5)

# Simulate sequential price updates
bot: MovingAverageTradingBot = MovingAverageTradingBot(10000)
while data_source.has_historical_data():
    bot.process_price(data_source.get_latest_price())