import matplotlib.pyplot as plt
import pandas as pd




def plot_price_vol(df): 
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8), gridspec_kw={'height_ratios': [9, 1]})
    ax1.plot(df['Close time'], df['Close'], color='blue', label='Closing Price')
    ax1.set_xlabel('Date')
    ax2.bar(df['Close time'], df['Volume'], width=5, color='orange', label='Volume')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show(block=True)


def show_max_points(df):
    max = df['Close'].rolling(window=50, center=True).max()
    df['max'] = df['Close'] == max



    plt.figure(figsize=(12, 6))

    # Plot the 'Close' price curve as a blue line
    plt.plot(df.index, df['Close'], label='Price', color='blue')

    # Plot the points where the price is the rolling maximum as red dots
    max_points = df[df['max']]
    plt.scatter(max_points.index, max_points['Close'], color='red', s=50, zorder=5, label='Rolling Max Points')

    # Add labels, a title, and a legend to the plot for clarity
    plt.title('Price with Rolling Maximum Points')
    plt.xlabel('Index')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    plt.show(block=True)

