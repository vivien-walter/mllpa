---
title: "assignLeaflets()"
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

assignLeaflets() is a function used to identify the leaflets in which the membrane molecules are found. Extensive explanations on
why leaflets are essential and why membrane geometries are esential can be found in the
[related tutorial](/mllpa/documentation/tutorials/tessellations/1-voronoi/#the-membrane-geometry).

During a normal use of ML-LPA, leaflets are automatically assigned if needed by the [doVoro()](/mllpa/documentation/api/common/dovoro/) function. The function assignLeaflets() is only used if one wants to extract the leaflets to
study them.

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Systems | | list of classes System | Instances of the System classes containing the molecules to save in a file. |
| Geometry | geometry= | str | (Opt.) Geometry of the system to perform the tessellations on. Complete list is given in the [related tutorial](/mllpa/documentation/tutorials/tessellations/1-voronoi/#the-membrane-geometry). By default, the geometry is set to a (2D) bilayer.

### Output(s)

| Name | Type | Description |
|---|---|---|
| Leaflets | np.ndarray | Array of the leaflets assigned to the membrane molecules. |

## Examples

### Tessellate 1 system with a 2D bilayer geometry

The following example will assign the leaflets in one instance of the System class, *system_A*,
based on the given geometry *bilayer* and return the result in the array *leaflet_array*

```python
import mllpa

leaflet_array = mllpa.assignLeaflets(system_A, geometry='bilayer')
```

### Tessellate 2 systems with a 3D vesicle geometry

The following example will assign the leaflets in two instances of the System class, *system_A* and *system_B*,
based on the given geometry *vesicle_3d* and return the result in the array *leaflet_array*

```python
leaflet_array = mllpa.assignLeaflets([system_A, system_B], geometry='vesicle_3d')
```
