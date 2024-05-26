# Factory

## Required tools
- Python 3.10
- Docker


### After pulling repository, build docker image using below command in project path.

```shell
docker build --no-cache -t factory-api -f Dockerfile . 
```

### Run Factory backend application using below command.

```shell
docker-compose -f docker/docker-compose.yml up
```