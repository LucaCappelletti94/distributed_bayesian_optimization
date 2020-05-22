import logging
import ray
import sys
import os
from distributed_bayesian_optimization import distributed_bo
from custom_loss import custom_loss, space


def loss(config, reporter):
    reporter(loss=config["x"]**2)  # A simple function to optimize


redis_password = sys.argv[1]
ray.init(
    address=os.environ["ip_head"],
    redis_password=redis_password,
    configure_logging=True,
    logging_level=logging.CRITICAL
)

distributed_bo(custom_loss, space, metric="my_custom_loss")

# Then we can close down ray
ray.shutdown()
