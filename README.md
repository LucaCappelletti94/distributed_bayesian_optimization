# experimenting_on_ray
Trying to understand how to use Ray to run distributed Bayesian Optimization

## Running the server
Start by running:

```bash
docker build --file ServerDockerfile -t experimenting_on_ray .
docker run --shm-size=8GB -t --tty --interactive --network host experimenting_on_ray
```

And then afterwards:

```bash
ray start --head --redis-port=8080
```

## Running the server

```bash
docker build --file ServerDockerfile -t experimenting_on_ray .
docker run --shm-size=8GB -t --tty --interactive experimenting_on_ray
```