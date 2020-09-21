---
title: "readNeighbors()"
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

readNeighbors() is a function used to read the states (as predicted through Machine Learning)
of the neighbors of each molecule to list the state compositions. The neighbors
list has to be collected first using the [doVoro()](/mllpa/documentation/api/common/dovoro/) function.

Unless specified explicitely, this function should be automatically started by *doVoro()*.

The function will both update the input tessellation and output an array of the neighbor composition as well as a list
of the phase names.

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Representation | | class Tessellation | Instance of the class Tessellation including the representation on the system and its Voronoi tessellation. |

### Output(s)

| Name | Type | Description |
|---|---|---|
| Neighbors Phases | np.ndarray | Array of the phases of the neighbors of each molecule. Dimension(s) are in (N frames, N molecules, N phases). |
| Phases List | np.ndarray | Array listing the phases analysed and the order used for the neighbors phases array. |

## Examples

### Read the local environment and return the composition

The following example will read the local environment in the instance of the Tessellation class named *voronoi*,
and both return the results in the variables *phase_array* and *phase_names*; but also store them in the same instance.

```python
import mllpa

phase_array, phase_names = mllpa.readNeighbors(voronoi)
```

### Read the local environment but don't return anything

The following example will read the local environment in the instance of the Tessellation class named *voronoi*,
and store the output in the same instance.

```python
mllpa.readNeighbors(voronoi)
```

## Related tutorials

The following tutorial(s) detail further the use of the *readNeighbors()* function:

* [Map the environment](/mllpa/documentation/tutorials/tessellations/2-local-environment/)

* [Analysis without phases](/mllpa/documentation/tutorials/tessellations/3-no-phases/)
