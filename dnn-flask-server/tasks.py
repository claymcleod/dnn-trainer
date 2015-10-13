from celery import Celery
from pymongo import MongoClient

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import PReLU
from keras.utils import np_utils, generic_utils

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn import cross_validation

client = MongoClient('mongodb://129.114.108.156:27017/dnn')
db = client.dnn_results

app = Celery('dnn', backend='amqp://guest@129.114.108.156//', broker='amqp://guest@129.114.108.156//')

def preprocess_data(X, scaler=None):
    if not scaler:
        scaler = StandardScaler()
        scaler.fit(X)
    X = scaler.transform(X)
    return X, scaler

@app.task(ignore_result=True)
def test_dnn(X_train, y_train, layers, session_id):
    model = Sequential()

    X_train, scaler = preprocess_data(X_train)

    model.add(Dense(X_train.shape[1], 512))
    model.add(PReLU((512,)))
    model.add(BatchNormalization((512,)))
    model.add(Dropout(0.5))

    model.add(Dense(512, 512))
    model.add(PReLU((512,)))
    model.add(BatchNormalization((512,)))
    model.add(Dropout(0.5))

    model.add(Dense(512, 512))
    model.add(PReLU((512,)))
    model.add(BatchNormalization((512,)))
    model.add(Dropout(0.5))

    model.add(Dense(512, 512))
    model.add(PReLU((512,)))
    model.add(BatchNormalization((512,)))
    model.add(Dropout(0.5))

    model.add(Dense(512, 512))
    model.add(PReLU((512,)))
    model.add(BatchNormalization((512,)))
    model.add(Dropout(0.5))

    model.add(Dense(512, 512))
    model.add(PReLU((512,)))
    model.add(BatchNormalization((512,)))
    model.add(Dropout(0.5))

    model.add(Dense(512, 3))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer="adam")
    model.fit(X, y, nb_epoch=200, batch_size=4, validation_split=0.15, verbose=0)
    objective_score = model.evaluate(X_train, y_train, batch_size=32)
    print("Objective score: {}".format(objective_score))
    db.results.insert_one({
        'session_id': session_id,
        'result': objective_score
    })

    return objective_score
