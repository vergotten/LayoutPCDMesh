# ScanNet Dataset

The **ScanNet dataset** is a large-scale collection of 3D indoor scenes captured using depth sensors. It serves as a valuable resource for various computer vision and robotics tasks. Here's an overview of the directories within the dataset:

1. **`meta_data`**:
   - Contains metadata files associated with the ScanNet scenes.
   - Metadata includes camera intrinsics, extrinsics, scene IDs, and other relevant information.
   - Useful for understanding the context and camera setup of each scene.

2. **`scannet_planes`**:
   - Stores plane segmentation results for each scene.
   - Planes are essential for understanding room layouts and surfaces.
   - Each plane is represented by its equation (normal vector and distance from origin).

3. **`scannet_train_detection_data`**:
   - Contains labeled object detection data.
   - Annotations include bounding boxes, class labels, and confidence scores.
   - Useful for training and evaluating object detection models.

4. **`scannet_train_detection_data_normals`**:
   - Similar to `scannet_train_detection_data`, but also includes surface normals.
   - Normals provide additional geometric information about object surfaces.
   - Useful for tasks like instance segmentation and semantic segmentation.

5. **`scans`**:
   - The heart of the dataset—contains the raw point cloud data for each scene.
   - Point clouds represent the 3D geometry of the indoor environment.
   - Each point is defined by its 3D coordinates (x, y, z).

6. **`scans_transform`**:
   - Contains transformed versions of the original point clouds.
   - Transformations may include alignment, scaling, or other preprocessing steps.
   - Useful for tasks that require consistent coordinate systems.

## Data Handling

To manage dataset paths and configuration settings, use the `scannet_config.yml` file. It centralizes important information and simplifies data access throughout your project.

Certainly! Let's update the README file to include information about how to use the YAML configuration file (`scannet_config.yml`). Here's an additional section you can add to your README:

---

## Using the YAML Configuration File

The `scannet_config.yml` file serves as a central place to manage important paths and settings related to the **ScanNet dataset**. Here's how you can utilize it effectively:

1. **Understanding the Structure**:
   - Open `scannet_config.yml` in a text editor.
   - Each variable corresponds to a specific directory or configuration option.
   - Comments within the file provide context for each variable.

2. **Customize Paths**:
   - Adjust the paths according to your local setup.
   - For example, if you move the dataset to a different location, update the `data_root` variable.

3. **Access Paths in Your Code**:
   - In your Python scripts or notebooks, load the configuration from the YAML file:
     ```python
     import yaml

     # Load the configuration
     with open('scannet_config.yml', 'r') as config_file:
         config = yaml.safe_load(config_file)

     # Access specific paths
     data_root = config['data_root']
     meta_data_dir = config['meta_data_dir']
     # and so on...
     ```
     
## Usage

- Researchers and practitioners can use the ScanNet dataset for:
  - Scene understanding
  - Object detection
  - Semantic segmentation
  - Layout estimation
  - 3D reconstruction
  
## Citation

If you use the ScanNet dataset in your work, please cite the original paper:

```
@inproceedings{dai2017scannet,
  title={ScanNet: Richly-annotated 3D Reconstructions of Indoor Scenes},
  author={Dai, Angela and Chang, Angel X. and Savva, Manolis and Halber, Maciej and Funkhouser, Thomas and Nie{\ss}ner, Matthias},
  booktitle={Proceedings of CVPR},
  year={2017}
}
```