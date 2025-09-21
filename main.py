from binance_sdk_spot.spot import Spot,ConfigurationRestAPI
import pandas as pd
from pandas import DataFrame 
import matplotlib.pyplot as plt


# Initialize the Spot client
config = ConfigurationRestAPI(api_key="b0mxs4awZtYEX4GdvIUEYQj1cetLFcBJDVV8gs3twF0HeqZFeq5Qh6LhoMcWlCTE", api_secret="f8HJWCYCvJS7odHSueuEtgiC7dsVfpdqBMfFImXuUyWIQg0aScP2plwds1ki73p9") 
client = Spot(config)



def klinesData(client, pair, interval): 

    klines_data = client.rest_api.klines(
        symbol=pair,
        interval=interval,
        limit=1000
    )

    return klines_data.data()


def klinesToDataFrame(klines) -> DataFrame: 
    columns = [
        'Open time',
        'Open',
        'High',
        'Low',
        'Close',
        'Volume',
        'Close time',
        'Quote asset volume',
        'Number of trades',
        'Taker buy base asset volume',
        'Taker buy quote asset volume',
        'Ignore'
    ]

    # Create the pandas DataFrame and assign the column names
    df = pd.DataFrame(klines, columns=columns)

    # Convert timestamp columns from milliseconds to human-readable datetime
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')

    # Convert numeric columns from string to float
    numeric_cols = [
        'Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume',
        'Taker buy base asset volume', 'Taker buy quote asset volume'
    ]
    df[numeric_cols] = df[numeric_cols].astype(float)
    return df

def closePeak(df) -> DataFrame: 
    rolling_max = df['Close'].rolling(window=10, center=True).max()
    df['isThereClosePeak'] = df['Close'] == rolling_max
    return df 


data = klinesData(client=client, pair="ETHBTC", interval="1w")
df = klinesToDataFrame(data)
df['EMA_short'] =df['Close'].ewm(span=9, adjust=False).mean()
df['EMA_long'] =df['Close'].ewm(span=21, adjust=False).mean()
df = closePeak(df)

print(df.loc[0 : 100 , "isThereClosePeak" ])
# Print the head of the DataFrame to show the result
print("\nDataFrame created successfully:")

"""
fig, ax = plt.subplots()
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8), gridspec_kw={'height_ratios': [9, 1]})

ax1.plot(df['Close time'], df['Close'], color='blue', label='Closing Price')
ax1.plot(df['Close time'], df['EMA_short'], color='yellow', label='EMA_short')
ax1.plot(df['Close time'], df['EMA_long'], color='black', label='EMA_long')

ax2.bar(df['Close time'], df['Volume'], width=5, color='orange', label='Volume')


plt.show()

"""
