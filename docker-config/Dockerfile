FROM claymcleod/dnn-base:latest
RUN pip install pymongo keras pandas
WORKDIR dnn-trainer/dnn-flask-server
RUN git pull
ENV C_FORCE_ROOT=True
CMD celery -A tasks worker --loglevel=INFO --concurrency=1
