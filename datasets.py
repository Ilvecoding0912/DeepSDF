import glob
import logging
import numpy as np
import os
import random
import torch
import torch.utils.data
import trimesh
from torch.utils.data import Dataset

class SDFDataset(Dataset):
    def __init__(self, pts, sdf):
        super().__init__()
        self.data = pts
        self.targets = sdf

    def __getitem__(self, index):
        return self.data[index], self.targets[index]

    def __len__(self):
        return self.data.shape[0]

class SampleFromMesh():
    def __init__(self, mesh, num_pts=500000):
        self.mesh = mesh
        self.sample_points = self.sampling(num_pts)
        self.get_sdf()

    def sampling(self, num_pts=500000):
        sample_points, face_indices = trimesh.sample.sample_surface(self.mesh, count=num_pts)
        return sample_points
    
    def get_sdf(self, noise_scale=0.0025):
        noise = np.random.normal(loc=0, scale=noise_scale, size=self.sample_points.shape)
        self.noisy_points = self.sample_points + noise
        self.sdf = self.mesh.nearest.signed_distance(self.noisy_points)

class SDFSamples(Dataset):
    def __init__(self) -> None:
        super().__init__()
