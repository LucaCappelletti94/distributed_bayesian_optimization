import os
from tqdm.auto import tqdm
import subprocess


def test_slurm_distributed_bo():
    subprocess.run(["sbatch", "bayesian_test.sh"])
    for _ in tqdm(range(120)):
        if os.path.exists("BO.csv"):
            break
