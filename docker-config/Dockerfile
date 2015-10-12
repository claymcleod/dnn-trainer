FROM claymcleod/dnn-base
WORKDIR dnn-trainer/dnn-flask-server
ENV C_FORCE_ROOT=True
CMD celery -A tasks worker --loglevel=INFO --concurrency=100
