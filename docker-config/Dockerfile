FROM kaggle/python
RUN apt-get install python-dev -y
RUN git clone https://github.com/claymcleod/dnn-trainer.git --depth 1
WORKDIR dnn-trainer/dnn-flask-server
RUN pip install celery keras
ENV C_FORCE_ROOT=True
CMD celery -A tasks worker --loglevel=INFO --concurrency=10
