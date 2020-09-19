---
title: "The .lpm model file"
section: "tutorials/outputs"
path: ""
category:
  - tutorial
tags:
  - machine learning
  - system
  - output
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-tutorials"
---

ML-LPA uses its own file type to store the trained Machine Learning models:
the **.lpm** files (<ins>L</ins>ipid <ins>P</ins>hase <ins>M</ins>odel).
This tutorial explore thoroughly these files.

## The .lpm file format

The **.lpm** are neither text nor binary files: they are in fact **.zip compressed files**
with a custom extension. Inside the archive can be found several text files defining the Machine Learning
models and describing the training scores.

There are multiple reasons to explain the choice of this unusual format:

* Using a non-binary file format **prevents compatibility issues** (*e.g.* different pickles version).

* Compressing the several files in a **single archive file** avoids losing some of the file
by mistake and prevents modifications of the text files by mistake.

* Using a **different file extension** prevents confusion with other archive files.

## Inside the .lpm file

### Opening the .lpm file

The .lpm files can be easily opened and explored. You will first need to **modify the file extension** and
then **open the archive file**. This can be done **manually in the GUI** of your operating system, or within the
Terminal with the **following commands** (in which can renaming in not required).

```sh
> mkdir model_contents
> unzip model_test.lpm -d model_contents
```

In this example, the .lpm file *model_test.lpm* have been created using the function
*generateModel()*. Check the [related tutorial](/mllpa/documentation/tutorials/phase-prediction/1-training/#generate-the-model-files) for more details.
{: .notice--info}


### The training .csv files

The **.lpm archive** contains three data files in the .csv format:

* *model_coordinates.csv*

* *model_distances.csv*

* *model_states.csv*

To avoid any compatibility issue with different scikit-learn versions,
**the instance of the scikit-learn model classes are never directly saved** in the files.
Instead, the training datasets are stored in the file and are used later to re-train the models
on them.

### The metadata .xml file

The **.lpm archive** also contains one data files in the .xml format: the **model_data.xml metadata file**.
In this files are stored several types of information collected during the training:

* The **information on the systems** that have been used to train the models (*e.g.* name of the molecule type,
  number of molecules).

* The **settings** used for the training (*e.g.* neighbour rank, size of the training subsets).

* The **scores obtained during the training**, either the final scores for each phases or the scores for each models used in ML-LPA.

* Other general metadata (*e.g.* ML-LPA and scikit-learn versions, date and time)

## What is next?

* Now that you know how what is inside a .lpm file, you can use it to [predict the phases]() in an unknown system.
