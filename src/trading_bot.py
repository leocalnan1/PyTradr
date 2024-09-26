import numpy as np
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
        self.dates = []  # Store the dates corresponding to the prices
        self.short_window = 50  # Short-term moving average window (20-day)
        self.long_window = 100   # Long-term moving average window (50-day)

    def process_price(self, date, price):
        """
        Process a new price, calculate moving averages, and make trading decisions.
        :param date: The current date of the price.
        :param price: The current price of the stock.
        """
        self.prices.append(price)
        self.dates.append(date)

        # Only start checking for trades after we have enough data points
        if len(self.prices) >= self.long_window:
            short_ma = np.mean(self.prices[-self.short_window:])  # 20-day moving average
            long_ma = np.mean(self.prices[-self.long_window:])    # 50-day moving average

            self.execute_trade(date, price, short_ma, long_ma)

    def execute_trade(self, date, price, short_ma, long_ma):
        """
        Execute the trade based on the moving average strategy (buy/sell).
        :param date: The current date of the price.
        :param price: The current price of the stock.
        :param short_ma: Short-term moving average (20-day).
        :param long_ma: Long-term moving average (50-day).
        """
        # Golden cross: Short MA crosses above Long MA -> Buy
        if short_ma > long_ma and self.current_position is None:
            self.open_position(date, price)

        # Death cross: Short MA crosses below Long MA -> Sell
        elif short_ma < long_ma and self.current_position is not None:
            self.close_position(date, price)

    def open_position(self, date, price):
        """
        Open a new trade (buy position).
        :param date: The date at which the stock is bought.
        :param price: The price at which the stock is bought.
        """
        if self.current_position is None:
            self.current_position = "Stock"  # Assume trading a generic stock
            self.entry_price = price
            print(f"Opened position on {date} at {price}")

    def close_position(self, date, price):
        """
        Close the current trade (sell position).
        :param date: The date at which the stock is sold.
        :param price: The price at which the stock is sold.
        """
        if self.current_position is not None:
            profit = price - self.entry_price
            self.update_profit(profit)
            print(f"Closed position on {date} at {price} with profit: {profit}")
            self.current_position = None  # Reset after selling

    def update_profit(self, profit):
        """
        Update the total profit after a trade is closed.
        :param profit: The profit from the completed trade.
        """
        self.total_profit += profit
        print(f"Total Profit: {self.total_profit}")
        print(f"")

# Example usage
data_source = CryptoMarketData(symbol="ETH-USD", historical=True, historical_day_range=365)

# Simulate sequential price updates
bot = MovingAverageTradingBot(10000)
while data_source.has_historical_data():
    date, price = data_source.get_historical_price()
    if price != -1:
        bot.process_price(date, price)
