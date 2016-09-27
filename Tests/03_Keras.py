from keras.models import Sequential
from keras.layers import Activation, Dense

model = Sequential()

model.add(Dense(output_dim=64, input_dim=100))
model.add(Activation("relu"))
model.add(Dense(output_dim=10))
model.add(Activation("softmax"))

# need:
# X_train, Y_train and X_test, Y_test

#model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
#from keras.optimizers import SGD
#model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True))

#model.fit(X_train, Y_train, nb_epoch=5, batch_size=32)
#model.train_on_batch(X_batch, Y_batch)

#loss_and_metrics = model.evaluate(X_test, Y_test, batch_size=32)

#classes = model.predict_classes(X_test, batch_size=32)
#proba = model.predict_proba(X_test, batch_size=32)
