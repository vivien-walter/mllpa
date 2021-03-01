# ML-LPA

Machine Learning-assisted Lipid Phase Analysis

![Version](https://img.shields.io/badge/version-1.0-f39f37)

[LINK TO THE PROJECT WEBSITE](https://vivien-walter.github.io/mllpa/)

## General informations

**Date:** 21/09/2020

**Author(s), Contact & Affiliation(s):**
- Vivien WALTER (<walter.vivien@gmail.com>) *(1)*
- Olivier BENZERARA (<olivier.benzerara@ics-cnrs.unistra.fr>) *(2)*
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

#### **Using PyPi**

To install ML-LPA using a terminal and PyPi, simply use the following command

```sh
> pip install mllpa
```

The PyPi repo can be found on this [link](https://pypi.org/project/mllpa/).

#### **Using the GitHub repo**

ML-LPA can be installed directly from the source files available on our GitHub repo. The detailed process to install from these files is described below:

1. Get the files, by clicking on **Code > Download ZIP**.

2. Unzip the folder, open it in the Terminal and navigate inside the *source/*.

3. Run the installation

    ```sh
    > python3 setup.py install
    ```

Detailed instructions can be found on the [website of the project](https://vivien-walter.github.io/mllpa/).

### Tutorials and API

All the documentation on ML-LPA can be found on the [website of the project](https://vivien-walter.github.io/mllpa/).
