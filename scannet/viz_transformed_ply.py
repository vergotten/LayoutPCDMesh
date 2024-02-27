"""
This script loads a 3D scene from the ScanNet dataset, applies a transformation to the scene,
and then saves the transformed scene back to the dataset. The transformation is specified by
an axis alignment matrix that is loaded from a metadata file associated with the scene.

The script uses Open3D for reading and writing triangle meshes, and for applying the transformation.

The paths to the ScanNet dataset and its various components (e.g., the raw scans, the transformed scans,
the plane annotations, etc.) are loaded from a configuration file named 'scannet_config.yml'.

The name of the scene to be transformed is specified in the main function at the bottom of the script.
"""

import os
import sys
import numpy as np
import open3d as o3d
import yaml

# Load the configuration file
with open('scannet_config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Application paths
APP_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_ROOT_DIR = os.path.dirname(APP_BASE_DIR)
sys.path.append(APP_ROOT_DIR)
sys.path.append(os.path.join(APP_ROOT_DIR, 'utils'))
sys.path.append(os.path.join(APP_ROOT_DIR, 'models'))

# Dataset paths
DATA_ROOT = config['data_root']
META_DATA_DIR = config['meta_data_dir']
SCANNET_PLANES_DIR = config['scannet_planes_dir']
SCANS_DIR = config['scans_dir']
SCANS_TRANSFORM_DIR = config['scans_transform_dir']
SCANNET_TRAIN_DETECTION_DATA_DIR = config['scannet_train_detection_data_dir']
SCANNET_TRAIN_DETECTION_DATA_NORMALS_DIR = config['scannet_train_detection_data_normals_dir']

def save_transformed_scene(scan_name):
    """Save the transformed scene of a scan.

    Args:
        scan_name (str): The name of the scan.
    """
    # Load scene axis alignment matrix
    meta_file = os.path.join(SCANS_DIR, scan_name, scan_name + '.txt')
    lines = open(meta_file).readlines()
    for line in lines:
        if 'axisAlignment' in line:
            axis_align_matrix = [float(x) \
                                 for x in line.rstrip().strip('axisAlignment = ').split(' ')]
            break
    axis_align_matrix = np.array(axis_align_matrix).reshape((4, 4))

    # Rotate scene
    mesh_file = os.path.join(SCANS_DIR, scan_name, scan_name + '_vh_clean_2.ply')
    mesh = o3d.io.read_triangle_mesh(mesh_file)
    mesh3 = mesh.transform(axis_align_matrix)

    save_mesh_file = os.path.join(SCANS_DIR, scan_name, scan_name + '_transformed.ply')
    o3d.io.write_triangle_mesh(save_mesh_file, mesh3)


if __name__ == "__main__":
    scan_name = "scene0626_02"
    save_transformed_scene(scan_name=scan_name)
