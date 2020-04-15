# experimenting_on_ray
Trying to understand how to use Ray to run distributed Bayesian Optimization

## Running the server
Start by running:

```bash
docker build --file ServerDockerfile -t experimenting_on_ray_server .
docker run --shm-size=8GB -t --tty --interactive --network host experimenting_on_ray_server
```

And then afterwards:

```bash
ray start --head --redis-port=6379 --redis-shard-ports=6380 --node-manager-port=12345 --object-manager-port=12346
```

## Running the client

```bash
docker build --file ClientDockerFile -t experimenting_on_ray_client .
docker run --shm-size=8GB -t --tty --interactive --network host experimenting_on_ray_client
```

And then afterwards


```bash
ray start --redis-address=address_of_the_server:6379 --node-manager-port=12345 --object-manager-port=12346
```