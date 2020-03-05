import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, LSTM
from datetime import datetime, date, timedelta
import tensorflow.python.util.deprecation as depreciation
import math

depreciation._PRINT_DEPRECATION_WARNINGS = False

class StockPredictor():

    def __init__(self, split_value, backward_batch_size, model_name, dataframe_file):
        self.split_value = split_value
        self.backward_batch_size = backward_batch_size
        self.model_name = model_name
        self.dataframe_file = dataframe_file

        self.scaler = MinMaxScaler(feature_range=(0, 1))

    """
    The model featured in this class is a pretty simple one,
    it has two layers of LSTM (Long Short Term Memory) cells
    followed by a dense layer that ties everything together 
    for the output.

    I chose to make the model and the predictions on a single stock
    and I chose IBM. Considering the low amount of data that was
    available (around 25 entries) the training is made in only one epoch.

    The principle of this model is its train set.
    The train set is made out of entries with length 4 and
    the target value is the fifth value from the set.

    Example for better understanding:
    If I have a time series of [1, 2, 3, 4, 5, 6]
    for the first element of x_train I will have
    [1, 2, 3, 4] and y_train will be 5.
    for the second element of x_train I will have
    [2, 3, 4, 5] and y_train will be 6.

    This principle is also used in the prediction of a distant date.

    """
    def train(self, filename):

        df = pd.read_csv(filename)
        aux_df = df[df['stock']=='IBM']
        
        aux_df = aux_df.reset_index(drop=True)
        
        df_ibm = pd.DataFrame(index=range(0, len(aux_df)), columns = ['date', 'close'])

        for i in range(0, len(aux_df)):
            df_ibm['date'][i] = datetime.strptime(aux_df['date'][i], '%m/%d/%Y').date()
            df_ibm['close'][i] = aux_df['close'][i]

        df_ibm.index = df_ibm['date']
        df_ibm.drop('date', axis=1, inplace=True)

        dataset = df_ibm.values

        train = dataset[0:self.split_value]
        test = dataset[self.split_value:]

        x_train, y_train = [], []
        
        scaled_data = self.scaler.fit_transform(dataset)

        for i in range(self.backward_batch_size, len(train)):
            x_train.append(scaled_data[i - self.backward_batch_size:i, 0])
            y_train.append(scaled_data[i, 0])

        x_train = np.array(x_train)
        y_train = np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
        model.add(LSTM(units=50))
        model.add(Dense(1))

        model.compile(loss='mean_squared_error', optimizer='adam')

        model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

        model.save(self.model_name)
        df_ibm.to_pickle(self.dataframe_file)

    """
    The following method makes a prediction using a
    saved trained model that it loads from a file.

    It all begins with the target date, considering that
    I compute the difference of days between the last known value
    and the target one. The difference obtained is divided by 7
    and floored, the reason for this is that the data provided
    has a time frame of a week, one entry per week.

    After the difference of weeks is obtained, the predictor
    goes into a for loop, predicting values week after week
    until we obtain a value from the targeted week.

    After the loop closes, we simply return the last value predicted,
    which is the furthest one in the timeseries. There is no need to
    go futher if we reached the desired week to predict.
    """
    def predict(self, date):

        model = load_model(self.model_name)
        df_ibm = pd.read_pickle(self.dataframe_file)
        dataset = df_ibm.values
        scaled_data = self.scaler.fit_transform(dataset)
        
        target_date = datetime.strptime(date, '%Y-%m-%d').date()
        difference = math.floor(abs((target_date - df_ibm.index.values.tolist()[-1]).days) / 7)

        for i in range(0, difference):

            inputs = df_ibm[len(df_ibm) - self.backward_batch_size:].values
            inputs = inputs.reshape(-1, 1)
            inputs = self.scaler.transform(inputs)

            x_test = []
            for i in range(self.backward_batch_size, inputs.shape[0] + 1):
                x_test.append(inputs[i - self.backward_batch_size:i, 0])
            
            x_test = np.array(x_test)
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

            closing_price = model.predict(x_test)
            closing_price = self.scaler.inverse_transform(closing_price)

            df_test = pd.DataFrame(closing_price[0], columns=['close'])
            df_test.index = [df_ibm.index.values.tolist()[-1] + timedelta(days=7)]
            df_ibm = df_ibm.append(df_test)

        return df_ibm['close'].iloc[-1]
