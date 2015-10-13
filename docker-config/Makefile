all:
	sudo docker build --no-cache -t claymcleod/dnn-worker .
	sudo for i in {1..10}; do docker run -d claymcleod/dnn-worker; done
