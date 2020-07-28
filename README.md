## Description
A simple experiment on distributed training on CPU using TensorFlow and Horovod.
Docker image containes a baseline script to run training on one node and a distributed training script that can be ran in one worker.

## Requirements
* docker

## Usage
1) Pull and run the image \
`docker run -dp 8887:8888 --name distributed_training --rm daveduke/distributed_training` 
2) Run a training script
* One node training may be run inside the jupyter notebook at `localhost:8887` or calling \
`docker exec -it distributed_training bash` \
`pipenv run horovodrun -np 1 -H localhost:1 python horovod_train.py 2> /dev/null`
* To train the model using three nodes working concurently one should run
`docker exec -it distributed_training bash` \
`pipenv run horovodrun -np 3 -H localhost:3 --timeline-filename ./timeline.json --timeline-mark-cycles python horovod_train.py 2> /dev/null`

## Experiment results
This graphs shows Horovod timeline visualization:
* Allreduce calls merging weights 
![alt text](https://github.com/IgorDavidyuk/distributed_training/blob/master/images/Screen%20Shot%202020-07-28%20at%2016.47.39.png)
* Broadcast calls updating weights of every worker to averaged values
![alt text](https://github.com/IgorDavidyuk/distributed_training/blob/master/images/Screen%20Shot%202020-07-28%20at%2016.48.20.png)

## Known issues
* Although all the experiments run in a docker container, training behavior sometimes depends on a particular machine. For instance, available RAM may be not enough to run training scripts with deafault settings. If some of the training scripts fail to run, try decreasing the batch size in debug mode, calling `docker-compose up --build -d`, inside the repository folder.
* Distributed training results for some reason is not deterministic. The differences in loss behavior from run to run may not be explained solely by errors in operations with floating-point weights or a random seed changes.
