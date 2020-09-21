---
title: "Setting phases manually"
section: "tutorials/phase-prediction"
path: ""
category:
  - tutorial
tags:
  - machine learning
  - system
  - prediction
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-tutorials"
---

Depending on the situation, some *lipids* - or other *membrane molecules* - might not undergo a phase
transition during the simulations. For instance, the *dioleoyl-glycerophosphocholine* (DOPC) has a transition
temperature of -17C, so it more than likely that it will remain in the fluid phase for all simulations run
in the water (> 0C). The problem of these molecules is that ML-LPA **cannot be trained** to predict their phases, and because of that
[analysis of the local environment](/mllpa/documentation/#d---local-environment-analysis) cannot be processed.

To avoid these problem, **phases can be assigned manually** in ML-LPA to an instance of the System class.

## Manual phase assignment

### Single assignment

To assign the lipid phases in a simulation, we need to first load the simulation files in an instance of the System class.
Then, we can use the class method *.setPhases()* to assign the phases. This method only takes as an argument the string with
the name of the phase.

```python
import mllpa

# Load the unknown system
unknown_system = mllpa.openSystem('unknown.gro', 'unknown.tpr', 'DOPC')

# Assign the phases
unknown_system.setPhases("fluid")
```

ML-LPA will then process all the lipids in the system and assign to each of them **the given phase**.
The final result can be accessed through the *.states* attribute of the instance of the System class
[as shown previously](/mllpa/documentation/tutorials/phase-prediction/4-ml-prediction/#from-an-lpm-file).

### Molecule-by-molecule assignment

The method *.setPhases()* can also be used to **assign a whole NumPy string array** to the molecules
stored in the instance.

```python
unknown_system.setPhases(lipid_phases)
```

In this example, we call a NumPy array named *lipid_phases* which have been generated
outside of the example script.
{: .notice--info}

The NumPy string array used as input should have the dimension ```(# frames, # molecules)```.

## What is next?

* Now you know how the phases of your unknown systems can been predicted, you can
start to analyse the [local environment of the lipids](/mllpa/documentation/tutorials/tessellations/1-voronoi/).

* You can also [store the results](/mllpa/documentation/tutorials/outputs/2-save-system/) in a file.

## Check the API

The following elements have been used in this tutorial:

* [System class](/mllpa/documentation/api/classes/system/)
