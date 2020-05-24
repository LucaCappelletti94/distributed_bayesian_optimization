#!/bin/bash
python -m pip install click
# Installing latest Ray from master
python -m pip install -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-0.9.0.dev0-cp36-cp36m-manylinux1_x86_64.whl
# Installing additional requirements
python -m pip install -r requirements.txt