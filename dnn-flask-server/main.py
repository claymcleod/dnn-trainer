import os
import numpy as np
import pandas as pd
from tasks import test_dnn
from flask import *
import timeit

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from pybrain import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import RecurrentNetwork
import numpy
from bson.json_util import dumps
from pymongo import MongoClient
client = MongoClient('mongodb://129.114.108.156:27017/dnn')
db = client.dnn_results

app = Flask("Deep Neural Net Training Flask Server", static_url_path='')

# @app.route('/start/', methods=['GET'])
# def hello():
#     layers = np.random.choice(dropouts, np.random.randint(0, len(dropouts) - 1))
#     result = test_dnn.delay(layers)
#     found = "Randomly chose %d layers" % result.get()
#     return jsonify(message=found)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/view/<int:session_id>')
def view(session_id):
    return app.send_static_file('view.html')

# @app.route('/start', methods=['POST'])
# def upload():
#     session_id = np.random.randint(0, 50000)
#     label_name = request.json["label"]
#     del request.json["label"]
#
#     data = request.json["data"]
#     columns = data[0]
#     del data[0]
#
#     features = pd.DataFrame(data, columns=columns)
#     features.fillna(0)
#
#     labels = features[label_name]
#     del features[label_name]
#
#     print features.columns
#
#     X = features.as_matrix()
#     y = labels.as_matrix()
#
#     ss = StandardScaler()
#     X = ss.fit_transform(X)
#
#     ohe = OneHotEncoder()
#     y = ohe.fit_transform(y.reshape( -1, 1 )).toarray()
#
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1337)
#
#     input_size = X_train.shape[1]
#     target_size = y_train.shape[1]
#
#     ds = SupervisedDataSet( input_size, target_size )
#     for (i, t) in zip(X_train, y_train):
#         ds.addSample(i, t)
#
#     tasks = []
#     for i in range(1, 50000):
#         print i
#         options = {
#             "session_id": session_id,
#             "hidden_size": i,#numpy.random.randint(0, 5000),
#             "max_epochs": 2000,
#             "recurrent": True, #np.random.rand() > .5,
#             "bias": True, #np.random.rand() > .5
#         }
#
#         tasks.append(test_nn.delay(ds, X_train, y_train, X_test, y_test, options))
#
#     return jsonify(session_id=session_id)

@app.route('/start', methods=['POST'])
def upload():
    session_id = np.random.randint(0, 50000)
    label_name = request.json["label"]
    del request.json["label"]

    data = request.json["data"]
    columns = data[0]
    del data[0]

    features = pd.DataFrame(data, columns=columns)
    features.fillna(0)

    labels = features[label_name]
    del features[label_name]

    print features.columns

    X = features.as_matrix()
    y = labels.as_matrix()

    ss = StandardScaler()
    X = ss.fit_transform(X)

    ohe = OneHotEncoder()
    y = ohe.fit_transform(y.reshape( -1, 1 )).toarray()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1337)

    input_size = X_train.shape[1]
    target_size = y_train.shape[1]

    ds = SupervisedDataSet( input_size, target_size )
    for (i, t) in zip(X_train, y_train):
        ds.addSample(i, t)

    tasks = []
    for i in range(1, 1000):
        print i
        options = {
            "session_id": session_id,
            "hidden_size": np.random.randint(0, 5000),
            "max_epochs": 1000
        }
        tasks.append(test_dnn.delay(ds, X_train, y_train, X_test, y_test, options))

    return jsonify(session_id=session_id)

@app.route('/api/')
def api():
    res = db.results.find({})
    return dumps(res)

@app.route('/api/<int:session_id>')
def api_session(session_id):
    res = db.results.find({'session_id': session_id})
    json = dumps(res)
    return json

@app.route('/fft/<int:session_id>')
def fft(session_id):
    accuracies = []
    for r in db.results.find({'session_id': session_id}):
        accuracies.append(r["result"])

    return dumps(abs(numpy.fft.fft(accuracies)))

if __name__ == '__main__':
  app.debug=True
  app.run(
        host="0.0.0.0",
        port=int("8000")
  )
