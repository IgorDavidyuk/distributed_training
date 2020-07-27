## Description
A simple experiment on distributed training using TensorFlow and Horovod.

docker run -dp 8887:8888 --name distributed_training daveduke/distributed_training
docker exec -it distributed_training bash
pipenv run horovodrun -np 3 -H localhost:3 --timeline-filename ./timeline.json --timeline-mark-cycles python horovod_train.py 2> /dev/null

## Known issues
Although all the experiments run in a docker container, some packages may depend on instruction set of particullar CPU.
If some of the training script fail to run try rebuilding the image using inside repository folder calling `docker build .`
