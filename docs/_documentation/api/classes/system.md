---
title: "System"
section: "api/classes"
path: ""
category:
  - api
tags:
  - training
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-api"
---

## Description

The System class is a class used to store all the information on the atoms belonging to a specific
molecule type and required to process Machine Learning training and predictions in ML-LPA.

## Attributes and Methods

### Initialisation

Instances of the System class can be generated in ML-LPA via two functions:

* [openSystem()](/mllpa/documentation/api/common/opensystem/)

* [systemFromPositions()](/mllpa/documentation/api/advanced/systemfrompositions/)

It is recommended to use these functions to generate the instances of the class. However, if
one wants to generate it by calling the class, the following data are required:

1. The **name** of the molecule type, as listed by the [getTypes()](/mllpa/documentation/api/advanced/gettypes/) function.

2. The **array of positions** of the atom in the correct dimensions, as extracted
by the [extractPositions()](/mllpa/documentation/api/advanced/extractpositions/) function.

3. The **dictionary of information** of the molecule type, as extracted by the
[getMolInfos()](/mllpa/documentation/api/advanced/getmolinfos/) function.

4. The **array of dimensions** of the simulation box over time, in the correct dimensions, as extracted
by the [extractPositions()](/mllpa/documentation/api/advanced/extractpositions/) function.

### Attributes

| Name | Type | Description |
| --- | --- | --- |
| **system.type** | str | Name of the molecule type stored in the instance. |
| **system.positions**  | np.ndarray | Positions of all the atoms of each molecules collected. |
| **system.boxes** | np.ndarray | Dimensions of the simulation box. |
| **system.infos** | dict | Dictionary containing all relevant informations on the molecules (e.g. atom masses, bonds). |
| **system.coordinates** | np.ndarray | Coordinates of the atoms of each molecule, after centering the molecule on their centers of mass and rotation.
| **system.distances** | np.ndarray | Distances between atoms pairs, pairs are set to a given neighbor rank. |
| **system.rank** | int | Rank used for the distance calculation. |
| **system.states** | np.ndarray | States of each molecules in the system. |

### Methods

| Name | Argument(s) | Description |
| --- | --- | --- |
| **system.getCoordinates()** | <ul><li>up=, {bool}, (Opt.) Make sure the molecule is always pointing "up". Default is True.</li></ul> | Compute the coordinate set based on the atom positions of the system. The results are directly stored in the instance. |
| **system.getDistances()** | <ul><li>rank=, {int}, (Opt.) Rank for the distance calculation. Default is 6.</li></ul> | Calculate the distance between atom pairs based on the atom positions of the system and the neighbor rank. The results are directly stored in the instance. |
| **system.getStates()** | <ul><li>models, {str or dict of models}, Path to the model files or dictionary of the models to use to predict the states.</li></ul> | Predict the states of all the molecules in the system using the provided models. Return the array of states. |
| **system.setStates()** | <ul><li>states, {str or np.ndarray}, States to apply to the molecules of the system.</li></ul> | Set manually the states of all the molecules in the system using the provided models. Return the array of states. |

## Examples

### Initialise an instance of the class

The following example will initialise an instance of the System class, named here *loaded_system*,
from the given molecule type *DPPC*, the position array *atom_positions*, the dictionary of type information
*mol_infos*, and the array of dimensions of the simulation boxes, *simulation_boxes*.

```python
from mllpa.system_class import System

loaded_system = System("DPPC", position_array, mol_infos, simulation_boxes)
```

### Convert the positions into coordinates

The following example will convert the position array inside the instance of the System class *loaded_system*
into the array of coordinates directly stored in the instance.

```python
loaded_system.getCoordinates()
```

### Convert the positions into distances

The following example will convert the position array inside the instance of the System class *loaded_system*
into the array of distances directly stored in the instance. The conversion will use a neighbor rank equals to 6.

```python
loaded_system.getDistances(rank=6)
```

### Prediction with a model file

The following example will use the model file *new_model.lpm* to predict the phase of *loaded_system*,
an instance of the System class. The output will be stored in the attributes of the instance.

```python
loaded_system.getStates("./new_model.lpm")
```

### Prediction with a model dictionary

The following example will use the models stored in the variable *models* to predict the phase of *loaded_system*,
an instance of the System class. The output will be stored in the instance.

```python
loaded_system.getStates(models)
```

### Assigning a single phase

The following example will assign the phase name *fluid* to all molecules of *loaded_system*,
an instance of the System class. The output will be stored in the attributes of the instance.

```python
loaded_system.setStates("fluid")
```

### Assigning a phase array

The following example will assign the array of phases *phase_array* to *loaded_system*,
an instance of the System class. The output will be stored in the instance of the System class.

```python
loaded_system.setStates(phase_array)
```

## Related functions

The following function(s) uses the System class either in their input our output:

* **Common functions**

    * [openSystem()](/mllpa/documentation/api/common/opensystem/)

    * [generateModel()](/mllpa/documentation/api/common/generatemodel/)

    * [getStates()](/mllpa/documentation/api/common/getstates/)

    * [setStates()](/mllpa/documentation/api/common/setstates/)

    * [saveSystems()](/mllpa/documentation/api/common/savesystems/)

    * [doVoro()](/mllpa/documentation/api/common/dovoro/)

* **Advanced functions**

    * [systemFromPositions()](/mllpa/documentation/api/advanced/systemfrompositions/)

## Related tutorials

The following tutorial(s) detail further the use of the *getStates()* function through the *.getStates()* method of
the system class:

* [Load from simulation files](/mllpa/documentation/tutorials/loading-files/1-simulation-files/)

* [Load from position array](/mllpa/documentation/tutorials/loading-files/2-positions/)

* [Attributes of the System class](/mllpa/documentation/tutorials/system-class/1-description/)

* [Methods of the System class](/mllpa/documentation/tutorials/system-class/2-methods/)

* [Machine Learning algorithms training](/mllpa/documentation/tutorials/phase-prediction/1-training/)

* [Optimisation of the neighbour rank](/mllpa/documentation/tutorials/phase-prediction/2-rank-optimisation/)

* [Lipid phase prediction](/mllpa/documentation/tutorials/phase-prediction/3-ml-prediction/)

* [Setting phases manually](/mllpa/documentation/tutorials/phase-prediction/4-set-phases/)

* [Voronoi tessellation](/mllpa/documentation/tutorials/tessellations/1-voronoi/)

* [Save the System class](/mllpa/documentation/tutorials/outputs/2-save-system/)
