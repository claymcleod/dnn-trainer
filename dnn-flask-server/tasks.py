from celery import Celery
from keras.optimizers import *
from keras.models import *
from keras.layers.core import *
from pymongo import MongoClient

client = MongoClient('mongodb://129.114.108.156:27017/dnn')
db = client.dnn_results

app = Celery('dnn', backend='amqp://guest@129.114.108.156//', broker='amqp://guest@129.114.108.156//')

@app.task(ignore_result=True)
def test_dnn(X_train, y_train, layers, session_id):
    model = Sequential()
    model.add(Dense(output_dim=64, input_dim=X_train.shape[1], init="glorot_uniform"))
    model.add(Activation("softmax"))
    model.add(Dense(output_dim=1, input_dim=64, init="glorot_uniform"))
    model.add(Activation("softmax"))
    model.compile(loss='categorical_crossentropy', optimizer='sgd')
    model.fit(X_train, y_train, nb_epoch=200, batch_size=32)
    objective_score = model.evaluate(X_train, y_train, batch_size=32)
    db.results.insert_one({
        'session_id': session_id,
        'result': objective_score
    })

    return result
