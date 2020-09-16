---
title: "Load from simulation files"
section: "tutorials/loading-files"
path: ""
category:
  - tutorial
tags:
  - file access
  - system
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-tutorials"
---

In order to analyse a simulation with ML-LPA, the simulation files should first be **loaded into ML-LPA**. We describe in this
tutorial how to load the files.

## Load the files

### Single frame

This is done using the *openSystem()* function. To load a single frame (no trajectory), one can use directly the command below in a Python script.

```python
import mllpa

loaded_system = mllpa.openSystem('test.gro', 'test.tpr', 'DPPC')
```

In this example, the coordinates and structure files are respectively called *test.gro* and *test.tpr*. The molecule loaded is *DPPC*.
See section *Advanced information* below for more details
{: .notice--info}

All the relevant information on the DPPC molecules found in the simulation files have been extracted and stored in the variable *loaded_system* as
an instance of the **System** class. More information on the System class are given in the [related tutorial]() and in the [API]().

### Full trajectory

To load a trajectory file as well, use the corresponding *trajectory_file=* keyword-arguments:

```python
import mllpa

loaded_system = mllpa.openSystem('test.gro', 'test.tpr', 'DPPC', trajectory_file="test.xtc")
```

In this example, the trajectory file is called *test.xtc*
{: .notice--info}

You can find the description of all the keyword-arguments in the [API]().

## Advanced information

### Type(s) of file

ML-LPA relies on the scientific library [MDAnalysis](https://www.mdanalysis.org) to open the simulation files.
As a consequence, ML-LPA shares the **same file format support as MDAnalysis**. The complete list of file formats currently
supported by MDAnalysis can be found [in this link](https://www.mdanalysis.org/docs/documentation_pages/coordinates/init.html#supported-coordinate-formats).

Loading a simulation in ML-LPA requires at least two files: a **coordinates file** and a **structure file**. To load and analyse multiple frames, a **trajectory file** can also
be loaded, but it is not required.

* **Coordinates file**: file containing the **positions** of the particles (*e.g.* atoms) of the system.

* **Structure file**: file containing the **structure and topology**, typically the bonds between atoms, of the molecules of the system.

* **Trajectory file**: file containing the **positions** of the particles (*e.g.* atoms) of the system over time.

We provide below a list of some file formats for each of the file types required, with the associated MD software used to generate the files.

| Software | Coordinates | Structure | Trajectory |
|---|---|---|---|
| GROMACS | .gro, .pdb | .tpr | .trr, .xtc |

We only include in this table the file format that have been tested so far. Since we
have not tested all the file format supported by MDAnalysis, this section will be completed
over time.
{: .notice--info}

### Molecule type selection

Because of the **calculation constraints** in ML-LPA, mostly on the number of atom per molecules,
**only one type of molecule** can be extracted from the simulation files and loaded at the time.

The name of the molecule type should match exactly the **name defined in the simulation**.
If you are unsure about the exact name of the molecule type you want to extract, you can
use the function *getTypes()* of ML-LPA to extract the list of molecule type names found in the files.
This function only takes the **coordinates file** as an input.

```python
import mllpa

molecule_types_list = mllpa.getTypes('test.gro')
```

The list is saved here in the variable *molecule_types_list* and can simply be displayed
with the command ```print(molecule_types_list)```.

## What is next?

* Now that you know how to load a system, you can either use it [prepare and train a model]() for
    machine learning analysis, or use an existing model to predict the [phases in the sytem]().

* If you want to know more about the System class, you either read the [tutorials on it](), or go
    to its [API]().

* If you need to directly load the positions from an array, you can have a read at the [corresponding tutorial](/documentation/tutorials/loading-files/2-positions/).

## Check the API

The following elements have been used in this tutorial:

* openSystem

* getTypes
