import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from process import append_diff_from_peak, EMA_DIF, Normalized
from connector import get_df

df = get_df("XRPUSDC", "1d")
df2 = get_df("ETHUSDC", "1d")
df3 = get_df("BTCUSDC", "1d")
df = pd.concat([df, df2, df3]).drop_duplicates().reset_index(drop=True)

def pre_process(df): 
    df = append_diff_from_peak(df)
    df = EMA_DIF(df, 9, 15)
    max_diff = df['dist_from_peak'].max()

    Y = Normalized('dist_from_peak', df)
    Y = Y['Normalized_dist_from_peak']
    X = df
    X = X.drop(columns=['Quote asset volume', 'Number of trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    X = X.drop(['dist_from_peak', 'Close time', 'Open time'], axis=1)

    X = Normalized('Close' , X)
    X = Normalized('Open' , X)
    X = Normalized('High' , X)
    X = Normalized('Low' , X)
    X = Normalized('Volume' , X)
    X = Normalized('EMA_dif' , X)
    return X,Y, max_diff

X, Y, max_y = pre_process(df)

X_eth, Y_eth, max_y_eth = pre_process(df2)

# # 2. Séparer les données en ensembles d'entraînement et de test
# # test_size=0.2 signifie 20% pour le test, 80% pour l'entraînement
# # random_state assure la reproductibilité du split
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

# Calculate Root Mean Squared Error (RMSE) for better interpretability
rmse = np.sqrt(mse)

# Report the Regression metrics
print(f"Erreur Quadratique Moyenne (MSE) du modèle Random Forest: {mse:.4f}")
print(f"Racine de l'Erreur Quadratique Moyenne (RMSE) du modèle: {rmse:.4f}")

eth_y_predict = rf_model.predict(X_eth)

diff = eth_y_predict * max_y_eth

plot_df = df2.copy()
plot_df['diff'] = diff
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8), gridspec_kw={'height_ratios': [6, 4]})
ax1.plot(df2['Close time'], df2['Close'], color='blue')
ax2.plot(plot_df['Close time'], plot_df['diff'], color='red')
plt.tight_layout()

plt.show()