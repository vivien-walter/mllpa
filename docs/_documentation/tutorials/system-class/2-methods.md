---
title: "Methods of the System class"
section: "tutorials/system-class"
path: ""
category:
  - tutorial
tags:
  - system
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-tutorials"
---

Similarly, to the attributes, the **methods of an instance of the System class** does not bear too much interest
in a standard quick and dirty use of ML-LPA. We describe in this tutorial some of the most useful methods of the class.

If you are only interested in getting ML-LPA to work quickly, we recommend to directly
move to the tutorials on [phase prediction]().
{: .notice--info}

## Re-generate the coordinates and distances

The **coordinates** and **distances** contained in the instance of the class were computed when the
instance was first created. As a result, an update of the **positions** held in the instance will not be
automatically reflected on the coordinates and distances. To compute the arrays again, two methods
can be called.

### Atom coordinates

To re-generate the coordinates of the atom in the **cylindrical system of coordinates**, the
method *.getCoordinates()* can be used.

```python
import mllpa

# We first load a system for our exemple
loaded_system = mllpa.openSystem('test.gro', 'test.tpr', 'DPPC')

# We replace the positions array in the instance of the class with one generated previously
loaded_system.positions = new_position_array

# We finally regenerate the coordinates to the new positions
loaded_system.getCoordinates()
```

In this example, we use the *openSystem()* function to load the information from
the simulation files. Check the [related tutorial](/mllpa/documentation/tutorials/loading-files/1-simulation-files/) for more details.
{: .notice--info}

Please be aware that we have not defined the array *new_position_array* in the example above.
The dimensions of the new array should be exactly the same as the ones of the previous one.
{: .notice--warning}

### Intra-molecular atomic distances

To re-generate the **intra-molecular distances** from the new position array, the
method *.getDistances()* can be used.

```python
loaded_system.getDistances(rank=6)
```

This method can also be used to simply update the neighbour rank used in the computation without
reloading the whole instance from the simulation files. A detailed example is shown in the [dedicated tutorial](/mllpa/documentation/tutorials/phase-prediction/2-rank-optimisation/).

The value of the neighbor rank should be optimised by the user, based on the systems
being used to train the Machine Learning algorithms. The rank equals to 6 here is
an example.
{: .notice--warning}

## What is next?

* Now that you know how to load a system, you can either use it to [prepare and train a model](/mllpa/documentation/tutorials/phase-prediction/1-training/) for
    machine learning analysis, or use an existing model to predict the [phases in the system](/mllpa/documentation/tutorials/phase-prediction/3-ml-prediction/).

## Check the API

The following elements have been used in this tutorial:

* [System class](/mllpa/documentation/api/classes/system/)
