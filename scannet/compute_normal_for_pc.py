"""
This script processes the ScanNet dataset to compute normals for point sets.

The `process` function goes through each scan in the ScanNet dataset, loads the corresponding point cloud,
computes the normals for each point in the point cloud using the MeshLab software, and then saves the computed normals back to the dataset.

The script uses the PyMeshLab library to load the point clouds and compute the normals. The normals are computed based on
the neighboring points within a certain radius around each point.

The paths to the ScanNet dataset and its various components (e.g., the raw scans, the transformed scans, the plane annotations, etc.)
are loaded from a configuration file named 'scannet_config.yml'.

The `process` function can be used to preprocess the ScanNet dataset before training machine learning models for tasks such
as 3D object recognition or semantic segmentation.
"""

import os
import yaml
from tqdm import tqdm
import numpy as np
import pymeshlab

# Load the configuration file
with open('scannet_config.yml', 'r') as file:
    config = yaml.safe_load(file)

def process():
    """Processes the ScanNet data to compute normals for point sets."""
    scene_files = os.listdir(config['scannet_train_detection_data_dir'])
    vert_files = sorted([x for x in scene_files if "vert.npy" in x])
    file_names = [x[:len("scene0000_00")] for x in vert_files]
    all_scan_names = list(set([os.path.basename(x)[0:12] \
                               for x in os.listdir(config['scannet_planes_dir']) if x.startswith('scene')]))
    split_filenames = config['meta_data_dir'] + '/scannetv2_val.txt'
    with open(split_filenames, 'r') as f:
        scan_names = f.read().splitlines()

    # remove unavailable scans
    scan_names = sorted([sname for sname in scan_names if sname in file_names and sname in all_scan_names])

    os.makedirs(config['scannet_train_detection_data_normals_dir'], exist_ok=True)

    for file_idx, filename in tqdm(enumerate(scan_names), total=len(scan_names)):
        tqdm.write("Start processing " + filename)

        vert_data = np.load(f"{config['scannet_train_detection_data_dir']}/{filename}_vert.npy")
        sem_label_data = np.load(f"{config['scannet_train_detection_data_dir']}/{filename}_sem_label.npy")

        ms = pymeshlab.MeshSet()

        with open("buffer.TXT", 'w+') as f:
            layout_pt_cnt = vert_data.shape[0]
            pc_center = np.mean(vert_data, axis=0)[:3]
            pc_center[2] = (np.max(vert_data, axis=0)[2] + pc_center[2]) / 2
            f.write("\n".join(
                [f"{x[0]} {x[1]} {x[2]}" for x in vert_data]
            ))
        ms.load_new_mesh("buffer.TXT", separator=2)
        ms.apply_filter('compute_normals_for_point_sets', k=100, smoothiter=5, flipflag=True, viewpos=pc_center)

        normal_vectors = ms.current_mesh().vertex_normal_matrix()

        reverse_mask = ((vert_data[:, :3] - pc_center[:3]).reshape(layout_pt_cnt, 1, 3) \
                        @ normal_vectors.reshape(layout_pt_cnt, 3, 1)).reshape(layout_pt_cnt) < 0

        normal_vectors[reverse_mask] = -normal_vectors[reverse_mask]  # Point towards inner
        np.save(f"{config['scannet_train_detection_data_normals_dir']}/{filename}.normal.npy", normal_vectors)


if __name__ == "__main__":
    """Main entry point of the script."""
    process()
