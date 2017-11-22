# Installing TensorFlow with GPU support

## First thing first
If you are not using Linux or have no plan to use GPU in computation, install the no-GPU version of TensorFlow following the guide [here](https://www.tensorflow.org/install/).

## Prerequisite Installations

There is also installation guide on official TensorFlow and Nvidia sites. However, they are complicated and not every time you can succeed it without any error. This docs will drive you through somehow easier steps and pretty sure would be success without error.

In this instruction we will use `cuDNN` and `CUDA` version `6` and `8` with `tensorflow_gpu` version `1.4.0` as seen in [TensorFlow guide](https://www.tensorflow.org/install/install_sources#tested_source_configurations).

### Nvidia graphic drivers

To install Nvidia graphic drivers, run the following commands. You can check the latest version of the driver at the [archive site](https://launchpad.net/~graphics-drivers/+archive/ubuntu/ppa). For now the latest version is `387`.

```sh
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update
sudo apt-get install nvidia-<version> nvidia-settings
```

### CUDA

Go to [cuDNN official site](https://developer.nvidia.com/cudnn) and download `cuDNN v6.0 (April 27, 2017), for CUDA 8.0` (this requires registration, please do). Unzip and install as follows:

```sh
tar -xvzf cudnn-8.0-linux-x64-v6.0.tgz
```



1. add nvidia ppa repo
2. update and install nvidia-387, nvidia-settings
3. download cuda run file
4. install run file, say no to driver installation, anything else is yes
5. add cuda path 
6. install cuDNN (6.0 for tensorflow) in the cuda path
7. test with cuda sample `1_utility/deviceQuery` by `cd deviceQuery; make`

```
sudo cp cuda/include/cudnn.h /usr/local/cuda-8.0/include 
sudo cp cuda/lib64/libcudnn* /usr/local/cuda-8.0/lib64 
```