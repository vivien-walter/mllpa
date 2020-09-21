---
title: "Lipid phase prediction"
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

Once the models have been generated through ML-LPA, they can be used, either from the **.lpm file**
or from the **variable**, to predict the phase of a simulation with an unknown composition. This tutorial
shows how to proceed.

## Predict phases

### From an *.lpm file

To predict the lipid phases in a simulation, we need to first load the simulation files in an instance of the System class.
Then, we can use the class method *.getPhases()* to run the prediction. This method only takes as an argument the
**path to the .lpm file**.

```python
import mllpa

# Load the unknown system
unknown_system = mllpa.openSystem('unknown.gro', 'unknown.tpr', 'DPPC')

# Predict the phases
unknown_system.getPhases("new_model.lpm")
```

In this example, we call a model file named *new_model.lpm* which have been generated
in a [previous step](/mllpa/documentation/tutorials/phase-prediction/1-training/#generate-the-model-files).
{: .notice--info}

Since the models should be specific to the type of simulation run (*e.g.* temperature range, lipid mixture,
  simulation parameters), **we do not provide model files** on this website and we recommend you to generate your own
  model files.
{: .notice--warning}

ML-LPA will then process all the lipids in the system **and assign each of them a phase**
based on their configurations. The results can be accessed through the *.phases* attribute of
the instance of the System class:

```python
lipid_phases = unknown_system.phases
```

This will output a NumPy string array with the dimension ```(# frames, # molecules)```.

### From a variable

It is possible to use directly a **model variable** generated using the function *generateModel()*.
To do so, just replace the argument in the *.getPhases()* method by the variable itself.

```python
unknown_system.getPhases(models)
```

In this example, we call a model variable named *models* which have been generated
in a [previous step](/mllpa/documentation/tutorials/phase-prediction/1-training/#extract-directly-the-models-in-variables).
{: .notice--info}

## Machine Learning algorithms

In order to predict the lipid phases with the highest accuracy, ML-LPA relies on a
2-steps prediction system:

* In the first step, the 2 types of data collected from the simulation files, *atom coordinates*
and *intra-molecular distances*, are fed into 3 different ML algorithms defined in **scikit-learn**.
The result is a total of 4 models looking at the data and making their independent predictions.

* In the second step, the *independent predictions* collected in the first step are analysed
by a **classification tree algorithm**, also defined in scikit-learn, that compares the predictions
to output the most accurate prediction possible.

### First predictions

The four models used to analyse the input data are:

* [Support Vector Machine](https://scikit-learn.org/stable/modules/svm.html#support-vector-machines), trained on coordinates.

* Support Vector Machine again, trained this time on distances.

* [K-Nearest Neighbors](https://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbors-classification), trained on coordinates.

* [Gaussian Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html#gaussian-naive-bayes), trained on distances.

The scores of each of the model, total and per phase, are all stored in the .lpm model files.

### Second and final prediction

The predictions of the 4 models above are classified using the [Classification and Regression Trees](https://scikit-learn.org/stable/modules/tree.html#classification) algorithm.
The scores of this model, total and per phase, is also stored in the .lpm model files.
However, the CART model defined by scikit-learn can also **output the classification tree determined through the training**. This can be done using
the typical following command.

In this example, we will need to import the Matplotlib library to plot the data.

{% highlight python linenos %}
import mllpa
import matplotlib.pyplot as plt
from sklearn import tree

# Load the simulations files to be trained on
gel_system = mllpa.openSystem('gel.gro', 'gel.tpr', 'DPPC')
fluid_system = mllpa.openSystem('fluid.gro', 'fluid.tpr', 'DPPC')

# Train the model on the systems - do not save the model files
models = mllpa.generateModel([gel_system, fluid_system], phases=['gel', 'fluid'], save_model=False)

# Extract the CART model from the dictionary
cart_model = models['ClassificationTree']

# Display the classification tree
tree.plot_tree(cart_model)
plt.show()
{% endhighlight %}

The classification tree should be directly displayed when the script is run.

## What is next?

* Now you know how the phases of your unknown systems can been predicted, you can
start to analyse the [local environment of the lipids](/mllpa/documentation/tutorials/tessellations/1-voronoi/).

* You can also [store the results](/mllpa/documentation/tutorials/outputs/2-save-system/) in a file.

## Check the API

The following elements have been used in this tutorial:

* [System class](/mllpa/documentation/api/classes/system/)
