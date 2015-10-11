ssh cc@$1 'sudo docker stop $(sudo docker ps -a -q) && sudo docker rm $(sudo docker ps -a -q) && cd ./dnn-trainer/docker-config && sudo service docker restart && make'
