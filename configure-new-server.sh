ssh cc@$1 'sudo yum upgrade -y && sudo yum install git docker -y && git clone https://github.com/claymcleod/dnn-trainer.git'
