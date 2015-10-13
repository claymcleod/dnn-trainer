all:
	sudo docker build --no-cache -t claymcleod/dnn-worker .
	for i in {1..200}; do sudo docker run -d claymcleod/dnn-worker; done
