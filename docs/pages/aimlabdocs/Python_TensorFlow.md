---
title: Installing TensorFlow with GPU support
keywords: 
sidebar: aimlab_sidebar
permalink: Python_TensorFlow.html
folder: aimlabdocs
---

## First Thing First
If you are not using Linux or have no plan to use GPU in computation, install the no-GPU version of TensorFlow following the guide [here](https://www.tensorflow.org/install/).

## Prerequisite Installation

There is also installation guide on official TensorFlow and Nvidia sites. However, they are complicated and not every time you can succeed it without any error. This docs will drive you through somehow easier steps and pretty sure would be success without error.

In this instruction we will use `CUDA` and `cuDNN` version `8` and `6.0` with `tensorflow_gpu` version `1.4.0` as seen in [TensorFlow guide](https://www.tensorflow.org/install/install_sources#tested_source_configurations).

### Nvidia graphic drivers

To install Nvidia graphic drivers, run the following commands. You can check the latest version of the driver at the [archive site](https://launchpad.net/~graphics-drivers/+archive/ubuntu/ppa). For now the latest version is `387`.

```sh
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update
sudo apt-get install nvidia-<version> nvidia-settings
```

### CUDA and cuDNN

#### CUDA

Go to [CUDA Toolkit Download site](https://developer.nvidia.com/cuda-downloads) and download runfile based on your setup. For example Ubuntu 16.04 with x64 system will have to select like image below.

![cuda-installation](pages/aimlabdocs/img/cuda_runfile.png)

Then run following command (*note that you need to say **NO** to **DRIVER INSTALLATION**, the others are yes*):

```sh
sudo sh cuda_9.0.176_384.81_linux.run
```

Finally, add CUDA and LD_LIBRARY_PATH to path (`.bashrc` or `.zshrc` depending on your setup):

```sh
# export cuda path
export PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

```

#### cuDNN

Go to [cuDNN official site](https://developer.nvidia.com/cudnn) and download `cuDNN v6.0 (April 27, 2017), for CUDA 8.0` (this requires registration, please do). Extract and install as follows:

```sh
// extract to ./cuda folder
tar -xvzf cudnn-8.0-linux-x64-v6.0.tgz

// copy include and lib64 dir to installed cuda path 
sudo cp cuda/include/cudnn.h /usr/local/cuda-8.0/include 
sudo cp cuda/lib64/libcudnn* /usr/local/cuda-8.0/lib64 
```

### Prerequisite testing

We may test CUDA sample by going into `deviceQuery` in CUDA path like so:

```sh
cd /usr/local/cuda-8.0/samples/1_Utilities/deviceQuery
make
./deviceQuery
```

If this print out your GPU specification table, then you are good to go.

## TensorFlow Installation

There are various ways to install TensorFlow but we recommend Anaconda as we have already used it and it is also easier to manage. First we need to create conda environment (please inspect your python version by either running `python` or `ipython`): 

```sh
conda create -n tensorflow python=3.6.1
```

To activate conda environment run the following command:

```sh
source activate tensorflow
```

Install TensorFlow using `pip` inside the conda environment:

```sh
(tensorflow)$ pip install --ignore-installed --upgrade <tfBinaryURL>
```

You can find *tfBinaryURL* from [this link](https://www.tensorflow.org/install/install_linux#the_url_of_the_tensorflow_python_package).

To exit the environment, just run:

```sh
source deactivate
```

There is some good trick to manage your environment variables which you can find [here](https://conda.io/docs/user-guide/tasks/manage-environments.html#saving-environment-variables).