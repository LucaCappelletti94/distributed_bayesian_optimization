distributed_bayesian_optimization
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy|
|code_climate_maintainability|

Using Ray to run distributed Bayesian optimization on SLURM clusters.

Usage examples
------------------------
First of all you need to setup the virtual environment:

.. code:: shell

    bash setup.sh

and then you can launch the job on slurm:

.. code:: shell

    sbatch bayesian_test.sh

If everything runs smoothly, you should get afterwards a file called BO.csv in the same directory.

Customize the file custom_loss.py accordingly to get the desired results.

Tests Coverage
----------------------------------------------
Since some software handling coverages sometimes
get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Using Ray to run distributed Bayesian optimization on SLURM clusters.

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/distributed_bayesian_optimization.png
   :target: https://travis-ci.org/LucaCappelletti94/distributed_bayesian_optimization
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_distributed_bayesian_optimization&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_distributed_bayesian_optimization
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_distributed_bayesian_optimization&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_distributed_bayesian_optimization
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_distributed_bayesian_optimization&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_distributed_bayesian_optimization
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/distributed_bayesian_optimization/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/distributed_bayesian_optimization?branch=master
    :alt: Coveralls Coverage

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/a37a87df721041e592686bfc99390760
    :target: https://www.codacy.com/manual/LucaCappelletti94/distributed_bayesian_optimization?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/distributed_bayesian_optimization&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/82d5c54c27833eb5d5ee/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/distributed_bayesian_optimization/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/82d5c54c27833eb5d5ee/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/distributed_bayesian_optimization/test_coverage
    :alt: Code Climate Coverage
