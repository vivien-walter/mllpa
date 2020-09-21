---
title: "Attributes of the System class"
section: "tutorials/system-class"
path: ""
category:
  - tutorial
tags:
  - system
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-tutorials"
---

In a standard quick and dirty use of ML-LPA, using or just accessing the **attributes of an instance of the System class**
does not bear too much interest. However, it is good to know what can be found inside the class if needed.
We describe in this tutorial some of the most useful attributes of the class.

If you are only interested in getting ML-LPA to work quickly, we recommend to directly
move to the tutorials on [phase prediction]().
{: .notice--info}

## General description

The **System class** as defined in ML-LPA contains all the relevant informations on a **molecule type** as extracted from simulation files.
In addition to the information **directly extracted** from the simulation, it also contains informations **computed** from the former.

Each instance of the System class is specific to only **one molecule type**. This is due to
constraints on the calculations run inside the class. In a multi-molecule types simulation, it
is therefore required to create one instance of the class per type.

## Useful attributes

### Atom positions

The first data that one might want to extract from the instance of the System class
are the **positions of the atom at each frame**. This can be done by using the attribute *.positions*

```python
import mllpa

loaded_system = mllpa.openSystem('test.gro', 'test.tpr', 'DPPC')

atom_positions = loaded_system.positions
```

In this example, we use the *openSystem()* function to load the information from
the simulation files. Check the [related tutorial](/mllpa/documentation/tutorials/loading-files/1-simulation-files/) for more details.
{: .notice--info}

The positions are stored in a **NumPy array** with the dimension

```(# frames, # molecules, # atom per molecules, # dimensions)```

The expected number of dimensions is 3, since the simulation boxes are always defined in a Cartesian system of coordinates.
{: .notice--info}

For example, a 10 frames simulation box with 26 DPPC molecules made of 130 atoms each should have an array of dimension ```(10, 26, 130, 3)```.
{: .notice--info}

### Coordinates and distances

The Machine Learning algorithms used in ML-LPA to predict the phase of the lipids do not work
directly with the atom positions. Instead, they use the **atom coordinates** in a cylindrical
system of coordinates (with the Z axis aligned to the main axis of inertia of the molecule) and
the **intra-molecular distances** at a specific neighbor rank (a pair of atoms at the neighbor rank N
are separated by N-1 atoms along a chain).

Using the instance of the System class, it is possible to extract these data using the attributes
*.coordinates* and *.distances*

```python
atom_coordinates = loaded_system.coordinates
molecule_distances = loaded_system.distances
```

The coordinates and distances are stored in a **NumPy array** with the respective dimensions

```(# frames, # molecules, # atom per molecules, # dimensions - 1)```

and

```(# frames, # molecules, # distances)```

The expected number of dimensions for the coordinates is 2, since the azimuth of the cylindrical system is discarded.
{: .notice--info}

For example, a 10 frames simulation box with 26 DPPC molecules made of 130 atoms each should have an array of dimension ```(10, 26, 130, 2)```.
{: .notice--info}

The number of distances in a molecule depends both on the number of atoms in the molecules, the shape of the molecule and the rank selected.
{: .notice--info}

### Molecule type information

The instance also includes an important number of **information on the molecule type** which was extracted from the structure file.
All these information are stored in a dictionary that can be get from the attribute *.infos*

```python
molecule_type_infos = loaded_system.infos
```

Among the several information found in this dictionary, the useful ones are (i) the atom IDs, (ii) the atom names and (iii) the atom masses. They can all
be extracted using the following keys:

```python
atom_ids = molecule_type_infos["heavy_atoms"]["ids"]
atom_names = molecule_type_infos["heavy_atoms"]["names"]
atom_masses = molecule_type_infos["heavy_atoms"]["masses"]
```

Both all (*atoms*) and non-hydrogen (*heavy_atoms*) atoms are listed in the dictionary, hence the first key.

You can find the list and description of all the keys in the [API]().

## What is next?

* Now that you know how what exactly is the System class, you can either use it to [prepare and train a model]() for
    machine learning analysis, or use an existing model to predict the [phases in the system]().

## Check the API

The following elements have been used in this tutorial:

* openSystem

* System class
