# ML-LPA

Machine Learning-assisted Lipid Phase Analysis

## General informations

**Version:** 1.0

**Date:** 09/2020

**Author(s), Contact & Affiliation(s):**
- Vivien WALTER (<walter.vivien@gmail.com>) *(1)*
- Olivier BENZERARA *(2)*
- Celine RUSCHER *(2)*

*(1)* Department of Chemistry, King's College London (UK)

*(2)* Institut Charles Sadron, CNRS, Universite de Strasbourg (FR)

## Description

### General Description

ML-LPA is a Python 3 module made to analyse simulation files and run Machine Learning analysis but also Voronoi tessellations on the molecules contained inside.

The module has been specifically designed to analyse the thermodynamic phases of individual lipid molecules inside cell membranes (e.g. DPPC, DSPC);
and optimised to work on all-atom representation (e.g. Charmm36). However, the module has been written to analyse unified-atom or coarse grain
(e.g. Martini) representations as well, and can be used to analyse the states of any molecule selected.

### References

Applications of the module can be found in the literature:

> Walter et al. A machine learning study of the two states model for lipid bilayer phase transitions, PCCP (2020), 22, 19147-19154

The module is based on other Python modules that have also been published, namely:

- **MDAnalysis**, to open and read the simulation files (Michaud-Agrawal et al. *MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations.* J. Comput. Chem. 32 (2011), 2319-2327).
- **Scikit-Learn**, to perform the Machine Learning training and predictions on the systems (Pedregosa et al., *Scikit-learn: Machine Learning in Python*, Journal of Machine Learning Research 12 (2011), 2825-2830).
- Tess, which is based on the C++ library **voro++**, to perform the tessellation on the systems (Chris H. Rycroft. *Voro++: A three-dimensional voronoi cell library in c++*. Chaos (2008), 19(041111)).
