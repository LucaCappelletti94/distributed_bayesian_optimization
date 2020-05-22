#!/bin/bash
# Cloning ray, getting my own version up until
# they accept the latest pull request.
git clone https://github.com/LucaCappelletti94/ray
# Getting into the subdirectory
cd ray
# Switching to the pull request branch
git checkout random_search_bo
# Making sure that this is the last version
git pull
# Installing virtual env
python -m pip install virtualenv
# Setupping the virtualend
python -m venv ray_venv
# Install Ray
python python/ray/setup-dev.py --yes
# Navigating back out
cd ..
# Installing additional requirements
pip install .
# Deactivate environment
deactivate