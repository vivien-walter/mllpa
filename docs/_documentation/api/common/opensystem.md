---
title: "openSystem()"
section: "api/common"
path: ""
category:
  - api
tags:
  - system
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-api"
---

## Description

openSystem() is a function used to load the simulation files to be analysed.  The function can load either single frames or whole trajectory. Only one type of molecule will be extracted from the files, since Machine Learning models can only be generated on one molecule type at the time. More informations on the System class can be found in the [related API reference]().

It is possible to load directly a position array into ML-LPA and generates an instance of the System class without using simulations files. Please refer to the function [systemFromPositions()]().

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description|
|---|---|---|---|
| Coordinate file | | str | Relative path to the coordinates file of the system (e.g. .gro file). |
| Structure file | | str | Relative path to the structure file of the system (e.g. .tpr file). |
| Type | | str | Molecule type to load from the simulation file. |
| Trajectory file | trajectory_file= | str | (Opt.) Relative path to the trajectory file of the system (e.g. .xtc file, .trr file). If not provided, the function will only read the positions from the coordinates file. Default is None. |
| Heavy | heavy= | bool | (Opt.) Only extract the positions of the non-hydrogen atoms. Default is True. |
| Up | up= | bool | (Opt.) Check that the molecules are always orientated pointing "up". Default is True. |
| Rank | rank= | int | (Opt.) Number of atoms (-1) between two neighbours along the same line used for distance calculations. At rank 1, the neighbours of an atom are all atom sharing a direct bond with it. Default is 6. |
| Begin | begin= | int | (Opt.) First frame to read in the trajectory. Cannot be lower than 0 or higher or equal than the final frame to read. Default is 0 (first frame of the trajectory). |
| End | end= | int | (Opt.) Last frame to read in the trajectory. Cannot be higher or equal to the length of the trajectory or lower or equal to the first frame to read. Default is the last frame of the trajectory. |
| Step | step= | int | (Opt.) Step between frame to read. Cannot be lower or equal to 0. Default is 1. |

### Output(s)

| Name | Type | Description|
|---|---|---|
| System | class System | Instance of the system classes containing all the informations on the system as well as the positions and configurations. |

## Examples

### Open a single frame

The following example will load the *DPPC* molecules found in the files *test.gro* and *test.tpr* into the
instance of the System class *loaded_system*.

```python
import mllpa

loaded_system = mllpa.openSystem('test.gro', 'test.tpr', 'DPPC')
```

### Select the neighbor rank

The following example will load the *DPPC* molecules found in the files *test.gro* and *test.tpr* into the
instance of the System class *loaded_system*, but will use a neighbor rank of 4 instead of 6
for the generation of the intra-molecular distances.

```python
loaded_system = mllpa.openSystem('test.gro', 'test.tpr', 'DPPC', rank=4)
```

### Open a whole trajectory

The following example will load the *DPPC* molecules found in all the frames the files *test.gro*, *test.tpr* and *test.xtc* into the
instance of the System class *loaded_system*.

```python
loaded_system = mllpa.openSystem('test.gro', 'test.tpr', 'DPPC', trajectory_file='test.xtc')
```

### Open a selection of frames in the trajectory

The following example will load the *DPPC* molecules found in the files *test.gro*, *test.tpr* and *test.xtc* into the
instance of the System class *loaded_system*, but will only read the frames from 100 to 500, skipping every 10 frames.

```python
loaded_system = mllpa.openSystem('test.gro', 'test.tpr', 'DPPC', trajectory_file='test.xtc', begin = 100, end = 500, step=10)
```

## Related tutorials

The following tutorial(s) detail further the use of the *openSystem()* function:

* [Load from simulation files](/mllpa/documentation/tutorials/loading-files/1-simulation-files/)
