## Description
A simple experiment on distributed training using TensorFlow and Horovod.

`docker run -dp 8887:8888 --name distributed_training --rm daveduke/distributed_training` \
`docker exec -it distributed_training bash` \
`pipenv run horovodrun -np 3 -H localhost:3 --timeline-filename ./timeline.json --timeline-mark-cycles python horovod_train.py 2> /dev/null`

## Requirements
* docker

## Usage
1) Pull and run the image \
`docker run -dp 8887:8888 --name distributed_training --rm daveduke/distributed_training` 
2) Run a training script
* One node training may be ran inside the jupyter notebook at `localhost:8887` or calling \
`docker exec -it distributed_training bash` \
`pipenv run horovodrun -np 1 -H localhost:1 python horovod_train.py 2> /dev/null`
* To train the model using three nodes working concurently one should run
`docker exec -it distributed_training bash` \
`pipenv run horovodrun -np 3 -H localhost:3 --timeline-filename ./timeline.json --timeline-mark-cycles python horovod_train.py 2> /dev/null`

## Experiment results
This graph shows lines that I prefer to interprete as consequent calls by three concurrent training processes.

## Known issues
Although all the experiments run in a docker container, some packages may depend on the instruction set of particular CPU. If some of the training scripts fail to run, try rebuilding the image, calling `docker build .`, inside the repository folder.
