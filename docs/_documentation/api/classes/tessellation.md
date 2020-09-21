---
title: "Tessellation"
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

The class Tessellations is used to store all informations required to perform a Voronoi tessellation
on the molecules of the system, along with all elements obtained through the tessellation.
After a neighbor analysis, the information are also stored in the instance of the class.

## Attributes and Methods

### Initialisation

Instances of the Tessellation class can be generated in ML-LPA via the function [doVoro()](/mllpa/documentation/api/common/dovoro/).

It is recommended to use this function to generate the instances of the class. However, if
one wants to generate it by calling the class, the following data are required:

1. The **array of names** of all the molecules.

2. The **array of ids** of all the molecules.

3. The **array of the centers of mass** of all the molecules.

4. The **array of dimensions** of the simulation box over time, in the correct dimensions, as extracted
by the [extractPositions()](/mllpa/documentation/api/advanced/extractpositions/) function.

5. The **array of the phases** of the molecules, as extracted by the functions [getPhases()](/mllpa/documentation/api/common/getphases/)
or [setPhases()](/mllpa/documentation/api/common/setphases/).

Please be aware that ghost lipids, required for most of the membrane geometries,
cannot be generated within the Tessellation class.
{: .notice--warning}

### Attributes

| Name | Type | Description |
| --- | --- | --- |
| **tessellation.names** | np.ndarray | Name of the molecule type of each molecule of the system. |
| **tessellation.ids** | np.ndarray | Indices of all the molecules of the system. |
| **tessellation.positions** | np.ndarray | 3D positions of the centers of mass of all the molecules of the system. |
| **tessellation.boxes** | np.ndarray | Dimensions of the simulation box. |
| **tessellation.phases** | np.ndarray | Phases of all the molecules of the system. |
| **tessellation.leaflets** | np.ndarray | Name of the leaflets in which all the molecules can be found, if applicable |
| **tessellation.ghosts** | np.ndarray | 3D positions of the centers of mass of the ghosts of all the molecules of the system, if applicable |
| **tessellation.volumes** | np.ndarray | Volumes - or Areas in 2D - found through the tessellation of all the molecules. |
| **tessellation.vertices** | np.ndarray | Positions of the vertices of the cell of each molecule. |
| **tessellation.neighbors** | np.ndarray | List of the neighbors of all the molecules of the system. |
| **tessellation.geometry** | str | Geometry selected for the tessellation during the generation. |
| **tessellation.threshold** | float | Threshold used to remove sporious neighbors found during the tessellation. |
| **tessellation.neighbors_phases** | np.ndarray | Phases of the neighbors of each molecules of the system. |
| **tessellation.phases_list** | np.ndarray | Name of the phases, in the order provided in **tessellation.neighbors_phases**. |

### Methods

| Name | Argument(s) | Description |
| --- | --- | --- |
| **tessellation.getLeaflets()** | <ul><li>geometry=, {str}, (Opt.) geometry of the system. Default is bilayer.</li></ul> | Find the leaflet in which all the molecules are located. |
| **tessellation.doVoronoi()** | <ul><li>geometry=, {str}, (Opt.) geometry of the system. Default is bilayer.</li><li>threshold=, {float}, (Opt.) threshold used to remove sporious neighbors found during the tessellation. Default is 0.01.</li></ul> | Perform the Voronoi tessellation on the system to find the individual cells of each molecules. |
| **tessellation.checkNeighbors()** | | Determine the state of the neighbors of each molecule of the system. |
| **tessellation.toTable()** | | Collect all the attributes of the instance and convert them into a pandas dataframe. |
| **tessellation.save()** | <ul><li>file_path, {str}, Path and name of the file to generate.</li><li>format, {str}, File extension and format to use for the output file.</li></ul> | Save the instance of the Tessellation class in a file. |

The *.save()* method uses the same argument and generates the same files than the [saveVoro()](/mllpa/documentation/api/common/savevoro/) function.
{: .notice--info}

## Examples

### Initialise an instance of the class

The following example will initialise an instance of the Tessellation class, named here *voronoi*,
from the name array *mol_names*, the position array *mol_positions*, the array of indices *mol_ids*,
the array of dimensions of the simulation boxes, *simulation_boxes* and the array of phases *mol_phases*.

```python
from mllpa.system_class import Tessellation

voronoi = Tessellation(mol_names, mol_ids, mol_positions, simulation_boxes, mol_phases)
```

### Assign molecules to their respective leaflets

The following example will assign the molecules in the instance of the Tessellation class *voronoi*
with the leaflets they can be found in, based on the geometry *bilayer*. The results will
be stored directly in the instance.

``` python
voronoi.getLeaflets(geometry='bilayer')
```

### Do the tessellation

The following example will tessellate the molecules in the instance of the Tessellation class *voronoi*,
based on the geometry *bilayer_3d*, and cures the results from spurious neighbors with a threshold at
1% (*0.01*). All the results will be stored directly in the instance.

``` python
voronoi.doVoronoi(geometry='bilayer_3d', threshold=0.01)
```

### Analyse the local environment

The following example will use a tessellation previously made in the instance of the Tessellation class *voronoi*
to analyse the local environment. The results are both stored in the instance and returned as the
array of the phase environment for each molecule *neighbor_phases* and the list of the phase
names *phases_list* given in the same order than in *neighbor_phases*

``` python
neighbors_phases, phases_list = voronoi.checkNeighbors()
```

### Convert the content into a pandas data frame

The following example will convert the attributes of the instance of the Tessellation class *voronoi*
in a pandas table-like structure *dataframe*.

``` python
dataframe = voronoi.toTable()
```

### Save the instance in a file

The following example will save the content of the instance of the Tessellation class *voronoi*
in a file *test_file.xml*

``` python
voronoi.save(file_path='test_file.xml')
```

## Related functions

The following function(s) uses the System class either in their input our output:

* **Common functions**

    * [doVoro()](/mllpa/documentation/api/common/dovoro/)

    * [readNeighbors()](/mllpa/documentation/api/common/readneighbors/)

    * [saveVoro()](/mllpa/documentation/api/common/savevoro/)

## Related tutorials

The following tutorial(s) detail further the use of the *getStates()* function through the *.getStates()* method of
the system class:

* [Voronoi tessellation](/mllpa/documentation/tutorials/tessellations/1-voronoi/)

* [Map the environment](/mllpa/documentation/tutorials/tessellations/2-local-environment/)

* [Analysis without phases](Analysis without phases)

* [Save the Tessellation class](/mllpa/documentation/tutorials/outputs/3-save-voronoi/)
