class CryptoMarketData:
    def __init__(self, mode='live', historical_file=None):
        """
        Initialize the CryptoMarketData object here.
        """
        pass

    def load_historical_data(self):
        """
        Loads the historical price data from a file (for historical mode).
        """
        pass

    def get_live_price(self):
        """
        Fetches the current live Crypto price from an external API.
        """
        pass

    def get_historical_price(self):
        """
        Returns the next price from the historical data (for replay mode).
        """
        pass

    def get_latest_price(self):
        """
        Depending on the mode ('live' or 'historical'), returns the latest price.
        """
        pass

if __name__ == "__main__":

    # Historical mode example
    dataSource = CryptoMarketData(mode="historical", historical_file="/path/to/data")
    latest_price = dataSource.get_latest_price()
    # Train with historical

    # Live mode example
    dataSource = CryptoMarketData(mode="live")
    latest_price = dataSource.get_latest_price()



