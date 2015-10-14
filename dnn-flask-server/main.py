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

    X = features.as_matrix()
    y = labels.as_matrix()

    ss = StandardScaler()
    X = ss.fit_transform(X)

    ohe = OneHotEncoder()
    y = ohe.fit_transform(y.reshape( -1, 1 )).toarray()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1337)

    print "Train: {} {} Test: {} {}".format(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

    input_size = X_train.shape[1]
    target_size = y_train.shape[1]

    print 'Input: {} Target: {}'.format(input_size, target_size)
    ds = SupervisedDataSet( input_size, target_size )
    for (i, t) in zip(X_train, y_train):
        print i, t
        ds.addSample(i, t)

    tasks = []
    for i in range(0, 1000):
        options = {
            "session_id": session_id,
            "hidden_size": numpy.random.randint(0, 1000),
            "max_epochs": numpy.random.randint(0, 1000),
            "recurrent": np.random.rand() > .5,
            "bias": np.random.rand() > .5
        }
        print options
        tasks.append(test_dnn.delay(ds, X_train, y_train, X_test, y_test, options))

    print "Done"
    return jsonify(session_id=session_id)

if __name__ == '__main__':
  app.debug=True
  app.run(
        host="0.0.0.0",
        port=int("8000")
  )
