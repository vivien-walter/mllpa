# ML-LPA

Machine Learning-assisted Lipid Phase Analysis

![Version](https://img.shields.io/badge/version-1.0-f39f37)

[LINK TO THE PROJECT WEBSITE](https://vivien-walter.github.io/mllpa/)

## General informations

**Date:** 21/09/2020

**Author(s), Contact & Affiliation(s):**
- Vivien WALTER (<walter.vivien@gmail.com>) *(1)*
- Olivier BENZERARA *(2)*
- Celine RUSCHER *(2)*
- Fabrice THALMANN *(2)*

*(1)* Department of Chemistry, King's College London (UK)

*(2)* Institut Charles Sadron, CNRS, Universite de Strasbourg (FR)

## Description

### General Description

ML-LPA is a Python 3 module made to analyse simulation files and run Machine Learning analysis but also Voronoi tessellations on the molecules contained inside.

The module has been specifically designed to analyse the thermodynamic phases of individual lipid molecules inside cell membranes (e.g. DPPC, DSPC);
and optimised to work on all-atom representation (e.g. Charmm36). However, the module has been written to analyse unified-atom or coarse grain
(e.g. Martini) representations as well, and can be used to analyse the states of any molecule selected.

### References

#### Package(s) used

The module is based on other Python modules that have also been published, namely:

- **MDAnalysis**, to open and read the simulation files (Michaud-Agrawal et al. *MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations.* J. Comput. Chem. 32 (2011), 2319-2327).
- **Scikit-Learn**, to perform the Machine Learning training and predictions on the systems (Pedregosa et al., *Scikit-learn: Machine Learning in Python*, Journal of Machine Learning Research 12 (2011), 2825-2830).
- Tess, which is based on the C++ library **voro++**, to perform the tessellation on the systems (Chris H. Rycroft. *Voro++: A three-dimensional voronoi cell library in c++*. Chaos (2008), 19(041111)).

#### Literature

* **Cite us**

If you use this package for your research, please cite the following publication:

> Walter et al. A machine learning study of the two states model for lipid bilayer phase transitions, PCCP (2020), 22, 19147-19154

* **Published example(s)**

Applications of the module can be found in the literature:

> Walter et al. A machine learning study of the two states model for lipid bilayer phase transitions, PCCP (2020), 22, 19147-19154

## Documentation

### Installation

#### **Using the GitHub repo**

ML-LPA can be installed directly from the source files available on our GitHub repo. The detailed process to install from these files is described below:

1. Get the files, by clicking on **Code > Download ZIP**.

2. Unzip the folder, open it in the Terminal and navigate inside the *source/*.

3. Run the installation

    ```sh
    > python3 setup.py install
    ```

Detailed instructions can be found on the [website of the project](https://vivien-walter.github.io/mllpa/).

### Command-Line Interface

In addition to the function in Python, ML-LPA is shipped with some CLI commands to be directly used in the terminal.
The commands currently implemented in ML-LPA as CLI are listed below.

#### Model training

The CLI of ML-LPA *mllpa train_model* can be used to train a series of Machine Learning models and generate a
model file that can be used later to predict the phases in unknown systems.

The command takes as arguments a set of coordinates (*-c*) and structure file (*-s*) for each of the
phases provided (*-p*). Optionaly, trajectory files can also be loaded (*-t*). The
name of the molecule type to read should be specified (*-mol*). The path to the output file
to create can be specified with the argument *-o*.

```sh
> mllpa train_model -c gel.gro fluid.gro -s gel.tpr fluid.tpr -mol DPPC -p gel fluid -o model_file.lpm
```

More details on the argument can be obtained with the *-h* or *--help* flags.

#### Lipid phase prediction

The command *mllpa read_phases* can be used to find the phases of the
molecules in simulation file(s), based on a pre-trained Machine Learning model.
The results are returned inside a file containing the centers of mass of all
the particles in the system.

The command takes as arguments a coordinates (*-c*) and structure file (*-s*).
Optionaly, trajectory files can also be loaded (*-t*). Each molecule type to process should
be listed with *-mol* and each have their model or label specified with *-m*. The path to the output file
to create can be specified with the argument *-o*.

```sh
> mllpa read_phases -c unknown.gro -s unknown.tpr -mol DPPC DOPC -m model_file.lpm fluid -o system_contents.csv
```

More details on the argument can be obtained with the *-h* or *--help* flags.

#### Local environment analysis

The command *mllpa do_voronoi* can be used to analyse the local
environment of the molecules using a Voronoi tessellations to map the neighbors.
The results are returned inside a file containing the centers of mass of all
the particles in the system.

The command takes as arguments a coordinates (*-c*) and structure file (*-s*).
Optionaly, trajectory files can also be loaded (*-t*). Each molecule type to process should
be listed with *-mol* and each have their model or label specified with *-m*. The path to the output file
to create can be specified with the argument *-o*. The geometry of the system should
be specified with *-geo*.

```sh
> mllpa do_voronoi -c unknown.gro -s unknown.tpr -mol DPPC DOPC -m model_file.lpm fluid -o system_contents.csv -geo bilayer
```

More details on the argument can be obtained with the *-h* or *--help* flags.

#### Reading model file

The command *mllpa read_model* can be used to read the content of
a model file and display all the values stored inside it. The
path of the model file should be specified with *-m*.

```sh
> mllpa read_model -m model_file.lpm
```

More details on the argument can be obtained with the *-h* or *--help* flags.

### Tutorials and API

All the documentation on ML-LPA can be found on the [website of the project](https://vivien-walter.github.io/mllpa/).
