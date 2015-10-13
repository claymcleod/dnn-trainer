FROM claymcleod/dnn-base
RUN pip install pymongo
WORKDIR dnn-trainer/dnn-flask-server
RUN git pull
ENV C_FORCE_ROOT=True
CMD for i in {1..200}; celery -A tasks worker --loglevel=INFO --concurrency=1; done
