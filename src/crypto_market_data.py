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
        self.historical_close_prices: pd.DataFrame = None
        self.historical_day_range: int = historical_day_range
        self.historical_idx: int = 0
        if self.historical:
            self.load_historical_data()


    def load_historical_data(self):
        """
        Loads the historical price data from a file (for historical mode).
        """
        end_date: str = datetime.today().strftime('%Y-%m-%d')
        start_date: str = (datetime.today() - timedelta(days=self.historical_day_range)).strftime('%Y-%m-%d')
        btc_data: yf.Ticker = yf.Ticker(self.symbol)
        historical_data: pd.DataFrame = btc_data.history(start=start_date, end=end_date)
        self.historical_close_prices = historical_data[['Close']]
        self.historical_idx = len(self.historical_close_prices)

    def get_live_price(self):
        """
        Fetches the current live Crypto price from an external API.
        """
        pass

    def get_historical_price(self) -> float:
        """
        Returns the next price from the historical data (for replay mode).
        """
        price: float = -1
        if self.historical_idx > 0:
            price: float = self.historical_close_prices["Close"][self.historical_idx-1]
            self.historical_idx -= 1
        return price

    def get_latest_price(self) -> float:
        """
        Depending on the mode ('live' or 'historical'), returns the latest price.
        """
        if self.historical:
            return self.get_historical_price()
        else:
            return 0

    def has_historical_data(self) -> bool:
        """
        Is there more historical data to return?
        """
        return self.historical_idx > 0


if __name__ == "__main__":

    # Historical mode example
    data_source = CryptoMarketData(historical=True, historical_day_range=5)
    while data_source.has_historical_data():
        print(data_source.get_latest_price())






