from pymongo import MongoClient
from celery import Celery
from pybrain import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import RecurrentNetwork
import numpy
import timeit

client = MongoClient('mongodb://129.114.108.156:27017/dnn')
db = client.dnn_results

app = Celery('dnn', backend='amqp://guest@129.114.108.156//', broker='amqp://guest@129.114.108.156//')

@app.task(ignore_result=True)
def test_dnn(ds, X_train, y_train, X_test, y_test, options):
    hidden_size = options["hidden_size"]

    net = buildNetwork( X_train.shape[1], hidden_size, y_train.shape[1], bias = options["bias"], recurrent=options["recurrent"])
    trainer = BackpropTrainer( net, ds )
    start = timeit.timeit()
    trainer.trainUntilConvergence(validationProportion = 0.15, maxEpochs = options["max_epochs"])
    end = timeit.timeit()

    objective_score = net.activateOnDataset( ds )
    incorrect = 0.0
    for i in range(X_test.shape[0]):
        pred = net.activate(X_test[i, :])
        if int(y_test[i][0]) != int(pred.argmax()):
            incorrect = incorrect + 1

    objective_score = 100.0 - (float(incorrect) / float(X_train.shape[0]))
    options["result"] = objective_score
    options["training_time"] = end - start
    db.results.insert_one(options)

    return objective_score
