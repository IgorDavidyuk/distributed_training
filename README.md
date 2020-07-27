# distributed_training
A simple experiment on distributed training in TensorFlow.

docker run -dp 8887:8888 --name distributed_training daveduke/distributed_training
docker exec -it distributed_training bash
pipenv run horovodrun -np 3 -H localhost:3 --timeline-filename ./timeline.json --timeline-mark-cycles python horovod_train.py 2> /dev/null