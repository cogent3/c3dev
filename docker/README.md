# Developing Cogent3 in a docker container

## install docker 

## Build docker image for development

Build a docker image in your repository from c3dev.DockerFile in this folder and name it c3dev (with the tag command).  Note the current directory should be the one that contains the c3dev.DockerFile configuration file and the entrypoint.sh script.  If not replace the final . with the path to the directory that contains those files.

```bash
    docker build --tag c3dev -f docker/c3dev.DockerFile . 
```

## Running a docker container for development

To run a docker container for development, you need to mount the root directory of the clone of your fork of the cogent3 repository into the container, and also mount your ssh key (saved to `$env:USERPROFILE/.ssh/github`) for accessing that fork into the container.

The following assumes your current directory is the root directory of your clone of the cogent3 repository.  If not you can replace the {PWD} macro with the path to the root directory of your clone of the cogent3 repository.

```sh
    docker run -it --rm -v ${PWD}:/cogent3 c3dev -v $env:USERPROFILE/.ssh/github:/root/.ssh/id_rsa -p 3000:3000 --name cogent3dev c3dev /bin/bash
```

Note: This will also set up port mapping of port 3000 so that you attach to the container with VS code  

## Build a docker image for profiling cogent3 in a container on your docker host

You have to first have built a docker image for development as described above, as the profile image is built from the development image.

Build a docker image in your repository from c3prof.DockerFile in this folder and name it c3prof (with the tag command) as follows.  Note the current directory should be the one that contains the c3dev.DockerFile and c3prof.DockerFile configuration files and the entrypoint.sh script.  If not replace the final . with the path to the directory that contains those files.

```bash
    docker build --tag c3prof -f docker/3prof.DockerFile . 
```

## Running a docker container for profiling cogent3 in a container on your docker host

To run a docker container for profiling cogent3 in a container on your docker host, you need to mount the root directory of the clone of your fork of the cogent3 repository into the container, and also mount your ssh key for accessing that fork into the container.

The following assumes your current directory is the root directory of your clone of the cogent3 repository.  If not you can replace the {PWD} macro with the path to the root directory of your clone of the cogent3 repository.

```sh
    docker run --rm -v ${PWD}:/cogent3 c3prof -v $env:USERPROFILE/.ssh/github:/root/.ssh/id_rsa --name cogent3prof c3prof 
```