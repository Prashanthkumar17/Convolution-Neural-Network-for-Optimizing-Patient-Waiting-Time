# -*- coding: utf-8 -*-
"""ANN_CNN_Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CS3-GGAZEADBpwsiP0c6Pd2lrnxWmibw
"""

from google.colab import drive
drive.mount('/content/drive/')

import keras
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn import metrics

# To generate pseudo-random numbers
np.random.seed(3)

X_CNN = np.empty([1000, 50, 50])
X_ANN = np.empty([1000, 2500])
y = np.empty([1000])
data_path = "/content/drive/My Drive/ANNCNN/ANNCNN/DS/"
for i in range(1000):
    dataset = pd.read_csv(data_path + 'data'+str(i)+'.csv')
    datasetNo_header = dataset.to_csv(header=None,index=False)
    X_CNN[i] = np.reshape(np.array((datasetNo_header.replace("[",'').replace("]","").replace('\n',"")).split()), (-1,50))
    X_ANN[i] = np.array((datasetNo_header.replace("[",'').replace("]","").replace('\n',"")).split())
    y[i] = np.array((dataset.columns[0].split(":"))[1])
    
# Spliting data into 80% for training & 20% for testing
X_train_CNN, X_test_CNN, X_train_ANN, X_test_ANN, y_train, y_test = train_test_split(X_CNN, X_ANN, y, test_size=0.2, random_state=32)

# Displaying shape of data
X_CNN.shape, X_ANN.shape, y.shape

# Displaying shape of training and testing data
X_train_CNN.shape, X_test_CNN.shape, X_train_ANN.shape, X_test_ANN.shape, y_train.shape, y_test.shape

"""# Applying Feature  Scaling"""

# It outputs maximum X value from X_CNN data
X_valuemax = np.amax(X_CNN)
# It oputputs maximum Y value from Y_CNN data
Y_valuemax = np.amax(y)
print(X_valuemax, Y_valuemax)

# Coverting all the values in x and y training and testing dataset to range between 0 and 1 by dividing each 
# and every value by maximum value
X_train_CNN = X_train_CNN.astype('float32')/X_valuemax
X_test_CNN  = X_test_CNN.astype('float32')/X_valuemax
X_train_ANN = X_train_ANN.astype('float32')/X_valuemax
X_test_ANN  = X_test_ANN.astype('float32')/X_valuemax
y_train   = y_train.astype('float32')/Y_valuemax
y_test    = y_test.astype('float32')/Y_valuemax

"""# Designing Artifical Neural Network (ANN) Model"""

# Spliting data into 80% for training and 20% for testing 
X_trainANN, X_validationANN, y_trainANN, y_validationANN = train_test_split(X_train_ANN, y_train, test_size= 0.2, random_state=2025)

# Displaying the shape of training and validation data
X_trainANN.shape,  X_validationANN.shape, y_trainANN.shape,y_validationANN.shape

# Create ANN model using keras
ANN_model = Sequential()
# Adding dense layer to model
ANN_model.add(Dense(16, input_dim=2500, kernel_initializer='normal', activation='relu'))
ANN_model.add(Dense(1, kernel_initializer='normal'))
# Compile model using adam optimizer
ANN_model.compile(loss='mean_squared_error', optimizer='adam')

#fit the model by inputing traing and testing data to the network
ANN_model.fit(X_trainANN, y_trainANN, epochs = 100, batch_size=64, validation_data=(X_validationANN, y_validationANN))

# saving the ANN model
ANN_model.save('1116540-ANN.h5')

"""# Designing CNN Model"""

# It displays the demension of CNN training and testing datasets
X_train_CNN.ndim, X_test_CNN.ndim

# Expanding the 3-dimension to 4-dimension array
X_train_CNN = np.expand_dims(X_train_CNN, -1)
X_test_CNN = np.expand_dims(X_test_CNN, -1)

# It displays the dimension of CNN datasets
X_train_CNN.ndim, X_test_CNN.ndim

#Spliting the data into training and validation
X_train_CNN, X_validation_CNN, y_train_CNN, y_validation_CNN = train_test_split(X_train_CNN, y_train, test_size= 0.2, random_state=2025)

#Displays the shape of training and validation data
X_train_CNN.shape,  X_validation_CNN.shape, y_train_CNN.shape, y_validation_CNN.shape

# Creatinging CNN model using keras 
CNN_model = keras.models.Sequential([
                         keras.layers.Conv2D(filters=64, kernel_size=3, strides=(1,1), padding='valid',activation= 'relu', input_shape=[50,50,1]),
                         keras.layers.MaxPooling2D(pool_size=(2,2)),
                         keras.layers.Flatten(),
                         keras.layers.Dense(units=128, activation='relu'),
                         keras.layers.Dense(units=1, activation='linear')
])

CNN_model.summary()

# complieing the cnn model using adam optimizer
CNN_model.compile(loss='mean_squared_error', optimizer='adam')

# fit the model using training and testing data
CNN_model.fit(X_train_CNN, y_train_CNN, epochs=80, batch_size=256, verbose=1, validation_data=(X_validation_CNN, y_validation_CNN))

# saving the CNN model
CNN_model.save('1116540-CNN.h5')

"""# Load the models to display predictive performance"""

# Commented out IPython magic to ensure Python compatibility.
from keras.models import load_model
import matplotlib.pyplot as plt
# %matplotlib inline

load_ANN_model = load_model('1116540-ANN.h5')
# Predictive ANN
predict_ANN = load_ANN_model.predict(X_test_ANN)
figure, axis = plt.subplots()
axis.scatter(y_test, predict_ANN)
axis.plot([y_test.min(), y_test.max()], [predict_ANN.min(), predict_ANN.max()], 'k--', lw=4)
axis.set_xlabel('True')
axis.set_ylabel('Predicted')
plt.show()

load_CNN_model = load_model('1116540-CNN.h5')

# Predict CNN
predict_CNN = load_CNN_model.predict(X_test_CNN)
figure, axis = plt.subplots()
axis.scatter(y_test, predict_CNN)
axis.plot([y_test.min(), y_test.max()], [predict_CNN.min(), predict_CNN.max()], 'k--', lw=4)
axis.set_xlabel('True')
axis.set_ylabel('Predicted')
plt.show()

"""# Comparision of Predictive Performance of Two Models"""

from sklearn import metrics

# Comparing the prediction performance of ANN and CNN using performance metrics

# Mean Square Error error performance metric.  
MSE = metrics.mean_squared_error(predict_ANN, predict_CNN)
print("Mean Square Error: ",MSE)

# Root Mean Square Error error metric
RMSE = np.sqrt(metrics.mean_squared_error(predict_ANN, predict_CNN))
print("Root Mean Square Error: ",RMSE)

# Mean Absolute Error metric
MAE = metrics.mean_absolute_error(predict_ANN, predict_CNN)
print("Mean Absolute Error: ",MAE)



