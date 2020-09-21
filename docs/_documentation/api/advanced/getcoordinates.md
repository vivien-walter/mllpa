---
title: "getCoordinates()"
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

getCoordinates() is a function used to transform the atom positions into coordinates
by centering them around their center of masses and rotation along a common axis.

The position array can be obtained using the function [extractPositions()](/mllpa/documentation/api/advanced/extractpositions/).
The molecule type information dictionary can be obtained using the function [getMolInfos](/mllpa/documentation/api/advanced/getmolinfos/).

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Positions | | np.ndarray | Array of the positions of the atoms of the molecules. Dimension(s) should be in (N frames, N molecules, N atoms per molecule, 3). |
| Type info | | dict | Dictionary containing all the informations on the molecule type. Can be extracted with read_simulation.getMolInfos() |
| Up | up= | bool | (Opt.) Check that the molecules are always orientated pointing "up". |

### Output(s)

| Name | Type | Description |
|---|---|---|
| New Positions | np.ndarray | Array of the coordinates of the atoms of the molecules. Dimension(s) are in (N frames, N molecules, N atoms per molecule, 2). |

## Examples

### Convert a position array

The following example will convert the position array *atom_positions*, using the dictionary
of information on the molecule type *mol_types*, into the array of coordinates *coordinates_array* that can be used in ML-LPA.

```python
import mllpa

coordinates_array = mllpa.getCoordinates(atom_positions, mol_types)
```
