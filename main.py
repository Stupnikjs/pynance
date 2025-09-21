from binance_sdk_spot.spot import Spot,ConfigurationRestAPI
import pandas as pd
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


def klinesToDataFrame(klines): 
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


data = klinesData(client=client, pair="BTCUSDC", interval="1w")
df = klinesToDataFrame(data)





# Print the head of the DataFrame to show the result
print("\nDataFrame created successfully:")


plt.plot(df['Close time'], df['Close'])
plt.show()


