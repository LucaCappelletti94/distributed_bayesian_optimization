# experimenting_on_ray
Trying to understand how to use Ray to run distributed Bayesian Optimization

## Testing 

```bash
docker build --file ServerDockerfile -t experimenting_on_ray .
docker run --shm-size=8GB -t --tty --interactive --publish 6666:6666 experimenting_on_ray
```


```bash
ray start --head --redis-port=6666
```