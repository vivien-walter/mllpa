---
title: "getDistances()"
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

getDistances() is a function used to transform the atom positions into intra-molecular distances
by measuring the distances between atom pairs at a given rank.

The position array can be obtained using the function [extractPositions()](/mllpa/documentation/api/advanced/extractpositions/).
The molecule type information dictionary can be obtained using the function [getMolInfos](/mllpa/documentation/api/advanced/getmolinfos/).

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Positions | | np.ndarray | Array of the positions of the atoms of the molecules. Dimension(s) should be in (N frames, N molecules, N atoms per molecule, 3). |
| Type info | | dict | Dictionary containing all the informations on the molecule type. Can be extracted with read_simulation.getMolInfos() |
| Rank | rank= | int | (Opt.) Number of atoms (-1) between two neighbours along the same line used for distance calculations. At rank 1, the neighbours of an atom are all atom sharing a direct bond with it. Default is 6. |

### Output(s)

| Name | Type | Description |
|---|---|---|
| Distances | np.ndarray | Array of the distances of the atoms of the molecules. Dimension(s) are in (N frames, N molecules, N distances). |

## Examples

### Convert a position array

The following example will convert the position array *atom_positions*, using the dictionary
of information on the molecule type *mol_types*, into the array of distances *distances_array* that can be used in ML-LPA.

```python
import mllpa

distances_array = mllpa.getDistances(atom_positions, mol_types)
```

### Select the neighbor rank

The following example will convert the position array *atom_positions*, using the dictionary
of information on the molecule type *mol_types*, into the array of distances *distances_array* that can be used in ML-LPA.
Here, a neighbor rank of 4 instead of 6 for the generation of the intra-molecular distances will be used

```python
distances_array = mllpa.getDistances(atom_positions, mol_types, rank=4)
```
