from ray.tune.suggest import Searcher
import pickle
import logging
import copy
from ray.tune.analysis.experiment_analysis import ExperimentAnalysis
import ray
import sys
import os
from ray import tune
from ray.tune.schedulers import AsyncHyperBandScheduler
from ray.tune.suggest import ConcurrencyLimiter


# NOTE: The following class has
# been now merged into Ray from my pull request
# but it is not yet part of the pubblished version.
from ray.tune import Stopper
import numpy as np


class EarlyStopping(Stopper):
    def __init__(self, metric, std=0.001, top=10, mode="min", patience=0):
        """Create the EarlyStopping object.
        Stops the entire experiment when the metric has plateaued
        for more than the given amount of iterations specified in
        the patience parameter.
        Args:
            metric (str): The metric to be monitored.
            std (float): The minimal standard deviation after which
                the tuning process has to stop.
            top (int): The number of best model to consider.
            mode (str): The mode to select the top results.
                Can either be "min" or "max".
            patience (int): Number of epochs to wait for
                a change in the top models.
        Raises:
            ValueError: If the mode parameter is not "min" nor "max".
            ValueError: If the top parameter is not an integer
                greater than 1.
            ValueError: If the standard deviation parameter is not
                a strictly positive float.
            ValueError: If the patience parameter is not
                a strictly positive integer.
        """
        if mode not in ("min", "max"):
            raise ValueError("The mode parameter can only be"
                             " either min or max.")
        if not isinstance(top, int) or top <= 1:
            raise ValueError("Top results to consider must be"
                             " a positive integer greater than one.")
        if not isinstance(patience, int) or patience < 0:
            raise ValueError("Patience must be"
                             " a strictly positive integer.")
        if not isinstance(std, float) or std <= 0:
            raise ValueError("The standard deviation must be"
                             " a strictly positive float number.")
        self._mode = mode
        self._metric = metric
        self._patience = patience
        self._iterations = 0
        self._std = std
        self._top = top
        self._top_values = []

    def __call__(self, trial_id, result):
        """Return a boolean representing if the tuning has to stop."""
        self._top_values.append(result[self._metric])
        if self._mode == "min":
            self._top_values = sorted(self._top_values)[:self._top]
        else:
            self._top_values = sorted(self._top_values)[-self._top:]

        # If the current iteration has to stop
        if self.has_plateaued():
            # we increment the total counter of iterations
            self._iterations += 1
        else:
            # otherwise we reset the counter
            self._iterations = 0

        # and then call the method that re-executes
        # the checks, including the iterations.
        return self.stop_all()

    def has_plateaued(self):
        return (len(self._top_values) == self._top
                and np.std(self._top_values) <= self._std)

    def stop_all(self):
        """Return whether to stop and prevent trials from starting."""
        return self.has_plateaued() and self._iterations >= self._patience


# NOTE: as for the class above,
# also the following one adding support for previous
# analysis and default kwargs is still to be added to the published version

try:  # Python 3 only -- needed for lint test.
    import bayes_opt as byo
except ImportError:
    byo = None


logger = logging.getLogger(__name__)


class BayesOptSearch(Searcher):
    """Uses fmfn/BayesianOptimization to optimize hyperparameters.

    fmfn/BayesianOptimization is a library for Bayesian Optimization. More
    info can be found here: https://github.com/fmfn/BayesianOptimization.

    You will need to install fmfn/BayesianOptimization via the following:

    .. code-block:: bash

        pip install bayesian-optimization

    This algorithm requires setting a search space using the
    `BayesianOptimization search space specification`_.

    Parameters:
        space (dict): Continuous search space. Parameters will be sampled from
            this space which will be used to run trials.
        metric (str): The training result objective value attribute.
        mode (str): One of {min, max}. Determines whether objective is
            minimizing or maximizing the metric attribute.
        utility_kwargs (dict): Parameters to define the utility function.
            The default value is a dictionary with three keys:
            - kind: ucb (Upper Confidence Bound)
            - kappa: 2.576
            - xi: 0.0
        random_state (int): Used to initialize BayesOpt.
        analysis (ExperimentAnalysis): Optionally, the previous analysis
            to integrate.
        verbose (int): Sets verbosity level for BayesOpt packages.
        max_concurrent: Deprecated.
        use_early_stopped_trials: Deprecated.

    .. code-block:: python

        from ray import tune
        from ray.tune.suggest.bayesopt import BayesOptSearch

        space = {
            'width': (0, 20),
            'height': (-100, 100),
        }
        algo = BayesOptSearch(space, metric="mean_loss", mode="min")
        tune.run(my_func, algo=algo)
    """
    # bayes_opt.BayesianOptimization: Optimization object
    optimizer = None

    def __init__(self,
                 space,
                 metric="episode_reward_mean",
                 mode="max",
                 utility_kwargs=None,
                 random_state=1,
                 verbose=0,
                 analysis=None,
                 max_concurrent=None,
                 use_early_stopped_trials=None):
        """Instantiate new BayesOptSearch object.

        Parameters:
            space (dict): Continuous search space.
                Parameters will be sampled from
                this space which will be used to run trials.
            metric (str): The training result objective value attribute.
            mode (str): One of {min, max}. Determines whether objective is
                minimizing or maximizing the metric attribute.
            utility_kwargs (dict): Parameters to define the utility function.
                Must provide values for the keys `kind`, `kappa`, and `xi`.
            random_state (int): Used to initialize BayesOpt.
            analysis (ExperimentAnalysis): Optionally, the previous analysis
                to integrate.
            verbose (int): Sets verbosity level for BayesOpt packages.
            max_concurrent: Deprecated.
            use_early_stopped_trials: Deprecated.
        """
        assert byo is not None, (
            "BayesOpt must be installed!. You can install BayesOpt with"
            " the command: `pip install bayesian-optimization`.")
        assert mode in ["min", "max"], "`mode` must be 'min' or 'max'!"
        self.max_concurrent = max_concurrent
        super(BayesOptSearch, self).__init__(
            metric=metric,
            mode=mode,
            max_concurrent=max_concurrent,
            use_early_stopped_trials=use_early_stopped_trials)

        if utility_kwargs is None:
            # The defaults arguments are the same
            # as in the package BayesianOptimization
            utility_kwargs = dict(
                kind="ucb",
                kappa=2.576,
                xi=0.0,
            )

        if mode == "max":
            self._metric_op = 1.
        elif mode == "min":
            self._metric_op = -1.
        self._live_trial_mapping = {}

        self.optimizer = byo.BayesianOptimization(
            f=None, pbounds=space, verbose=verbose, random_state=random_state)

        self.utility = byo.UtilityFunction(**utility_kwargs)
        if analysis is not None:
            self.register_analysis(analysis)

    def suggest(self, trial_id):
        if self.max_concurrent:
            if len(self._live_trial_mapping) >= self.max_concurrent:
                return None
        new_trial = self.optimizer.suggest(self.utility)

        self._live_trial_mapping[trial_id] = new_trial

        return copy.deepcopy(new_trial)

    def register_analysis(self, analysis):
        """Integrate the given analysis into the gaussian process.

        Parameters
        ------------------
        analysis (ExperimentAnalysis): Optionally, the previous analysis
            to integrate.
        """
        for (_, report), params in zip(analysis.dataframe().iterrows(),
                                       analysis.get_all_configs().values()):
            # We add the obtained results to the
            # gaussian process optimizer
            self.optimizer.register(
                params=params, target=self._metric_op * report[self._metric])

    def on_trial_complete(self, trial_id, result=None, error=False):
        """Notification for the completion of trial."""
        if result:
            self._process_result(trial_id, result)
        del self._live_trial_mapping[trial_id]

    def _process_result(self, trial_id, result):
        self.optimizer.register(
            params=self._live_trial_mapping[trial_id],
            target=self._metric_op * result[self.metric])

    def save(self, checkpoint_dir):
        trials_object = self.optimizer
        with open(checkpoint_dir, "wb") as output:
            pickle.dump(trials_object, output)

    def restore(self, checkpoint_dir):
        with open(checkpoint_dir, "rb") as input:
            trials_object = pickle.load(input)
        self.optimizer = trials_object


# HERE starts the actual script


redis_password = sys.argv[1]
num_cpus = int(sys.argv[2])
ray.init(
    address=os.environ["ip_head"],
    redis_password=redis_password,
    configure_logging=True,
    logging_level=logging.CRITICAL
)

config = {}  # This is a fixed configuration to pass to the functions
space = {
    "x": (0, 10)  # This is the space of parameters to explore
}


def loss(config, reporter):
    reporter(loss=config["x"]**2)  # A simple function to optimize


random_search_analysis = tune.run(
    loss,
    name="gaussian_process_ray",
    stop=EarlyStopping("loss"),
    local_dir="ray_results_gp",
    config={
        # I currently have found no better option for the initial random search.
        "x": tune.uniform(0, 20)
    },
    num_samples=10,  # Number of iterations
    resources_per_trial={"cpu":1, "gpu":0},
    raise_on_failed_trial=False,
    verbose=0
)

random_search_analysis.dataframe().to_csv("random_search.csv")

gp = BayesOptSearch(
    space,
    metric="loss",
    mode="min",
    analysis=random_search_analysis
)

algo = ConcurrencyLimiter(gp, max_concurrent=1) # This limits the number of parallel executions, if so desidered.

# TODO: add a scheduler,
# by using AsyncHyperBandScheduler.
# I'm talking with one of the developers to better understand how this works.

analysis = tune.run(
    loss,
    name="gaussian_process_ray",
    stop=EarlyStopping("loss"),
    local_dir="ray_results_gp",
    search_alg=algo,
    config=config,
    num_samples=100, # Number of iterations
    resources_per_trial={"cpu":1, "gpu":0},
    raise_on_failed_trial=False,
    verbose=0
)

analysis.dataframe().to_csv("bayesian_process.csv")
# Then we can close down ray
ray.shutdown()