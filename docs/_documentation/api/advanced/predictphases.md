---
title: "predictPhases()"
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

predictPhases() is a function that reads the input dataset and makes prediction on the molecule states based on a pre-trained Machine Learning model.
It is similar to the *getPhases()* function, however it uses coordinates and distances array instead of the instance of the
System class as input.

The coordinates and distances arrays can be obtained using respectively the functions [getCoordinates()](/mllpa/documentation/api/advanced/getcoordinates/)
and [getDistances()](/mllpa/documentation/api/advanced/getdistances/).
The models can be trained using the function [generateModel()](/mllpa/documentation/api/common/generatemodel/).

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Coordinates | | np.ndarray | Array of the coordinates of the atoms of the molecules, merged between all systems and all frames. Dimension(s) should be in (N frames \* N molecules, 2 \* N atoms per molecule). |
| Distances | | np.ndarray | Array of the distances of the atoms of the molecules, merged between all systems and all frames. Dimension(s) should be in (N frames \* N molecules, N distances). |
| Models | | str or dict of models | Path to the model file to load or dictionary of the Scikit-Learn models to use to predict the states of the molecules. |

### Output(s)

| Name | Type | Description |
|---|---|---|
| Phases | np.ndarray | Array of all the molecule phases predicted in the system. Dimension(s) are in (N frames, N molecules). |

## Examples

### Predict the phases from a file

The following example will analyse the coordinates array *coordinates_array* and the distances array *distances_array*
using the models pre-trained in the file *new_model.lpm* and return the phases of the molecules in
the variable *phase_array*.

```python
import mllpa

phase_array = mllpa.predictPhases(coordinates_array, distances_array, "new_model.lpm")
```

### Predict the phases from a model dictionary

The following example will analyse the coordinates array *coordinates_array* and the distances array *distances_array*
using the models pre-trained in the variable *models* and return the phases of the molecules in
the variable *phase_array*.

```python
phase_array = mllpa.predictPhases(coordinates_array, distances_array, models)
```
