# -*- coding: utf-8 -*-
"""six.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14ks_uZlzxW2OGX4YoJ6Jhpc-6hzopvGi
"""

#Sentiment Analysis using LSTMand Glove Embedding
# Importing the necessary libraries
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.datasets import imdb
# Load the IMDB dataset (keeping the top 5000 words)
vocab_size = 5000
maxlen = 100
embedding_dim = 128
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)
# Padding the sequences to a fixed length
X_train = pad_sequences(X_train, maxlen=maxlen)
X_test = pad_sequences(X_test, maxlen=maxlen)
# Build the LSTM model
model = Sequential()
# Embedding layer (vocab size, embedding dimension, input length)
model.add(Embedding(input_dim=vocab_size, output_dim=embedding_dim,
input_length=maxlen))
# Adding an LSTM layer
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
# Fully connected layer
model.add(Dense(1, activation='sigmoid'))
# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy',
metrics=['accuracy'])
# Print the model summary
model.summary()
# Optionally, print output shapes for each layer
# Use model.summary() for a structured output
# Train the model
model.fit(X_train, y_train, epochs=5, batch_size=64, validation_data=(X_test,
y_test))
# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")
from tensorflow.keras.utils import plot_model
plot_model(model, show_shapes=True, to_file='model.png')