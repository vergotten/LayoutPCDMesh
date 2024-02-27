"""
This script is designed to export 3D scan data from the ScanNet dataset.

The `ScannetDetectionDataset` class in the script loads 3D point cloud data and associated bounding box labels from the dataset.
The bounding boxes are axis-aligned and parameterized by their center point (cx, cy, cz) and dimensions (dx, dy, dz).

The `__getitem__` method of the `ScannetDetectionDataset` class returns a dictionary containing the point cloud data and
various labels for each bounding box, including the center point, semantic class, heading angle, and size.

The script also includes utility functions for rotating the bounding boxes and point clouds, and for splitting the dataset into training and validation sets.

The paths to the ScanNet dataset and its various components (e.g., the raw scans, the transformed scans, the plane annotations, etc.)
are loaded from a configuration file named 'scannet_config.yml'.

The `ScannetDetectionDataset` class can be used to create PyTorch data loaders for training and evaluating
models for 3D object detection tasks on the ScanNet dataset.
"""

import os
import datetime
import numpy as np
import yaml

from load_scannet_data import export


# Load the configuration file
with open('scannet_config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Set the directories from the configuration file
SCANNET_DIR = config['scans_dir']
TRAIN_SCAN_NAMES = [line.rstrip() for line in open(config['meta_data_dir'] + '/scannet_train.txt')]
LABEL_MAP_FILE = config['meta_data_dir'] + '/scannetv2-labels.combined.tsv'
DONOTCARE_CLASS_IDS = np.array([])
OBJ_CLASS_IDS = np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 24, 28, 33, 34, 36, 39])
MAX_NUM_POINT = 50000
OUTPUT_FOLDER = config['scannet_train_detection_data_dir']


def export_one_scan(scan_name, output_filename_prefix):
    """Exports one scan given its name and an output filename prefix.

    Args:
        scan_name (str): The name of the scan to export.
        output_filename_prefix (str): The prefix for the output filename.
    """
    mesh_file = os.path.join(SCANNET_DIR, scan_name, scan_name + '_vh_clean_2.ply')
    agg_file = os.path.join(SCANNET_DIR, scan_name, scan_name + '.aggregation.json')
    seg_file = os.path.join(SCANNET_DIR, scan_name, scan_name + '_vh_clean_2.0.010000.segs.json')
    meta_file = os.path.join(SCANNET_DIR, scan_name,
                             scan_name + '.txt')  # includes axisAlignment info for the train set scans.
    mesh_vertices, semantic_labels, instance_labels, instance_bboxes, instance2semantic = \
        export(mesh_file, agg_file, seg_file, meta_file, LABEL_MAP_FILE, None)

    mask = np.logical_not(np.in1d(semantic_labels, DONOTCARE_CLASS_IDS))
    mesh_vertices = mesh_vertices[mask, :]
    semantic_labels = semantic_labels[mask]
    instance_labels = instance_labels[mask]

    num_instances = len(np.unique(instance_labels))
    print('Num of instances: ', num_instances)

    bbox_mask = np.in1d(instance_bboxes[:, -1], OBJ_CLASS_IDS)
    instance_bboxes = instance_bboxes[bbox_mask, :]
    print('Num of care instances: ', instance_bboxes.shape[0])

    N = mesh_vertices.shape[0]
    if N > MAX_NUM_POINT:
        choices = np.random.choice(N, MAX_NUM_POINT, replace=False)
        mesh_vertices = mesh_vertices[choices, :]
        semantic_labels = semantic_labels[choices]
        instance_labels = instance_labels[choices]

    np.save(output_filename_prefix + '_vert.npy', mesh_vertices)
    np.save(output_filename_prefix + '_sem_label.npy', semantic_labels)
    np.save(output_filename_prefix + '_ins_label.npy', instance_labels)
    np.save(output_filename_prefix + '_bbox.npy', instance_bboxes)


def batch_export():
    """Exports all scans listed in TRAIN_SCAN_NAMES."""
    if not os.path.exists(OUTPUT_FOLDER):
        print('Creating new data folder: {}'.format(OUTPUT_FOLDER))
        os.mkdir(OUTPUT_FOLDER)

    for scan_name in TRAIN_SCAN_NAMES:
        print('-' * 20 + 'begin')
        print(datetime.datetime.now())
        print(scan_name)
        output_filename_prefix = os.path.join(OUTPUT_FOLDER, scan_name)
        if os.path.isfile(output_filename_prefix + '_vert.npy'):
            print('File already exists. skipping.')
            print('-' * 20 + 'done')
            continue
        try:
            export_one_scan(scan_name, output_filename_prefix)
        except:
            print('Failed export scan: %s' % (scan_name))
        print('-' * 20 + 'done')


if __name__ == '__main__':
    """Main entry point of the script."""
    batch_export()
