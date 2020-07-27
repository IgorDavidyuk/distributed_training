FROM python:3.6-slim

# installing Open MPI
RUN apt-get update && \
    apt-get -y install make g++ wget ssh
WORKDIR /opt
RUN wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.4.tar.gz
RUN gunzip -c openmpi-4.0.4.tar.gz | tar xf - 
WORKDIR ./openmpi-4.0.4
RUN ./configure --prefix=/usr/local
RUN make all install
ENV LD_LIBRARY_PATH=/usr/local/lib

# set up python environment
RUN python -m pip install --upgrade pip && python -m pip install pipenv
ENV WORK_DIR=/usr/src/app
WORKDIR $WORK_DIR

COPY ./Pipfile* ./
ENV PIP_NO_CACHE_DIR=off
RUN pipenv install

COPY . .
RUN pipenv run python ./prepare_data.py

# WORKDIR ./notebooks
ENTRYPOINT [ "./entrypoint.sh" ]