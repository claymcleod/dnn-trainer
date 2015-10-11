all:
	sudo docker build --no-cache=true -t claymcleod/dnn-trainer .
	for i in {1..5}; do sudo docker run -d claymcleod/dnn-trainer; done
