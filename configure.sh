ssh cc@$1 'sudo yum upgrade -y && sudo yumg install git && git clone https://github.com/claymcleod/dnn-trainer.git && cd ./dnn-trainer/docker-config && make'
