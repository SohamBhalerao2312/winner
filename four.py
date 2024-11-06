# -*- coding: utf-8 -*-
"""four

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hx7P0jDcQMHTAyKhGeSh21jX7fHM2rLN
"""

#Time Series Analysis with LSTM using python’s keras Library
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
# Generate synthetic time series data
def generate_time_series(batch_size, n_steps):
  freq1, freq2, offsets1, offsets2 = np.random.rand(4, batch_size, 1)
  time = np.linspace(0, 1, n_steps)
  series = 0.5 * np.sin((time - offsets1) * (freq1 * 10 + 10)) # wave 1
  series += 0.2 * np.sin((time - offsets2) * (freq2 * 20 + 20)) # wave 2
  series += 0.1 * (np.random.rand(batch_size, n_steps) - 0.5) # noise
  return series[..., np.newaxis].astype(np.float32)
# Prepare the data
n_steps = 50
X_train = generate_time_series(10000, n_steps)
X_valid = generate_time_series(2000, n_steps)
X_test = generate_time_series(2000, n_steps)
# We are predicting the next value in the time series, so y is shifted by one timestep.
y_train = X_train[:, -1, 0] # predicting the last value of the series
y_valid = X_valid[:, -1, 0]
y_test = X_test[:, -1, 0]
# Build a 1D CNN model for time series prediction
model = models.Sequential()
# 1D Convolutional Layer for time series data
model.add(layers.Conv1D(filters=64, kernel_size=5, strides=1,
padding='causal', activation='relu', input_shape=[n_steps, 1]))
model.add(layers.Conv1D(filters=64, kernel_size=5, strides=1,
padding='causal', activation='relu'))
# Flatten the output and pass it to a Dense layer
model.add(layers.GlobalAveragePooling1D())
model.add(layers.Dense(1))
# Compile the model
model.compile(optimizer='adam', loss='mse')
# Train the model
history = model.fit(X_train, y_train, epochs=20, validation_data=(X_valid,
y_valid))
# Evaluate the model
test_loss = model.evaluate(X_test, y_test)
print(f'Test Loss: {test_loss}')
# Plot the training and validation loss
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()
# Make predictions on the test data
y_pred = model.predict(X_test)
# Plot the predicted vs actual values for the first time series in the test set
plt.plot(y_test[:100], label="Actual")
plt.plot(y_pred[:100], label="Predicted")
plt.xlabel('Time step')
plt.ylabel('Value')
plt.legend()
plt.show()