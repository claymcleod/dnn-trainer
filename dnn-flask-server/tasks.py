from pymongo import MongoClient
from celery import Celery
from pybrain import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import RecurrentNetwork
import numpy
import time

client = MongoClient('mongodb://129.114.108.156:27017/dnn')
db = client.dnn_results

app = Celery('dnn', backend='amqp://guest@129.114.108.156//', broker='amqp://guest@129.114.108.156//')

@app.task(ignore_result=True)
def test_dnn(ds, X_train, y_train, X_test, y_test, options):
    hidden_size = options["hidden_size"]

    net = buildNetwork( X_train.shape[1], hidden_size, y_train.shape[1], bias = options["bias"], recurrent=options["recurrent"])
    trainer = BackpropTrainer( net, ds )
    start = time.time()
    trainer.trainUntilConvergence(validationProportion = 0.15, maxEpochs = options["max_epochs"])
    end = time.time()

    objective_score = net.activateOnDataset( ds )
    incorrect = 0.0
    for i in range(X_test.shape[0]):
        pred = net.activate(X_test[i, :])
        print "Expected: {} Actual: {}".format(y_test[i][0], int(pred.argmax()))
        if int(y_test[i][0]) != int(pred.argmax()):
            incorrect = incorrect + 1

    objective_score = 100.0 - (float(incorrect) / float(X_test.shape[0]) * 100.0)

    print "Incorrect: {} Total: {} Score: {}".format(incorrect, X_test.shape[0], objective_score)

    options["result"] = objective_score
    options["training_time"] = end - start
    options["nodes"] = y_train.shape[1] + hidden_size * (X_train.shape[1] + 1)
    db.results.insert_one(options)

    return objective_score
