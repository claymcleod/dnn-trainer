all:
	sudo docker pull claymcleod/dnn-base:latest
	sudo docker build --no-cache -t claymcleod/dnn-worker .
	for i in {1..21}; do sudo docker run -d claymcleod/dnn-worker; done
