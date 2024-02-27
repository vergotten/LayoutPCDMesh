#!/bin/bash

#yes | sudo
#wget https://developer.download.nvidia.com/compute/cuda/12.3.2/local_installers/cuda_12.3.2_545.23.08_linux.run

#sudo chmod -x cuda_12.3.2_545.23.08_linux.run
#sudo sh cuda_12.3.2_545.23.08_linux.run

## Set the variable
#CUDNN_DIR="/mnt/f/NN_tools/cudnn-linux-x86_64-8.9.7.29_cuda12-archive"

## Copy the cuDNN files
#sudo cp $CUDNN_DIR/include/cudnn.h /usr/local/cuda/include
#sudo cp $CUDNN_DIR/lib/libcudnn* /usr/local/cuda/lib

sudo apt-get install build-essential

#Download Anaconda
wget https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh

#Install Anaconda
yes | bash Anaconda3-2023.03-Linux-x86_64.sh -b -p $HOME/anaconda3

#Add Anaconda to PATH
echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Create a new conda environment with Python 3.8
yes | conda create -n myenv python=3.8

# Activate the new environment
conda activate myenv

# Install PyTorch with CUDA 11.3 support
conda install pytorch==1.10.1 torchvision==0.11.2 torchaudio==0.10.1 cudatoolkit=11.3 -c pytorch -c conda-forge

pip install -r "requirements.txt"

# Navigate to the directory containing PointNet2's setup.py
cd /pointnet2

# Install PointNet2
yes | python setup.py install
