ssh cc@$1 'sudo docker stop -t=1 $(sudo docker ps -a -q) && sudo docker rm $(sudo docker ps -a -q)'
