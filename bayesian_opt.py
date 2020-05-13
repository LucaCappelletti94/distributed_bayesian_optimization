# trainer.py
from collections import Counter
import os
import sys
import time
import ray
from ray.tune.suggest.bayesopt import BayesOptSearch
from ray.tune.schedulers import ASHAScheduler


redis_password = sys.argv[1]
ray.init(address=os.environ["ip_head"], redis_password=redis_password)

space = {
    'x': (0, 20)
}

def my_func(config, reporter):
    reporter(mean_loss=config["x"]**2)

algo = BayesOptSearch(space, metric="mean_loss", mode="min",  utility_kwargs={
    "kind": "ucb",
    "kappa": 2.5,
    "xi": 0.0
})

analysis = ray.tune.run(
    my_func, search_alg=algo, num_samples=100, scheduler=ASHAScheduler(metric="mean_accuracy", mode="max", grace_period=1),)

print(analysis.get_best_config(metric="mean_loss"))