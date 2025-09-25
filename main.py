import pandas as pd
import connector as conn
import plotter 
import numpy as np
import matplotlib.pyplot as plt

eth = conn.get_df('ETHUSDC', '1w')
btc = conn.get_df('BTCUSDC', '1w')

plotter.plot_two_price(btc['Close'], eth['Close'], btc['Close time'])






