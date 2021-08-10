# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import preprocessing
from tensorflow import keras
from tensorflow.keras import optimizers
from tensorflow.keras.layers import Dense, Dropout, LSTM, Input, Activation
from tensorflow.keras.models import Model

HISTORY_DAYS = 40
TICKER = 'ITUB4'

# %% 
raw_dataframe = pd.read_csv('C:\\Repositories\\StockPricesPredictions\\datasets\\b3_stocks_1994_2020.csv')
dataset = raw_dataframe[raw_dataframe.ticker == TICKER]
dataset = dataset.drop(columns=["ticker", "datetime"])
 
# Preprocessing
# %%
normalizer = preprocessing.MinMaxScaler()
dataset_normalized = normalizer.fit_transform(dataset)
history_normalized = np.array([dataset_normalized[i : i + HISTORY_DAYS].copy() for i in range(len(dataset_normalized) - HISTORY_DAYS)])

next_day_normalized = np.array([dataset_normalized[:,1][i + HISTORY_DAYS].copy() for i in range (len(dataset_normalized) - HISTORY_DAYS)])
next_day_normalized = np.expand_dims(next_day_normalized, -1)

next_day_values = np.array([dataset.values[:,1][i + HISTORY_DAYS].copy() for i in range(len(dataset) - HISTORY_DAYS)])
next_day_values = np.expand_dims(next_day_values, -1)

y_normalizer = preprocessing.MinMaxScaler()
y_scaler = y_normalizer.fit(next_day_values)

assert history_normalized.shape[0] == next_day_values.shape[0]

# Train-Test Split
# %%
TEST_SPLIT = 0.9
TEST_N = int(history_normalized.shape[0] * TEST_SPLIT)

history_train = history_normalized[:TEST_N]
y_train = next_day_normalized[:TEST_N]

history_test = history_normalized[TEST_N:]
y_test = next_day_normalized[TEST_N:]

unscaled_y = next_day_values[TEST_N:]

# Model
# %%
lstm_input = keras.Input(shape=(HISTORY_DAYS, 5))
x = LSTM(50)(lstm_input)
x = Dropout(0.2)(x)
x = Dense(64)(x)
x = Activation('sigmoid')(x)
x = Dense(1)(x)
output = Activation('linear',)(x)
model = Model(inputs=lstm_input, outputs=output)

adam = optimizers.Adam(lr=0.0005)
model.compile(optimizer=adam, loss='mse')

# Traning
# %%
model.fit(x=history_train, y=y_train, batch_size=64, epochs=50, shuffle=True, validation_split=0.1)
evaluation = model.evaluate(history_test, y_test)
print(evaluation)

# Evaluation
# %%
y_test_predicted = model.predict(history_test)
y_test_predicted = y_scaler.inverse_transform(y_test_predicted)

y_predicted = model.predict(history_normalized)
y_predicted = y_scaler.inverse_transform(y_predicted)

real_mse = np.mean(np.square(unscaled_y - y_test_predicted))
scaled_mse = real_mse / (np.max(unscaled_y) - np.min(unscaled_y)) * 100
print(scaled_mse)

assert unscaled_y.shape == y_test_predicted.shape

# %%
plt.plot(unscaled_y[0:-1], scalex=True, label='real')
plt.plot(y_test_predicted[0:-1], scalex=True, label='predicted')
plt.legend(['Real', 'Predicted'])
# %%
plt.show()

# %%
plt.plot(next_day_values[0:-1], scalex=True, label='real')
plt.plot(y_predicted[0:-1], scalex=True, label='predicted')
plt.legend(['Real', 'Predicted'])
# %%
plt.show()