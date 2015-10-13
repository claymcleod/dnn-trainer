import os
import numpy as np
import pandas as pd
from tasks import test_dnn
from flask import *


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
    X_train = features.as_matrix()
    y_train = labels.as_matrix()

    y_train = y_train.reshape( -1, 1 )

    input_size = X_train.shape[1]
    target_size = 3

    new_y_train = []
    for i in range(0, y_train.shape[0]):
        if int(y_train[i][0]) == 0:
            new_y_train.append([1, 0, 0])
        elif int(y_train[i][0]) == 1:
            new_y_train.append([0, 1, 0])
        elif int(y_train[i][0]) == 2:
            new_y_train.append([0, 0, 1])


    ds = SupervisedDataSet( input_size, target_size )
    ds.setField( 'input', X_train )
    ds.setField( 'target', new_y_train )

    hidden_size = 10   # arbitrarily chosen

    net = buildNetwork( input_size, hidden_size, target_size, bias = True, recurrent=True)
    trainer = BackpropTrainer( net, ds )

    tasks = []
    for i in range(0, 1000):
        print "{}".format(i)
        tasks.append(test_dnn.delay(ds, net, trainer, X_train, y_train, session_id))

    print "Done"
    return jsonify(session_id=session_id)

if __name__ == '__main__':
  app.debug=True
  app.run(
        host="0.0.0.0",
        port=int("8000")
  )
