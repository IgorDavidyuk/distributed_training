#!/bin/bash
set -m
# start notebook
jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password='' &

fg %1 # fg shell command continues a stopped job by running it in the foreground
