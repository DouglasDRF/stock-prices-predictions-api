import numpy as np
from sklearn import preprocessing
from tensorflow import keras
from tensorflow.keras import optimizers
from tensorflow.keras.layers import Dense, Dropout, LSTM, Input, Activation
from tensorflow.keras.models import Model

model_file_path = '/model.h5'
class StocksPredictionModel():

    def __init__(self, history_size=40):

        self.__history_size = history_size
        self.is_trained = False
        self.__technical_indicators = []

        try:
            model = keras.models.load_model(model_file_path)
            self.is_trained = True
        except:
            lstm_input = keras.Input(shape=(self.__history_size, 5))
            x = LSTM(50)(lstm_input)
            x = Dropout(0.2)(x)
            x = Dense(64)(x)
            x = Activation('sigmoid')(x)
            x = Dense(1)(x)
            output = Activation('linear',)(x)
            model = Model(inputs=lstm_input, outputs=output)

            adam = optimizers.Adam(lr=0.0005)
            model.compile(optimizer=adam, loss='mse')
        finally:
            self.__model = model
            
        self.__y_scaler = preprocessing.MinMaxScaler()
    
    def normalize_ochlv_history(self, ochlv_history, training_mode=False):
        normalizer = preprocessing.MinMaxScaler()
        dataset_normalized = normalizer.fit_transform(ochlv_history)
        ochlv_history_normalized = np.array([dataset_normalized[i : i + self.__history_size].copy() for i in range(len(dataset_normalized) - self.__history_size)])

        next_open_values = np.array([ochlv_history.values[:,0][i + self.__history_size].copy() for i in range(len(ochlv_history) - self.__history_size)])
        next_open_values = np.expand_dims(next_open_values, -1)
        
        self.__y_scaler = self.__y_scaler.fit(next_open_values)
        assert ochlv_history_normalized.shape[0] == next_open_values.shape[0]
        
        if training_mode == False:
            return ochlv_history_normalized
        else:
            next_open_normalized = np.array([dataset_normalized[:,0][i + self.__history_size].copy() for i in range (len(dataset_normalized) -  self.__history_size)])
            next_open_normalized = np.expand_dims(next_open_normalized, -1)
            return ochlv_history_normalized, next_open_normalized, next_open_values

    def train(self, dataset):
        ochlv_history_normalized, next_open_normalized, next_open_values = self.normalize_ochlv_history(dataset, True)
        X_train, y_train, X_test, y_test = self.__split_train_test(ochlv_history_normalized, next_open_normalized)
        
        self.__model.fit(x=X_train, y=y_train, batch_size=64, epochs=50, shuffle=True, validation_split=0.1)
        evaluation = self.__model.evaluate(X_test, y_test)
        print(f'Normalized MSE: {evaluation}')

        self.current_accuracy = 100 - self.__eval(X_test, next_open_values[self.__test_n:], ochlv_history_normalized)
        self.__model.save(model_file_path, overwrite=True)
        self.is_trained = True

    def predict(self, X_ochlv_history_normalized):
        normalized_result = self.__model.predict(X_ochlv_history_normalized)
        final_result = self.__y_scaler.inverse_transform(normalized_result)
        return final_result

    def __eval(self, history_test, y_unscaled, full_history):
        y_test_predicted = self.predict(history_test)
        y_predicted = self.predict(full_history)

        real_mse = np.mean(np.square(y_unscaled - y_test_predicted))
        scaled_mse = real_mse / (np.max(y_unscaled) - np.min(y_unscaled)) * 100

        assert y_unscaled.shape == y_test_predicted.shape

        print(f'Real Root Mean Squared: {scaled_mse}%')
        return scaled_mse
        
    def __split_train_test(self, ochlv_history_normalized, next_open_normalized, split_ratio=0.9):

        self.__test_n = int(ochlv_history_normalized.shape[0] * split_ratio)

        history_train = ochlv_history_normalized[:self.__test_n]
        y_train = next_open_normalized[:self.__test_n]

        history_test = ochlv_history_normalized[self.__test_n:]
        y_test = next_open_normalized[self.__test_n:]

        return history_train, y_train, history_test, y_test