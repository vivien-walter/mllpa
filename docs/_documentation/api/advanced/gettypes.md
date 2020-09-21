---
title: "getTypes()"
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

getTypes() is a function used to extract and return the list of molecule types found in the simulation files.
These types can be used as input for the [openSystem()](/mllpa/documentation/api/common/opensystem/) function.

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Coordinates file | | str | Relative path to the coordinates file of the system (e.g. .gro file). |

### Output(s)

| Name | Type | Description |
|---|---|---|
| Molecule Types | np.ndarray | Array of all the molecule types names found in the system. Dimension(s) are in (N molecule types). |

## Examples

### List the molecules in a file

The following example will open a coordinates file, *test.gro*, and return the list
of the molecule types found in the variable *types_list*.

```python
import mllpa

types_list = mllpa.getTypes('test.gro')
```

## Related tutorials

The following tutorial(s) detail further the use of the *getTypes()* function:

* [Load from simulation files](/mllpa/documentation/tutorials/loading-files/1-simulation-files/)
