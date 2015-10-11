all:
	sudo docker build --no-cache=true -t claymcleod/dnn-trainer .
	sudo docker stop $(sudo docker ps -a -q)
	sudo docker rm $(sudo docker ps -a -q)
	for i in {1..5}; do sudo docker run -d claymcleod/dnn-trainer; done
