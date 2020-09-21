---
title: "setStates()"
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

setStates() is a function used to assign manually the states of the molecules from the system.

The function can take as input either the name of the phase, or an array of names of dimension ```(# Frames, # Molecules)```; it will both update the input system
and output an array of all the states.

Alternatively, the method *.setStates()* from the [System class]() can be used for the exact same purpose.

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| System | | class System | Instance of the system classes containing all the informations on the system as well as the positions and configurations. |
| States | | str or np.ndarray | States to assign manually to the molecules. |

### Output(s)

| Name | Type | Description |
|---|---|---|
| States | np.ndarray | Array of all the molecule states predicted in the system. Dimension(s) are in (N frames, N molecules). |

## Examples

### Assigning a single phase

The following example will assign the phase name *fluid* to all molecules of *system_A*,
an instance of the System class. The output will be stored in a variable named *phase_array* in
addition to the attributes of the instance.

```python
import mllpa

phase_array = mllpa.setStates(system_A, "fluid")
```

### Assigning a phase array

The following example will assign the array of phases *phase_array* to *system_A*,
an instance of the System class. The output will only be stored in the instance of the System class.

```python
mllpa.setStates(system_A, phase_array)
```

### Using the method instead of the function

The following example will assign the phase name *fluid* to all molecules of *system_A*,
an instance of the System class, but will call the method of the instance instead of the function.
The output will be stored directly in the instance of the System class.

```python
system_A.setStates("fluid")
```

## Related tutorials

The following tutorial(s) detail further the use of the *setStates()* function through the *.setStates()* method of
the system class:

* [Setting phases manually](/mllpa/documentation/tutorials/phase-prediction/4-set-phases/)

* [Methods of the System class](/mllpa/documentation/tutorials/system-class/2-methods/)

* [Analysis without phases](/mllpa/documentation/tutorials/tessellations/3-no-phases/)
