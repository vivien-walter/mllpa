---
title: "summonGhosts()"
section: "api/advanced"
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

summonGhosts() is a function used to generate the ghosts of the membrane molecules,
in order to avoid spurious neighbors in the Voronoi tessellation due to the system geometry
and the PBC. Extensive explanations on ghosts are provided in the [related tutorial](/mllpa/documentation/tutorials/tessellations/1-voronoi/#ghost-lipids).

During a normal use of ML-LPA, ghosts are automatically generated if needed by the [doVoro()](/mllpa/documentation/api/common/dovoro/) function. The function summonGhosts() is only used if one wants to extract the ghosts to
study them.

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Systems | | list of classes System | Instances of the System classes containing the molecules to save in a file. |
| Geometry | geometry= | str | (Opt.) Geometry of the system to perform the tessellations on. Complete list is given in the [related tutorial](/mllpa/documentation/tutorials/tessellations/1-voronoi/#the-membrane-geometry). By default, the geometry is set to a (2D) bilayer.
| Exclude Ghosts | exclude_ghosts= | list of int | (Opt.) List of systems indices, provided with the same order than in the argument systems, that should be excluded from ghost generation. Default is None. |

### Output(s)

| Name | Type | Description |
|---|---|---|
| Ghosts | np.ndarray | Position array of all the molecule ghosts generated for the Voronoi tessellation. |

## Examples

### Tessellate 1 system with a 2D bilayer geometry

The following example will generate the ghosts using one instance of the System class, *system_A*,
based on the given geometry *bilayer* and return the ghost positions in the array *ghost_array*.

```python
import mllpa

ghost_array = mllpa.summonGhosts(system_A, geometry='bilayer')
```

### Tessellate 2 systems with a 2D vesicle geometry and exclude one system from the ghost generation

The following example will generate the ghosts using two instances of the System class, *system_A* and *system_B*,
based on the given geometry *vesicle* and return the ghost positions in the array *ghost_array*. The first system of the list (*0*), *system_A*, will be excluded from the lipid ghost generation.

```python
ghost_array = mllpa.summonGhosts([system_A, system_B], geometry='vesicle', exclude_ghosts=[0])
```
