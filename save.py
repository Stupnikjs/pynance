
import os
import pandas as pd
import connector as conn



def save_pair_csv(pair, interval): 
    filename = os.path.join(interval, pair + ".csv")
    client = conn.connect_client() 
    data = conn.klines_data(client=client, pair=pair, interval=interval)
    df_fetch = conn.klinesToDataFrame(data)
    os.makedirs(interval, exist_ok=True)  
     
    if os.path.exists(filename): 
        df = pd.read_csv(filename)
        df = pd.concat([df, df_fetch]).drop_duplicates().reset_index(drop=True)
        df.to_csv(filename, index=False)
    else:
        df_fetch.to_csv(filename, index=False)
        
def wrapper_save(interval):
    pair = ["BTCUSDC", "ETHUSDC", "ETHBTC", "LINKUSDC", "LINKBTC"]
    for p in pair:
        save_pair_csv(p, interval)
        

