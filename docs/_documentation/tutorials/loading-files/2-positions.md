---
title: "Load from position array"
section: "tutorials/loading-files"
path: ""
category:
  - tutorial
tags:
  - file access
  - system
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-tutorials"
---

In certain cases, it could be desirable to load directly the positions and configurations not from
simulation files but **from position arrays**, as supported by [NumPy](https://numpy.org). We describe in this
tutorial how to proceed.

Please be aware that loading a system from a position array can be a complicated and tedious operation.
Loading from simulation files should always be preferred when possible.
{: .notice--warning}

## Load the position array

### Prepare the required material

ML-LPA always need a small **collection of information** on the simulation in order to be loaded.

* The **position array**, containing the positions of all the particles of the desired molecule types in all the frames of the simulation.
The position array, obviously generated using the NumPy scientific library, should have the following dimensions:

    ```(# frames, # molecules, # atom per molecules, # dimensions)```

    The expected number of dimensions is 3, since the simulation boxes are always defined in a Cartesian system of coordinates.
    {: .notice--info}

    For example, a 10 frames simulation box with 26 DPPC molecules made of 130 atoms each should have an array of dimension ```(10, 26, 130, 3)```.
    {: .notice--info}

    The position array can only correspond to one single molecule type. See below for more details.
    {: .notice--warning}

* The name of the **molecule type** that you is being loaded. The name of the molecule type should match exactly the **name defined in the simulation**.
More information can be found on [this link](/documentation/tutorials/loading-files/1-simulation-files/#molecule-type-selection).

* A **dictionary containing all the information** on the molecule type. The dictionary includes critical information such as the names, ids and masses of all the atoms, but also
all the bonds between in the molecule. Creating the dictionary by oneself can be quite tough (check this link to see the expected format), so it is advised to use instead
the function *getMolInfos()*

    The function *getMolInfos()* reads directly a **structure file**. Check [the following link](/documentation/tutorials/loading-files/1-simulation-files/#types-of-file) for more information on the required file format.

    ```python
    import mllpa

    mol_infos = mllpa.getMolInfos('test.tpr', 'DPPC')
    ```

    In this example, the structure file is called *test.tpr*. The molecule loaded is *DPPC*.
    {: .notice--info}

* The **size** of the simulation box at each frame of the simulation. Similarly to the position array, dimensions should be provided in a NumPy array.
The required dimensions for this array are

    ```(# frames, # dimensions)```

    For example, a 10 frames should have an array of dimension ```(10, 3)```.
    {: .notice--info}

All these details are strictly required and ML-LPA cannot work without them.
{: .notice--warning}

### Run the function

Once all the required information have been collected, they can be loaded in ML-LPA using the
function *systemFromPositions()*.

```python
import mllpa

loaded_system = mllpa.systemFromPositions(position_array, 'DPPC', mol_infos, boxes)
```

All the collected information have been stored in the variable *loaded_system* as
an instance of the **System** class. More information on the System class are given in the [related tutorial]() and in the [API]().

In this example, all arguments provided are given in the same order than [described above](/documentation/tutorials/loading-files/2-positions/#prepare-the-required-material).
{: .notice--info}

*systemFromPositions()* can also takes some optional keyword-arguments.
You can find the description of all the keyword-arguments in the [API]().

## What is next?

* Now that you know how to load a system, you can either use it [prepare and train a model]() for
    machine learning analysis, or use an existing model to predict the [phases in the sytem]().

* If you want to know more about the System class, you either read the [tutorials on it](), or go
    to its [API]().

## Check the API

The following elements have been used in this tutorial:

* getMolInfos

* systemFromPositions
