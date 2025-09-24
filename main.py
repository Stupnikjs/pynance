import pandas as pd
import connector as conn
import plotter 
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import find_peaks
from save import wrapper_save

# peaks, prop = find_peaks(df['Close'], distance=50, height=round(df['Close'].max()/4))
# plotter.show_max_points(peaks, df)

wrapper_save("1w")



