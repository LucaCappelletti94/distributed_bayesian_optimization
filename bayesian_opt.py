# trainer.py
from collections import Counter
import os
import sys
import time
import ray
from ray.tune.suggest.bayesopt import BayesOptSearch


redis_password = sys.argv[1]
ray.init(address=os.environ["ip_head"], redis_password=redis_password)

space = {
    'x': (0, 20)
}

def my_func(x):
    return {
        "mean_loss":x**2
    }

algo = BayesOptSearch(space, max_concurrent=2, metric="mean_loss", mode="min",  utility_kwargs={
    "kind": "ucb",
    "kappa": 2.5,
    "xi": 0.0
})

analysis = ray.tune.run(my_func, search_alg=algo)

analysis.get_best_config(metric="mean_loss")