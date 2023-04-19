#!/usr/bin/env bash

mkdir -p data
cd data/

# Downloading data
wget http://shapenet.cs.stanford.edu/shapenet/obj-zip/ShapeNetCore.v2.zip

# unzip data
!unzip ShapeNetCore.v2.zip 

# run
python read_data.py