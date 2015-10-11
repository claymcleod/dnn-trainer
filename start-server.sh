ssh cc@$1 'cd ./dnn-trainer/docker-config && git pull && sudo service docker restart && make'
