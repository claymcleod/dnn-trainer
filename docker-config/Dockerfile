FROM python
RUN apt-get update && apt-get install python-dev gfortran libblas-dev liblapack-dev python-numpy python-scipy python-matplotlib python-pandas python-sympy python-nose -y
RUN pip install celery keras
RUN git clone https://github.com/claymcleod/dnn-trainer.git --depth 1
WORKDIR dnn-trainer/dnn-flask-server
ENV C_FORCE_ROOT=True
CMD celery -A tasks worker --loglevel=INFO --concurrency=100
