import numpy as np
import os, boto3
import datetime as dt
import tensorflow as tf
from sklearn import preprocessing
from tensorflow import keras
from tensorflow.keras import optimizers
from tensorflow.keras.layers import Dense, Dropout, LSTM, Input, Activation
from tensorflow.keras.models import Model

if not os.path.exists(os.getcwd() + '\\trained_models'):
    os.makedirs(os.getcwd() + '\\trained_models')

try:
    physical_devices = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
except:
    pass

class StocksPredictionModel():

    def __init__(self, history_size=40):

        self.is_trained = False
        self.tickers_on_trainning = []
        self.__history_size = history_size
        self.current_accuracy = 0
        self.__technical_indicators = []
        self.__y_scaler = preprocessing.MinMaxScaler()

        try:
            model = keras.models.load_model(last_model)
            self.is_trained = True
            print('Model is loaded and trained')
        except Exception as e:
            lstm_input = keras.Input(shape=(self.__history_size, 5))
            x = LSTM(50)(lstm_input)
            x = Dropout(0.2)(x)
            x = Dense(64)(x)
            x = Activation('sigmoid')(x)
            x = Dense(1)(x)
            output = Activation('linear',)(x)
            model = Model(inputs=lstm_input, outputs=output)

            adam = optimizers.Adam(learning_rate=0.0005)
            model.compile(optimizer=adam, loss='mse')
            print('Could not load model:')
            print(e)
            print('Model is created from scratch and needs to be trained')
        finally:
            self.__model = model

    def normalize_ochlv_history(self, ochlv_history, training_mode=False):
        normalizer = preprocessing.MinMaxScaler()
        dataset_normalized = normalizer.fit_transform(ochlv_history)

        if training_mode == False:
            ochlv_history_normalized = np.array(dataset_normalized.copy())

            next_day_values = np.array(ochlv_history.values[:, 1].copy())
            next_day_values = np.expand_dims(next_day_values, -1)

            self.__y_scaler = self.__y_scaler.fit(next_day_values)
            assert ochlv_history_normalized.shape[0] == next_day_values.shape[0]

            return ochlv_history_normalized.reshape(1, 40, 5)
        else:
            ochlv_history_normalized = np.array([dataset_normalized[i: i + self.__history_size].copy(
            ) for i in range(len(dataset_normalized) - self.__history_size)])

            next_day_values = np.array([ochlv_history.values[:, 1][i + self.__history_size].copy()
                                       for i in range(len(ochlv_history) - self.__history_size)])
            next_day_values = np.expand_dims(next_day_values, -1)

            self.__y_scaler = self.__y_scaler.fit(next_day_values)
            assert ochlv_history_normalized.shape[0] == next_day_values.shape[0]

            next_day_normalized = np.array([dataset_normalized[:, 1][i + self.__history_size].copy()
                                           for i in range(len(dataset_normalized) - self.__history_size)])
            next_day_normalized = np.expand_dims(next_day_normalized, -1)

            return ochlv_history_normalized, next_day_normalized, next_day_values

    def train(self, dataset, save=False):
        ochlv_history_normalized, next_open_normalized, next_open_values = self.normalize_ochlv_history(
            dataset, True)
        X_train, y_train, X_test, y_test = self.__split_train_test(
            ochlv_history_normalized, next_open_normalized)

        self.__model.fit(x=X_train, y=y_train, batch_size=64,
                         epochs=50, shuffle=True, validation_split=0.1)
        evaluation = self.__model.evaluate(X_test, y_test)
        print(f'Normalized MSE: {evaluation}')

        self.current_accuracy = 100 - \
            self.evaluate(X_test, next_open_values[self.__test_n:])

        if save == True:
            file_model_name = 'model-' + dt.datetime.now().isoformat().replace(':', '-') + '.h5'
            self.__model.save(models_path + file_model_name, overwrite=True)
            s3.upload_file(models_path + file_model_name, BUCKET_NAME, file_model_name)
            self.is_trained = True
            return file_model_name
        else:
            self.is_trained = True

    def predict(self, X_ochlv_history_normalized):
        normalized_result = self.__model.predict(X_ochlv_history_normalized)
        final_result = self.__y_scaler.inverse_transform(normalized_result)
        return final_result

    def evaluate(self, history_test, y_unscaled):
        y_test_predicted = self.predict(history_test)

        real_mse = np.mean(np.square(y_unscaled - y_test_predicted))
        scaled_mse = real_mse / (np.max(y_unscaled) - np.min(y_unscaled)) * 100

        assert y_unscaled.shape == y_test_predicted.shape

        print(f'Real Root Mean Squared: {scaled_mse}%')
        self.current_accuracy = scaled_mse
        return scaled_mse

    def __split_train_test(self, ochlv_history_normalized, next_open_normalized, split_ratio=0.9):

        self.__test_n = int(ochlv_history_normalized.shape[0] * split_ratio)

        history_train = ochlv_history_normalized[:self.__test_n]
        y_train = next_open_normalized[:self.__test_n]

        history_test = ochlv_history_normalized[self.__test_n:]
        y_test = next_open_normalized[self.__test_n:]

        return history_train, y_train, history_test, y_test


BUCKET_NAME = 'stock-predictions'
s3 = boto3.client('s3')
response = s3.list_objects_v2(Bucket=BUCKET_NAME)
last_model_key = None

models_path = os.getcwd()
models_path = models_path + ('\\trained_models\\' if '\\' in models_path else '/trained_models/')

if response['KeyCount'] > 0:
    last_model_key = response['Contents'][-1]['Key']
    s3.download_file(BUCKET_NAME, last_model_key, models_path + last_model_key)

def get_trained_models():
    return os.listdir(models_path)

last_model = models_path + get_trained_models()[-1] if len(get_trained_models()) else ''

__static_model_instance = StocksPredictionModel()

def get_model_instance() -> StocksPredictionModel:
    return __static_model_instance
