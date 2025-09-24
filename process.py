from binance_sdk_spot.spot import Spot,ConfigurationRestAPI
import numpy as np
import pandas as pd
from pandas import DataFrame 
import matplotlib.pyplot as plt
import os



def remove_useless_column(df) -> DataFrame:
    df.drop(columns=['Taker buy base asset volume',
        'Taker buy quote asset volume',
        'Ignore', 'Quote asset volume'])
    return df 



def append_diff_from_peak(df) -> DataFrame:
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
