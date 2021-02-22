---
title: "Installation"
permalink: /install/
author_profile: false
entries_layout: grid
show_downloads: true
sidebar:
  nav: "sidebar-installation"
---

Installation of ML-LPA is rather straightforward. A **detailed guide** is given below.

## Requirements

ML-LPA requires a **Python 3** version to be installed on the computer, as well as the following libraries to work:

* NumPy
* h5py
* MDAnalysis
* pandas
* scikit-learn (version >= 0.22.0)
* tess
* tqdm

During the installation, ML-LPA should automatically install all missing libraries from the list.

## From PyPi

ML-LPA can be installed by simply using the *pip* command. Just open a terminal and type the following line

```sh
> pip install mllpa
```

The page for ML-LPA on PyPi can be visited using [pypi.org/project/mllpa/](this link).

## From the GitHub repo

ML-LPA can be installed directly from the **source files** available on our GitHub repo. The detailed
process to install from these files is described below.

### Get the files

You will need first to get the source files from our **GitHub repo**. Use any of the following link to access the file.

<a href="https://github.com/vivien-walter/mllpa" class="btn btn--info"><b>See on GitHub</b></a> <a href="https://github.com/vivien-walter/mllpa/archive/master.zip" class="btn btn--primary"><i class='fas fa-download'></i> <b>DOWNLOAD</b></a>

### Install the package

**Important:** We recommend to setup a **virtualenv** first, to avoid any version conflict with pre-existing packages.
Instruction on how to install a virtualenv can be found [in this link](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
{: .notice--info}

1. Open the MLLPA folder in the Terminal and go to the *source* folder.

    ```sh
    > cd mllpa-master/
    > cd source/
    ```

2. Install the library using the *setup.py* file.

    The setup.py file has been designed to install automatically all the libraries and packages required that cannot be found
    in the environment.

    **Warning:** Because of a problem with the MDAnalysis library, MDAnalysis should be installed manually first.
    This can be done by using the command ```> pip3 install MDAnalysis```
    {: .notice--warning}

    When you are ready to install, just run the following command in the Terminal.

    ```sh
    > python3 setup.py install
    ```

## Check the installation

To verify that the installation went well, you can simply open a Python shell and try to import ML-LPA.

```python
import mllpa
```

If the shell does not return any error, ML-LPA is correctly installed in your environment.

## What is next?

Now that ML-LPA has been correctly installed on your computer, you can start using it to **analyse your lipid bilayers.**

If you need to get started in how to use ML-LPA, please visit the [Tutorials](/tutorials/) section of the website.
