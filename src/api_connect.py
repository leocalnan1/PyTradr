import requests
import pandas as pd

url = "https://api.crypto.com/v2/public/get-candlestick"
params = {
    "instrument_name": "ETH_USDT",
    "timeframe": "1D"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()['result']['data']

    df = pd.DataFrame(data)

    df['t'] = pd.to_datetime(df['t'], unit='ms')

    df.columns = ['open', 'high', 'low', 'close', 'volume', 'timestamp']

    print(df)
else:
    print(f"Error: {response.status_code}")
