---
title: "Machine Learning algorithms training"
section: "tutorials/phase-prediction"
path: ""
category:
  - tutorial
tags:
  - machine learning
  - system
  - training
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-tutorials"
---

Once the simulation files have been extracted and their information stored in **instances of the System class**,
ML-LPA is ready to be trained to identify the lipid phases.

## Requirements for the systems

ML-LPA can be trained to predict **multiple phases** at the same time (# phases >= 2). For each of the phases
being trained on, one instance of the System class is required.

Furthermore, to avoid issues and bias brought by **over-representation of one phase** as compared to the other, several
requirements have to be met:

* The **molecule type should be the same** in all instances.

* The **number of atoms per molecule should be the same** in all instances.

* The **neighbour rank**, and therefore the **number of distances per molecule**, **should be the same** in all instances.

    The neighbour rank can be edited anytime using the System class method *.getDistances()*. Please read the
    [corresponding section](/mllpa/documentation/tutorials/system-class/2-methods/#intra-molecular-atomic-distances) for more details.
    {: .notice--info}

* The **total number of molecules should be large enough** to train on a significant population. We recommend to use
at least 500 molecules per instances for the training.

    If the instances does not have enough molecules per frame, ML-LPA should be trained on more than one frame.
    For example, if the instaces have 50 molecules, the training should be done on 10 frames at least.
    {: .notice--info}

    The number of frames can only be selected while loading the molecules from the simulation files with the
    *openSystem()* function. For more details, see the [API](/mllpa/documentation/api/common/opensystem/).
    {: .notice--info}

* The total number of molecules being used for the training **should be the same in all instances**.

    If the instances have different number of molecules per frame, the number of frames used for the training
    should be adjusted so ```# frames x # molecules per frame``` is constant. For example, if the instance A
    has 30 molecules and the instance B 90 molecules, the instance A should be trained on 3 times more frames
    than B.
    {: .notice--info}

## Train the models

ML-LPA relies on a **2-steps** prediction system involving a total of **4 different ML algorithms** defined
in scikit-learn. More detailed information on the prediction system and the ML algorithms used can be found
in a [later tutorial](/mllpa/documentation/tutorials/phase-prediction/3-ml-prediction/).

### Generate the model files

Once all the requirements have been met, ML-LPA is ready to be trained. This is done using the function
*generateModel()*. The inputs of the function are two lists: (1) one list containing all **the systems with the different phases**
to be trained on, and (2) one list with their **respective labels**.

```python
import mllpa

# We import one set of simulation files per phase
gel_system = mllpa.openSystem('gel.gro', 'gel.tpr', 'DPPC')
fluid_system = mllpa.openSystem('fluid.gro', 'fluid.tpr', 'DPPC')

# Train the models and saved them in a file
mllpa.generateModel([gel_system, fluid_system], phases=['gel', 'fluid'], file_path='new_model.lpm')
```

In this example, the coordinates and structure files of the gel and fluid phases
are respectively called *gel.gro* and *gel.tpr*, and *fluid.gro* and *fluid.tpr*.
We use the *openSystem()* function to load the information from
the simulation files. Check the [related tutorial](/mllpa/documentation/tutorials/loading-files/1-simulation-files/) for more details.
{: .notice--info}

Once the training has been completed, the models are stored in a **.lpm** (<ins>L</ins>ipid <ins>P</ins>hase <ins>M</ins>odel) file at the given location.
This file can be used anytime to predict the phases in a simulation of unknown composition. More details on the
.lpm files are given in the [corresponding tutorial](/mllpa/documentation/tutorials/outputs/1-model-file/).

### Extract directly the models in variables

For many reasons, one can decide to **not save the models in a file**, and just extract them directly in variables to use them
straight. This can be done by disabling the *save_model=* keyword-argument:

```python
models = mllpa.generateModel([gel_system, fluid_system], phases=['gel', 'fluid'], save_model=False)
```

The models are returned in a dictionary of instances of **specific scikit-learn classes**.

You can find the description of all the keyword-arguments of the *generateModel()* function in the [API](/mllpa/documentation/api/common/generatemodel/).

## Assessing reproducibility and scoring

One issue that can arise while training ML models with a set of data is that the size of the dataset will
**never be large enough** to correspond exactly to all the **population of possible configurations** for each phase.
As a consequence, we are bound to train our models on a **sample** that we hope large enough to prevent any training bias.

In order to check whether the sample of **N molecules** is a *good enough representation* of the population, ML-LPA will proceed
by **resampling** the input data and generate **K times** 3 different sub-samples of respective sizes **j N**, **j N** and **(1-j) N**,
where **K** and **j** can be set by the user, and **j** a float between 0 and 0.33.

<center><img src="{{ site.baseurl }}/assets/images/tutorials/training.png" width='500' height='500'/></center>
<center><sub>Flowchart of the logic used to train the ML models</sub></center><br>

The sample of size (1-j)N and one of the samples of size jN will be used to train the 2-steps prediction system, while the
other sample of size jN is used to assess the accuracy of the system and of each algorithm. The final score and reproducibility are
calculated from the **K repetitions of the resampling and training**.

## What is next?

* Now that you know how to generate a model in ML-LPA, the next obvious step would be to
use it to [predict the phases](/mllpa/documentation/tutorials/phase-prediction/3-ml-prediction/) in an unknown system.

* You can also check how to [read the scores in the .lpm files](/mllpa/documentation/tutorials/outputs/1-model-file/)
or [optimise the neighbour rank](/mllpa/documentation/tutorials/phase-prediction/2-rank-optimisation/).

## Check the API

The following elements have been used in this tutorial:

* [generateModel()](/mllpa/documentation/tutorials/phase-prediction/2-model-file/)
