import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class CryptoMarketData:
    def __init__(self, symbol: str = "BTC-USD", historical: bool = True, historical_day_range: int = 365):
        """
        Initialize the CryptoMarketData object here.
        """
        self.symbol: str = symbol
        self.historical: bool = True
        self.historical_data: pd.DataFrame = None
        self.historical_day_range: int = historical_day_range
        self.historical_idx: int = 0
        if self.historical:
            self.load_historical_data()

    def load_historical_data(self):
        """
        Loads the historical price data from an external source (for historical mode).
        """
        end_date: str = datetime.today().strftime('%Y-%m-%d')
        start_date: str = (datetime.today() - timedelta(days=self.historical_day_range)).strftime('%Y-%m-%d')
        btc_data: yf.Ticker = yf.Ticker(self.symbol)
        historical_data: pd.DataFrame = btc_data.history(start=start_date, end=end_date)
        self.historical_data = historical_data[['Close']]
        self.historical_day_range = len(self.historical_data)

    def get_historical_price(self):
        """
        Returns the next price from the historical data along with its date.
        """
        if self.historical_idx < self.historical_day_range:
            date = self.historical_data.index[self.historical_idx].strftime('%Y-%m-%d')
            price = self.historical_data["Close"].iloc[self.historical_idx]
            self.historical_idx += 1
            return date, price
        return None, -1

    def has_historical_data(self) -> bool:
        """
        Is there more historical data to return?
        """
        return self.historical_idx < self.historical_day_range


if __name__ == "__main__":
    # Historical mode example
    data_source = CryptoMarketData(symbol="ETH-USD", historical=True, historical_day_range=365 * 2)

    # Simulate sequential price updates and display date and price
    while data_source.has_historical_data():
        date, price = data_source.get_historical_price()
        if price != -1:  # Ensure valid price is returned
            print(f"Date: {date}, Price: {price}")






