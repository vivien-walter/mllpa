---
title: "extractPositions()"
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

extractPositions() is a function used to extract the position array of all the atoms of the selected molecule type,
as well as the dimension of the simulation boxes.
The resulting arrays are in the format and dimensions used my ML-LPA for all the standard analysis.

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Coordinates file | | str | Relative path to the coordinates file of the system (e.g. .gro file). |
| Type | | str | Name of the molecule type to extract the information from. The type should be similar as the one listed in getTypes(). |
| Trajectory file | trj= | str | (Opt.) Relative path to the trajectory file of the system (e.g. .xtc file, .trr file). If not provided, the function will only read the positions from the coordinates file. |
| Heavy | heavy= | bool | (Opt.) Only extract the positions of the non-hydrogen atoms. Default is True. |
| Type info | type\_info= | dict | (Opt.) Dictionary containing all the informations on the molecule type. Can be extracted with read_simulation.getMolInfos(). If not provided, the function will read extract the required informations from the coordinates file. |
| Begin | begin= | int | (Opt.) First frame to read in the trajectory. Cannot be lower than 0 or higher or equal than the final frame to read. Default is 0 (first frame of the trajectory). |
| End | end= | int | (Opt.) Last frame to read in the trajectory. Cannot be higher or equal to the length of the trajectory or lower or equal to the first frame to read. Default is the last frame of the trajectory. |
| Step | step= | int | (Opt.) Step between frame to read. Cannot be lower or equal to 0. Default is 1. |

### Output(s)

| Name | Type | Description |
|---|---|---|
| Positions | np.ndarray | Array of the positions of the atoms of the molecules. Dimension(s) are in (N frames, N molecules, N atoms per molecule, 3). |
| Boxes | np.ndarray | Array of the box dimensions. Dimension(s) are in (N frames, 3). |

## Examples

### Open a single frame

The following example will extract the *DPPC* molecules found in the files *test.gro* and *test.tpr*
and return the positions in the array *atom_positions*.

```python
import mllpa

atom_positions, simulation_boxes = mllpa.extractPositions('test.gro', 'test.tpr', 'DPPC')
```

### Open a whole trajectory

The following example will extract the *DPPC* molecules found in all the frames the files *test.gro*, *test.tpr* and *test.xtc*
and return the positions in the array *atom_positions*.

```python
atom_positions, simulation_boxes = mllpa.extractPositions('test.gro', 'test.tpr', 'DPPC', trj='test.xtc')
```

### Open a selection of frames in the trajectory

The following example will extract the *DPPC* molecules found in all the frames the files *test.gro*, *test.tpr* and *test.xtc*
and return the positions in the array *atom_positions*, but will only read the frames from 100 to 500, skipping every 10 frames.

```python
atom_positions, simulation_boxes = mllpa.extractPositions('test.gro', 'test.tpr', 'DPPC', trj='test.xtc', begin = 100, end = 500, step=10)
```
