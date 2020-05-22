from ray import tune
from ray.tune.suggest.bayesopt import BayesOptSearch
from ray.tune.stopper import EarlyStopping
from ray.tune.schedulers import AsyncHyperBandScheduler
from ray.tune.analysis.experiment_analysis import ExperimentAnalysis
from typing import Callable, Dict


def distributed_bo(
    loss: Callable,
    space: Dict,
    metric: str,
    mode: str = "min",
    patience: int = 5,
    name: str = "gaussian_process",
    random_search_steps: int = 5,
    bo_steps: int = 500,
    resources_per_trial: Dict = None,
    config: Dict = None
):
    """Executes a distributed bayesian optimization on a Ray cluster.

    Usage examples
    --------------------

    
    Parameters
    --------------------
    loss: Callable,
        Loss function to be computed.
    space: Dict,
        The space of parameters to explore.
    metric: str,
        The metric passed by the loss function to consider.
    mode: str = "min",
        The optimization direction.
    patience: int = 10,
        Early stopping patience.
    name: str = "gaussian_process",
        Name of the distributed BO experiment.
    random_search_steps: int = 10,
        Number of the initial random search.
    bo_steps: int = 500,
        Number of the steps to run in the Bayesian Optimization.
    resources_per_trial: Dict = None,
        Resources to use for each node,
        by default: {"cpu": 1, "gpu": 0}
    config: Dict = None,
        Configuration to pass to the function.
    """

    if config is None:
        config = {}

    if resources_per_trial is None:
        resources_per_trial = {
            "cpu": 1,
            "gpu": 0
        }

    # Scheduler for the experiments
    hyperband = AsyncHyperBandScheduler(
        time_attr="training_iteration",
        metric=metric,
        mode=mode
    )

    # Following bayesian optimization
    gp = BayesOptSearch(
        space,
        metric=metric,
        mode=mode,
        random_search_steps=random_search_steps
    )

    # Execution of the BO.
    return tune.run(
        loss,
        name=name,
        stop=EarlyStopping(metric, mode=mode, patience=patience),
        local_dir=name,
        scheduler=hyperband,
        search_alg=gp,
        config=config,
        num_samples=bo_steps + random_search_steps,  # Number of iterations
        resources_per_trial=resources_per_trial,
        raise_on_failed_trial=False,
        verbose=0
    )
