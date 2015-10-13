all:
	sudo docker build --no-cache -t claymcleod/dnn-worker .
	for i in {1..64}; do sudo docker run -d claymcleod/dnn-worker; done
