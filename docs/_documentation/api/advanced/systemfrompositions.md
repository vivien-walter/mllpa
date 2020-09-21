---
title: "systemFromPositions()"
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

systemFromPositions() is a function similar to [openSystem()](/mllpa/documentation/api/common/opensystem/) used to load the simulation
files to be analysed. The function will use position arrays instead of simulation files.
More informations on the System class can be found in the [related API reference]().

Similarly to the *openSystem()* function, systemFromPositions() can only load one molecule type at a time.

The position and simulation box arrays can be obtained using the function [extractPositions()](/mllpa/documentation/api/advanced/extractpositions/).
The molecule type information dictionary can be obtained using the function [getMolInfos](/mllpa/documentation/api/advanced/getmolinfos/).

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description|
|---|---|---|---|
| Positions | |np.ndarray | Array of the positions of the atoms of the molecules. Dimension(s) should be in (N frames, N molecules,  N atoms per molecule, 3). |
| Type | | str | Molecule type to load from the simulation file. |
| Type infos |  | dict | Dictionary containing all the informations on the molecule type. Can be extracted with getMolInfos() |
| Boxes | | np.ndarray | Array of the box dimensions. Dimension(s) are in (N frames, 3). |
| Up | up= | bool | (Opt.) Check that the molecules are always orientated pointing "up". Default is True. |
| Rank | rank= | int | (Opt.) Number of atoms (-1) between two neighbours along the same line used for distance calculations. At rank 1, the neighbours of an atom are all atom sharing a direct bond with it. Default is 6. |

### Output(s)

| Name | Type | Description|
|---|---|---|
| System | class System | Instance of the system classes containing all the informations on the system as well as the positions and configurations. |

## Examples

### Load the position in the System class

The following example will load for the given molecule type *DPPC* a position array,
*atom_positions*, a dictionary of type information, *mol_infos*, and the array of dimensions
of the simulation boxes, *simulation_boxes*, into an instance of the System class named here *loaded_system*.

```python
import mllpa

types_list = mllpa.systemFromPositions(atom_positions, 'DPPC', mol_infos, simulation_boxes)
```

### Select the neighbor rank

The following example will load for the given molecule type *DPPC* a position array,
*atom_positions*, a dictionary of type information, *mol_infos*, and the array of dimensions
of the simulation boxes, *simulation_boxes*, into an instance of the System class named here *loaded_system*.
Here, a neighbor rank of 4 instead of 6 for the generation of the intra-molecular distances will be used.

```python
types_list = mllpa.systemFromPositions(atom_positions, 'DPPC', mol_infos, simulation_boxes, rank=4)
```

## Related tutorials

The following tutorial(s) detail further the use of the *getTypes()* function:

* [Load from position array](/mllpa/documentation/tutorials/loading-files/2-positions/)
