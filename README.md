# experimenting_on_ray
Trying to understand how to use Ray to run distributed Bayesian Optimization

## Testing 

```bash
docker run --shm-size=16GB -t --tty --interactive --publish 6666:6666 ray-project/base-deps
```