import ray
import logging
import shutil
from distributed_bayesian_optimization import distributed_bo


def loss(config, reporter):
    x = config.get("x")
    reporter(loss=x)  # A simple function to optimize


def test_distributed_bo():
    ray.init(
        configure_logging=True,
        logging_level=logging.CRITICAL
    )

    space = {
        "x": (0, 20)  # This is the space of parameters to explore
    }

    analysis = distributed_bo(loss, space, "loss", name="bo_test", bo_steps=50)
    ray.shutdown()
    shutil.rmtree("bo_test")