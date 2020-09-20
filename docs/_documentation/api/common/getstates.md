---
title: "getStates()"
section: "api/common"
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

getStates() is a function used to predict the states of the molecules from the system by using
a model previously created using the function [generateModel()](/mllpa/documentation/api/common/generatemodel/).

The function can take as input either the path to a model file, or a dictionary of models; it will both update the input system
and output an array of all the states.

Alternatively, the method *.getStates()* from the [System class]() can be used for the exact same purpose.

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| System | | class System | Instance of the system classes containing all the informations on the system as well as the positions and configurations. |
| Models | | str or dict of models | Path to the model file to load or dictionary of the Scikit-Learn models to use to predict the states of the molecules. |

### Output(s)

| Name | Type | Description |
|---|---|---|
| States | np.ndarray | Array of all the molecule states predicted in the system. Dimension(s) are in (N frames, N molecules). |

## Examples

### Prediction with a model file

The following example will use the model file *new_model.lpm* to predict the phase of *system_A*,
an instance of the System class. The output will be stored in a variable named *phase_array* in
addition to the attributes of the instance.

```python
import mllpa

phase_array = mllpa.getStates(system_A, "./new_model.lpm")
```

### Prediction with a model dictionary

The following example will use the models stored in the variable *models* to predict the phase of *system_A*,
an instance of the System class. The output will only be stored in the instance of the System class.

```python
mllpa.getStates(system_A, models)
```

### Using the method instead of the function

The following example will use the model file *new_model.lpm* to predict the phase of *system_A*,
an instance of the System class, but will call the method of the instance instead of the function.
The output will be stored directly in the instance of the System class.

```python
system_A.getStates("./new_model.lpm")
```

## Related tutorials

The following tutorial(s) detail further the use of the *getStates()* function through the *.getStates()* method of
the system class:

* [Lipid phase prediction](/mllpa/documentation/tutorials/phase-prediction/3-ml-prediction/)

* [Methods of the System class](/mllpa/documentation/tutorials/system-class/2-methods/)
