
from keras.models import Sequential
from keras.layers import Dense, Activation


model = Sequential()
model.add(Dense(32, input_dim=64))
model.add(Activation('relu'))
model.add(Dense(64)
model.add(Activation('softmax'))




model.compile(optimizer='rmsprop',
		loss='categorical_crossentropy',
		metrics=['accuracy'])















