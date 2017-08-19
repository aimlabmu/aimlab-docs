---
title: Setting up Python environment using Miniconda
keywords: python, miniconda
sidebar: aimlab_sidebar
permalink: Python_EnvirontmentSetup.html
folder: aimlabdocs
---

## Dependencies
- Miniconda 3 with Python 3.6
- Git 
- Visual Studio Code

## Instruction
- Download all dependencies and install them.
- For Miniconda 3, **DO NOT** forget to check `Add Anaconda to my PATH environment variable` and `Register Anaconda as my default Python 3.6` otherwise you won't be able to use `conda` command in command line.

### Miniconda 3
Since Miniconda is a small version of Anaconda, so it does not include any packages at installation. After installing Miniconda, we have to install packages by ourselves, some of the basic packages which is used regularly are listed as follows.

```sh
# update conda itself
conda update conda
# install basic packages
conda install numpy pandas matplotlib scipy scikit-image scikit-learn jupyter notebook
```

#### Proxy settings for Anaconda
According to [Anaconda official docs](https://conda.io/docs/config.html#configure-conda-for-use-behind-a-proxy-server-proxy-servers) we can set proxy for its package manager (`conda`). Add these lines to `~/.condarc` or `C:/Users/<username>/.condarc` to set proxy server for conda.

```sh
proxy_servers:
    # for salaya campus
    http: http://<mu proxy user>:<mu proxy pw>@proxy-sa.mahidol:8080
    # for siriraj campus
    http: http://<mu proxy user>:<mu proxy pw>@proxy-si.mahidol:8080
```

> *OpenCV installation using conda may be a bit tricky check [this](opencv/readme.md) out if you are stuck.*

### Git
Git is a powerful Version Control System (DVCS) which helps a lot in any progamming related jobs. To install Git on Windows we just have to download and run an installer from [official website](https://git-scm.com/). No special settings is needed for Git in installation but on first run (Git Bash), it is recommended to set user `name` and `email` as shown in example below. 

> *Note - email should be the same with those used to register on **Github** or **Bitbucket**, but username can be anything though it is better to keep it the same as that used on **Github** too.*

```sh
# set git name and email globally
# config file is located on ~/.gitconfig
# or C:/Users/username/.gitconfig on Windows
git config --global user.name <username>
git config --global user.email <email>
```

### Visual Studio Code
Visual Studio Code is an open source text editor developed by Microsoft (forked from Atom by Github). It is so fast, convenient and can be powerful by using the good choices of extensions. The only recommended extension related to Python development environment is:

- [Python](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python)

Other than this you can explore and try by yourself.

*PS. Since Mahidol University uses proxy in network connection, some steps may not be able to do in one go. Please try turn on and of Windows system proxy and retry those steps.*