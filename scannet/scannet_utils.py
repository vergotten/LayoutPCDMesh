"""
This script provides utility functions for reading and processing 3D mesh data from the ScanNet dataset.

Functions included in the script:

- `represents_int(s)`: Checks if a string represents an integer.
- `read_label_mapping(filename, label_from='raw_category', label_to='nyu40id')`: Reads a label mapping from a file. The mapping is a dictionary where each key-value pair maps a label from the `label_from` category to a label in the `nyu40id` category.
- `read_mesh_vertices(filename)`: Reads the XYZ coordinates of each vertex in a 3D mesh from a PLY file.
- `read_mesh_vertices_rgb(filename)`: Reads the XYZ coordinates and RGB color values of each vertex in a 3D mesh from a PLY file.
- `save_transformed_scene(scan_name)`: Loads a 3D scene from the ScanNet dataset, applies a transformation to the scene, and then saves the transformed scene back to the dataset. The transformation is specified by an axis alignment matrix that is loaded from a metadata file associated with the scene.

The paths to the ScanNet dataset and its various components (e.g., the raw scans, the transformed scans, the plane annotations, etc.) are loaded from a configuration file named 'scannet_config.yml'.

The name of the scene to be transformed is specified in the main function at the bottom of the script.
"""

''' Ref: https://github.com/ScanNet/ScanNet/blob/master/BenchmarkScripts '''
import os
import sys
import csv

try:
    import numpy as np
except:
    print("Failed to import numpy package.")
    sys.exit(-1)

try:
    from plyfile import PlyData, PlyElement
except:
    print("Please install the module 'plyfile' for PLY i/o, e.g.")
    print("pip install plyfile")
    sys.exit(-1)

def represents_int(s):
    ''' if string s represents an int. '''
    try: 
        int(s)
        return True
    except ValueError:
        return False


def read_label_mapping(filename, label_from='raw_category', label_to='nyu40id'):
    assert os.path.isfile(filename)
    mapping = dict()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            mapping[row[label_from]] = int(row[label_to])
    if represents_int(list(mapping.keys())[0]):
        mapping = {int(k):v for k,v in mapping.items()}
    return mapping

def read_mesh_vertices(filename):
    """ read XYZ for each vertex.
    """
    assert os.path.isfile(filename)
    with open(filename, 'rb') as f:
        plydata = PlyData.read(f)
        num_verts = plydata['vertex'].count
        vertices = np.zeros(shape=[num_verts, 3], dtype=np.float32)
        vertices[:,0] = plydata['vertex'].data['x']
        vertices[:,1] = plydata['vertex'].data['y']
        vertices[:,2] = plydata['vertex'].data['z']
    return vertices

def read_mesh_vertices_rgb(filename):
    """ read XYZ RGB for each vertex.
    Note: RGB values are in 0-255
    """
    assert os.path.isfile(filename)
    with open(filename, 'rb') as f:
        plydata = PlyData.read(f)
        num_verts = plydata['vertex'].count
        vertices = np.zeros(shape=[num_verts, 6], dtype=np.float32)
        vertices[:,0] = plydata['vertex'].data['x']
        vertices[:,1] = plydata['vertex'].data['y']
        vertices[:,2] = plydata['vertex'].data['z']
        vertices[:,3] = plydata['vertex'].data['red']
        vertices[:,4] = plydata['vertex'].data['green']
        vertices[:,5] = plydata['vertex'].data['blue']
    return vertices


