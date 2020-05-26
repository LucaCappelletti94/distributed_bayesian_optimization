import os
from tqdm.auto import tqdm
import subprocess
import time


def test_slurm_distributed_bo():
    subprocess.run(["sbatch", "bayesian_test.sh"], shell=True)
    for _ in tqdm(range(180)):
        time.sleep(1)
        if os.path.exists("BO.csv"):
            break
    assert os.path.exists("BO.csv")