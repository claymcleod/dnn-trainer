from celery import Celery
from keras.optimizers import *
from keras.models import *
from keras.layers.core import *

app = Celery('dnn', backend='amqp://guest@129.114.108.156//', broker='amqp://guest@129.114.108.156//')

@app.task
def test_dnn(layers):
    return len(layers)
