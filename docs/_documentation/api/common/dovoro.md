---
title: "doVoro()"
section: "api/common"
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

doVoro() is a function used to tessellate the system. The tessellations collect the volumes
(areas if 2-dimensions), vertices and neighbor lists of each molecule. The result of the tessellation
and all the relevant informations are stored in an instance of the Tessellation class.
More informations on the System class can be found in the [related API reference](/mllpa/documentation/api/classes/system/).

It is essential to select the correct geometry for the system to compute the relevant tessellation.
Extensive explanations are given in the [related tutorial](/mllpa/documentation/tutorials/tessellations/1-voronoi/#defining-the-geometry).

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Systems | | list of classes System | Instances of the System classes containing the molecules to save in a file. |
| Geometry | geometry= | str | (Opt.) Geometry of the system to perform the tessellations on. Complete list is given in the [related tutorial](/mllpa/documentation/tutorials/tessellations/1-voronoi/#the-membrane-geometry). By default, the geometry is set to a (2D) bilayer.
| Threshold | threshold= | float | (Opt.) Relative area/volume threshold at which neighbours starts to be considered. Value is given as a percentage of the total area/volume. Default is 0.01 (1%). |
| Exclude Ghosts | exclude_ghosts= | list of int | (Opt.) List of systems indices, provided with the same order than in the argument systems, that should be excluded from ghost generation. Default is None. |
| Read Neighbors | read_neighbors= | bool | (Opt.) Automatically map the local environment after the tessellation. Default is True |

### Output(s)

| Name | Type | Description |
|---|---|---|
| Representation | class Tessellation | Instance of the class Tessellation including the representation on the system and its Voronoi tessellation. |

## Examples

### Tessellate 1 system with a 2D bilayer geometry

The following example will tessellate one instance of the System class, *system_A*,
based on the given geometry *bilayer* and store the result in the instance of the Tessellation class
named *voronoi*

```python
import mllpa

voronoi = mllpa.doVoro(system_A, geometry='bilayer')
```

### Tessellate 1 system with a 3D bilayer geometry but do not map the neighbors

The following example will tessellate one instance of the System class, *system_A*,
based on the given geometry *bilayer* and store the result in the instance of the Tessellation class
named *voronoi*. The local environment of the molecules will not be maped by setting *read_neighbors=*
to False.

```python
voronoi = mllpa.doVoro(system_A, geometry='bilayer_3d', read_neighbors=False)
```

### Tessellate 2 systems with a 3D vesicle geometry and a different threshold

The following example will tessellate two instances of the System class, *system_A* and *system_B*,
based on the given geometry *vesicle_3d* and store the result in the instance of the Tessellation class
named *voronoi*. Spurious neighbors will be removed with a threshold of 5% (*0.05*)

```python
voronoi = mllpa.doVoro([system_A, system_B], geometry='vesicle_3d', threshold=0.05)
```

### Tessellate 2 systems with a 2D vesicle geometry and exclude one system from the ghost generation

The following example will tessellate two instances of the System class, *system_A* and *system_B*,
based on the given geometry *vesicle* and store the result in the instance of the Tessellation class
named *voronoi*. The first system of the list (*0*), *system_A*, will be excluded from the lipid ghost
generation.

```python
voronoi = mllpa.doVoro([system_A, system_B], geometry='vesicle', exclude_ghosts=[0])
```

## Related tutorials

The following tutorial(s) detail further the use of the *doVoro()* function:

* [Voronoi tessellations](/mllpa/documentation/tutorials/tessellations/1-voronoi/)

* [Analysis without phases](/mllpa/documentation/tutorials/tessellations/3-no-phases/)
