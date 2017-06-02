
# coding: utf-8

# In[1]:

import numpy
import process_data


# In[2]:

'''
total_to_train = 5
filename = 'data/matrix_700k.txt'
board, move_from, move_to = process_data.process_data(filename, 0, total_to_train) # [0,total_to_train)



board2 = numpy.array([numpy.append(board[i],move_from[i]) for i in range(len(board))])

# Training data is .8 of the data
percent_train = .8
upper = int(total_to_train*percent_train)

# for training move_from NN
board_train = board[0:upper]
board_test  = board[(upper + 1):total_to_train]
move_from_train = move_from[0:upper]
move_from_test  = move_from[(upper + 1):total_to_train]

# for training move_to NN
board2_train = board2[0:upper]
board2_test  = board2[(upper + 1):total_to_train]
move_to_train = move_to[0:upper]
move_to_test  = move_to[(upper + 1):total_to_train]


'''


# In[4]:

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
import keras.callbacks

class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.batch_counter = 1

    def on_batch_end(self, batch, logs={}):
        if self.batch_counter % 1000 == 0:
            print("LOSS: ",logs.get('loss'),"ACC:",logs.get('acc'))
            self.batch_counter = 1
        self.batch_counter += 1
''' 
From model NN
'''
def get_base_model_from():
        model = Sequential()
        model.add(Dense(144, activation='relu', input_dim=72))
        model.add(Dense(72, activation='relu'))
        model.add(Dense(72, activation='relu'))
        model.add(Dropout(.5))
        model.add(Dense(72, activation='softmax'))       
        model.compile(optimizer='rmsprop',
            loss='categorical_crossentropy',
            metrics=['accuracy']) 
        return model
    
def train_from(num_epoch, b_size, b_per_epoch, history=None):
        model = get_base_model_from()
	
	# Generator to feed training data
	train_gen = process_data.data_generator('data/small_training.txt', batch_size=b_size, to_from='from')

	# Generator to feed validation data
	valid_gen = process_data.data_generator('data/small_validation.txt', batch_size=100, to_from='from')

        model.fit_generator(train_gen, epochs=num_epoch, steps_per_epoch=b_per_epoch, validation_data=valid_gen, validation_steps=50, callbacks=[history], verbose=1)
        return model
    
def test_from(num_epoch):
    model = get_base_model_from()
    model.fit(board_train,move_from_train,epochs=num_epoch, batch_size=500)
    return model.evaluate(board_test, move_from_test, batch_size=500)


'''
To model NN
'''
def get_base_model_to():
        model = Sequential()
        model.add(Dense(288, activation='relu', input_dim=144))
        model.add(Dense(144, activation='relu'))
        model.add(Dropout(.5))
        model.add(Dense(72, activation='softmax'))       
        model.compile(optimizer='rmsprop',
            loss='categorical_crossentropy',
            metrics=['accuracy']) 
        return model
    
def train_to(num_epoch,):
        model = get_base_model_to()
        model.fit(board2_train,move_to_train,epochs=num_epoch, batch_size=500)
        return model
    
def test_to(num_epoch):
    model = get_base_model_to()
    model.fit(board2_train,move_to_train,epochs=num_epoch, batch_size=500)
    return model.evaluate(board2_test, move_to_test, batch_size=500)


# In[12]:

n_epoch = 20
b_size = 1000
batch_per_epoch = 40000
history = LossHistory()
model_from = train_from(n_epoch, b_size, batch_per_epoch, history=None)


# In[ ]:


#model_to = train_to(20)


# In[ ]:

model_from.save('engines/from.h5')
print("DONE!")
#model_to.save('engines/to.h5')


# In[ ]:




# In[ ]:



#model.save('move_to_model.h5')


# In[ ]:

'''
test = board_train[0]
test = test.reshape((1,72))

z = model.predict(test)
z = list(z[0])

results = []
for i in range(len(z)):
    results.append((i,z[i]))
    
re = sorted(results, key = lambda x: x[1], reverse=True)

re
'''


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



