import numpy as np
import matplotlib.pyplot as plt

from model import StocksPredictionModel
from model.data_helper import load_dataset

model = StocksPredictionModel()

dataset = load_dataset('BBDC4')
ochlv_history_normalized = model.normalize_ochlv_history(dataset)

if (model.is_trained is not True):
    model.train(dataset)

######################################## Testing the OO Model ##################################################

y_predicted = model.predict(ochlv_history_normalized)

plt.plot(y_predicted[0:-1], scalex=True, label='predicted')
plt.legend(['Predicted'])
plt.show()
