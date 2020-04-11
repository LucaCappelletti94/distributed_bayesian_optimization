# experimenting_on_ray
Trying to understand how to use Ray to run distributed Bayesian Optimization

## Connecting to the server
To connect to the server and afterwards have access to the various dashboards you need to connect with an SHH tunnel as follows:

```bash
ssh -L 8265:localhost:8265 -L 6006:localhost:6006 server_hostname 2> /dev/null
```

The "2> /dev/null" is for capturing the ssh tunnel wining about the services that are yet to be started.

The 8265 port is for the Ray dashboard, while the 6006 port is for the tensorboard dashboard.

## Running the server
Start by running:

```bash
docker build --file ServerDockerfile -t experimenting_on_ray .
docker run --shm-size=8GB -t --tty --interactive --network host experimenting_on_ray
```

And then afterwards:

```bash
ray start --head --redis-port=6379 --redis-shard-ports=6380 --node-manager-port=12345 --object-manager-port=12346
```

## Running the client

```bash
docker build --file ServerDockerfile -t experimenting_on_ray .
docker run --shm-size=8GB -t --tty --interactive experimenting_on_ray
```

And then afterwards


```bash
ray start --address=address_of_the_server:6379 --node-manager-port=12345 --object-manager-port=12346
```
