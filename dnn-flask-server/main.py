import os
import numpy as np
import pandas as pd
from tasks import test_dnn
from flask import *
from werkzeug import secure_filename
from keras.optimizers import *
from keras.models import *
from keras.layers.core import *

app = Flask("Deep Neural Net Training Flask Server", static_url_path='')

app.config['UPLOAD_FOLDER'] = 'data/'

ALLOWED_EXTENSIONS = set(['csv'])

layers = [
    Dense(64, 20)
]

dropouts = [Dropout(x) for x in np.linspace(0, 1, 100)]

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
    label_name = request.json["label"]
    del request.json["label"]

    data = request.json["data"]
    columns = data[0]
    del data[0]

    features = pd.DataFrame(data, columns=columns)
    features.fillna(0)

    labels = features[label_name]
    del features[label_name]
    features = features.as_matrix()
    labels = labels.as_matrix()

    tasks = []
    for i in range(0, 1000):
        print "{}".format(i)
        tasks.append(test_dnn.delay(features, labels, layers, cb=callback))

    print "Done"
    session_id = np.random.randint(0, 50000)
    return jsonify(session_id=session_id)

def callback(result):
    print(result)

if __name__ == '__main__':
  app.debug=True
  app.run(
        host="0.0.0.0",
        port=int("8000")
  )
