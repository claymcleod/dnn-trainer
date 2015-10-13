from pymongo import MongoClient
from celery import Celery
from pybrain import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import RecurrentNetwork
import numpy



client = MongoClient('mongodb://129.114.108.156:27017/dnn')
db = client.dnn_results

app = Celery('dnn', backend='amqp://guest@129.114.108.156//', broker='amqp://guest@129.114.108.156//')

@app.task(ignore_result=True)
def test_dnn(ds, net, trainer, X_train, y_train, session_id):
    trainer.trainUntilConvergence(validationProportion = 0.15, maxEpochs = 100)

    objective_score = net.activateOnDataset( ds )
    incorrect = 0.0
    for i in range(X_train.shape[0]):
        pred = net.activate(X_train[i, :])
        if int(y_train[i][0]) != int(pred.argmax()):
            incorrect = incorrect + 1

    objective_score = 100.0 - (float(incorrect) / float(X_train.shape[0]))
    db.results.insert_one({
        'session_id': session_id,
        'result': objective_score
    })

    return objective_score
