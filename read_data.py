import json
import os, sys
import warnings
from os import path
from pathlib import Path
from typing import Dict
from tqdm import tqdm
import trimesh
import numpy as np
import glob
import shutil
from datasets import SampleFromMesh

DATA_DIR = os.path.join(os.getcwd(), 'data', 'ShapeNetCore.v2')
SAVE_DIR = os.path.join(os.getcwd(), 'data', 'data')
points_dir, noisy_points_dir = os.path.join(SAVE_DIR, 'points'), os.path.join(SAVE_DIR, 'noisy_points')
sdf_dir = os.path.join(SAVE_DIR, 'sdf')
mesh_dir = os.path.join(SAVE_DIR, 'mesh')

# make directories for processed data
os.makedirs(points_dir, exist_ok=True)
os.makedirs(noisy_points_dir, exist_ok=True)
os.makedirs(sdf_dir, exist_ok=True)
os.makedirs(mesh_dir, exist_ok=True)
idx = 0

for category in os.listdir(DATA_DIR)[:3]:
    # save dir path of each category
    category_dir = os.path.join(DATA_DIR, category)

    for source_dir in tqdm(glob.glob(category_dir+'/*')):
        # read all .obj file
        mesh_file_name = list(glob.iglob(source_dir + "/**/*.obj"))+ list(glob.iglob(source_dir + "/*.obj"))
                                                                          
        mesh = trimesh.load(mesh_file_name[0], force='mesh')
        sample_mesh = SampleFromMesh(mesh)

        # save data
        np.save(os.path.join(points_dir, str(idx)+'.npy'), sample_mesh.sample_points)
        np.save(os.path.join(noisy_points_dir, str(idx)+'.npy'), sample_mesh.noisy_points)
        np.save(os.path.join(sdf_dir, str(idx)+'.npy'), sample_mesh.sdf)
        shutil.copy(mesh_file_name[0], os.path.join(mesh_dir, str(idx)+'.npy'))
        idx += 1

