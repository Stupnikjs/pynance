from scipy.signal import find_peaks
import numpy as np
import pandas as pd
from pandas import DataFrame 
import matplotlib.pyplot as plt
import os


def Normalized(column, df) -> DataFrame:
    normalized = "Normalized_" + column
    max_ = df[column].max()
    df[normalized] = df[column] / max_
    df  = df.drop(columns=[column])
    return df

def EMA_DIF(df, short, long) -> DataFrame:
    short = df['Close'].ewm(span=short, adjust=False).mean()
    long = df['Close'].ewm(span=long, adjust=False).mean()
    df['EMA_dif'] = short - long
    return df 
     
 

def remove_useless_column(df) -> DataFrame:
    df.drop(columns=['Taker buy base asset volume',
        'Taker buy quote asset volume',
        'Ignore', 'Quote asset volume'])
    return df 



def append_diff_from_peak(df) -> DataFrame:
    peaks, prop = find_peaks(df['Close'], distance=50, height=round(df['Close'].max()/4))
    df["isPeak"] = df.index.isin(peaks)

    peak_indices = df[df['isPeak']].index.values
    print(peak_indices)
    if len(peak_indices) == 0:
        df['dist_from_peak'] = np.nan
        return df
    all_indices = df.index.values
    # The outer subtraction (broadcasting) creates a 2D array of all possible distances.
    # The result is a matrix where entry (i, j) is the distance from point i to peak j.
    distances = np.abs(all_indices[:, np.newaxis] - peak_indices)
    # Find the minimum distance for each row (axis=1) and assign it to the new column.
    df['dist_from_peak'] = np.min(distances, axis=1)

    return df


