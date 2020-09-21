---
title: "Quick & Dirty tutorial"
section: "tutorials/"
path: ""
category:
  - tutorial
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-tutorials"
---

While it is recommended to read the [whole tutorials](/mllpa/documentation/#tutorials) before getting started with ML-LPA,
we present on this page a quick and dirty example on how ML-LPA can be used to analyse a set of simulation files.

In the following example, we will use two simulations (one at low temperature, *gel*, and one at high temperature, *fluid*) to train
ML-LPA to recognise the phases of DPPC molecules. We will then use the generated models to analyse the unknown phase
composition of a DPPC bilayers which also includes some DOPC and cholesterol (named CHL1) molecules; the latter having no phase transition
in the studied temperature range. Finally the system will be tessellated to analyse the local environment of the molecules in the bilayer.
{: .notice--warning}

## Codelines

Please refer to the **comments in the code** to see the purpose of each function and step.
Sections below describes the different functions used and where to find more information
on them.

{% highlight python linenos %}
import mllpa

## STEP 1 - TRAINING

# Load the simulations files to be trained on
gel_system = mllpa.openSystem('gel.gro', 'gel.tpr', 'DPPC')
fluid_system = mllpa.openSystem('fluid.gro', 'fluid.tpr', 'DPPC')

# Train the models and save them in a variable AND in a file
models = mllpa.generateModel([gel_system, fluid_system], phases=['gel', 'fluid'], save_model=True, file_path='test_dppc.lpm')

## STEP 2 - PREDICTION

# Load the simulation file with the unknown composition in DPPC and with DOPC molecules as well
unknown_system_dppc = mllpa.openSystem('unknown.gro', 'unknown.tpr', 'DPPC')
unknown_system_dopc = mllpa.openSystem('unknown.gro', 'unknown.tpr', 'DOPC')
unknown_system_chol = mllpa.openSystem('unknown.gro', 'unknown.tpr', 'CHL1')

# Predict the phase of the lipids that have been trained on
unknown_system_dppc.getPhases(models)

# Assign a given phase to lipids that does not undergo phase transition
unknown_system_dopc.setPhases("fluid")
unknown_system_chol.setPhases("cholesterol") # We add here a label instead of a phase

## STEP 3 - TESSELLATION

# Do the tessellation and analyse the local environment - but exclude cholesterols from the ghost generation
unknown_tessellation = mllpa.doVoro([unknown_system_dppc, unknown_system_dopc, unknown_system_chol], geometry='bilayer_3d', exclude_ghost=[2], read_neighbors=True)

## STEP 4 - OUTPUT

# Save the file
mllpa.saveVoro(unknown_tessellation, file_path="unknown_tessellation.csv")
{% endhighlight %}

## Details on the example

### Training

In the training part of the codes, two functions are being used:

* [*openSystem()*](/mllpa/documentation/api/common/opensystem/), used to load the simulation files and extract the essential
information for ML-LPA. [More details here](/mllpa/documentation/tutorials/loading-files/1-simulation-files/#load-the-files).

* [*generateModel()*](/mllpa/documentation/api/common/generatemodel/), used to create a set of Machine Learning models from the instances of the
System classes. [More details here](/mllpa/documentation/tutorials/phase-prediction/1-training/#generate-the-model-files).

### Prediction

In the prediction part of the codes, one function and two methods are being used:

* [*openSystem()*](/mllpa/documentation/api/common/opensystem/), used to load the simulation files and extract the essential
information for ML-LPA. [More details here](/mllpa/documentation/tutorials/loading-files/1-simulation-files/#load-the-files).

* [*.getPhases()*](/mllpa/documentation/api/classes/system/), used to predict the phases of the molecules, using an pre-generated model.
[More details here](/mllpa/documentation/tutorials/phase-prediction/4-ml-prediction/#predict-phases).

* [*.setPhases()*](/mllpa/documentation/api/classes/system/), used to assign manually a phase to the molecules.
[More details here](/mllpa/documentation/tutorials/phase-prediction/5-set-phases/#manual-phase-assignment).

### Tessellation

In the tessellation part of the codes, two functions are being used:

* [*doVoro()*](/mllpa/documentation/api/common/dovoro/), used to tessellate the system and read the local environment. [More details here](/mllpa/documentation/tutorials/tessellations/1-voronoi/).

### Output

In the output part of the codes, one function is used:

* [*saveVoro()*](/mllpa/documentation/api/common/savevoro/), used to save the content of an instance of the Tessellation
class. [More details here](/mllpa/documentation/api/common/savevoro/).
