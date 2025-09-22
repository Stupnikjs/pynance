
import pandas as pd
import connector as conn
import plotter 
import numpy as np
import matplotlib.pyplot as plt

import os



pair = ["BTCUSDC", "ETHUSDC", "ETHBTC", "LINKUSDC"]








client = conn.connect_client()

path = os.path.join("data", "ETHBTC_1w.csv")

df = pd.read_csv(path)


max = df['Close'].rolling(window=50, center=True).max()
df['max'] = df['Close'] == max

isPeak = df['max'] == True

peaks =  df[isPeak].index.values

all_indices = df.index.values

# Calculate the absolute difference from each point to every peak point.
# np.newaxis is crucial here; it transforms all_indices into a column vector,
# allowing for broadcasting to create a 2D array of distances.
distances = np.abs(all_indices[:, np.newaxis] - peaks)

df['dist_from_peak'] = np.min(distances, axis=1)
print(df.tail())