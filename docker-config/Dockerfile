FROM scivm/scientific-python-2.7
RUN pip install celery keras
RUN git clone https://github.com/claymcleod/dnn-trainer.git --depth 1
WORKDIR dnn-trainer/dnn-flask-server
ENV C_FORCE_ROOT=True
CMD celery -A tasks worker --loglevel=INFO --concurrency=100
