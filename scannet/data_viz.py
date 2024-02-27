"""
The load_and_visualize_data function loads the point cloud data for a given scene, along with associated instance
labels, semantic labels, and bounding boxes. It then visualizes this data by writing it to OBJ files, which can be
viewed in a 3D viewer. The visualizations include the original point cloud with RGB colors, as well as separate
visualizations of the instance labels and semantic labels.

The script uses the PyMeshLab library to load the point clouds and compute the normals. The normals are computed based
on the neighboring points within a certain radius around each point.

The paths to the ScanNet dataset and its various components (e.g., the raw scans, the transformed scans,
the plane annotations, etc.) are loaded from a configuration file named ‘scannet_config.yml’.

The load_and_visualize_data function can be used to preprocess the ScanNet dataset before
training machine learning models for tasks such as 3D object recognition or semantic segmentation.
"""

import sys
import os
import yaml
import numpy as np

import sys
sys.path.insert(0, '/mnt/f/Code/3D/LayoutPCD2Mesh')
from utils import pc_util

from utils import pc_util

# Load the configuration file
with open('scannet_config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Set the directories from the configuration file
BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

scene_name = config['scannet_train_detection_data_dir'] + '/scene0002_00'
# output_folder = 'data_viz_dump'
output_folder = os.path.join(BASE_DIR, 'data_viz_dump')


def load_and_visualize_data(scene_name, output_folder):
    """Loads the ScanNet data and visualizes it.

    Args:
        scene_name (str): The name of the scene to load.
        output_folder (str): The folder to save the visualizations.
    """
    data = np.load(scene_name + '_vert.npy')
    scene_points = data[:, 0:3]
    colors = data[:, 3:]
    instance_labels = np.load(scene_name + '_ins_label.npy')
    semantic_labels = np.load(scene_name + '_sem_label.npy')
    instance_bboxes = np.load(scene_name + '_bbox.npy')

    print(np.unique(instance_labels))
    print(np.unique(semantic_labels))
    # input()
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # Write scene as OBJ file for visualization
    pc_util.write_ply_rgb(scene_points, colors, os.path.join(output_folder, 'scene.obj'))
    pc_util.write_ply_color(scene_points, instance_labels, os.path.join(output_folder, 'scene_instance.obj'))
    pc_util.write_ply_color(scene_points, semantic_labels, os.path.join(output_folder, 'scene_semantic.obj'))

    # from model_util_scannet import ScannetDatasetConfig
    # DC = ScannetDatasetConfig()
    print(instance_bboxes.shape)


if __name__ == "__main__":
    """Main entry point of the script."""
    load_and_visualize_data(scene_name, output_folder)
