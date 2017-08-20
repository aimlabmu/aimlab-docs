---
title: Setting up OpenCV for Python using conda
keywords: 
sidebar: aimlab_sidebar
permalink: Python_OpenCV.html
folder: aimlabdocs
---

Anaconda provides a good python powered environment for scientific research. One of the most used library in image processing, [OpenCV](http://opencv.org/), is also supported by [Anaconda community](https://anaconda.org/menpo/opencv3). To install OpenCV using conda, run the following command.

```sh
conda install -c menpo opencv3
``` 

This command will fetch for OpenCV `v3.2.0`. However, that version avaliable on repo is only for Linux. And another problem is that OpenCV `v3.1.0` seems to lock with Python `3.5` so we need to downgrade Python in order to install OpenCV. To downgrade Python to version `3.5` and install OpenCV `v.3.1.0`, run commands as follows:

```sh
# downgrade python 3.5
conda install python=3.5
# install opencv 3.1.0
conda install -c menpo opencv3=3.1.0
```