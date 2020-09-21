---
title: "Save the System class"
section: "tutorials/outputs"
path: ""
category:
  - tutorial
tags:
  - file access
  - system
  - output
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-tutorials"
---

Once the phases of the system have been [predicted by ML-LPA](/mllpa/documentation/tutorials/phase-prediction/3-ml-prediction/) -
or [assigned manually](/mllpa/documentation/tutorials/phase-prediction/4-set-phases/) -
it can be essential to store and save the results in a file on your computer.
This tutorial will explain how it can be easily done.

## Pick the file format

When an instance of the System class is saved by ML-LPA, the following data are saved in the file:

* **Name** and **index** of the molecule.

* **Center of mass (COMs)** of the molecule (X, Y, Z).

* The **phase** in which the molecule was found.

Since both COMs and phases arrays are defined over time, they will be concatenated prior saving
in a single array of dimension ```(# Frames, # Molecules, [X, Y, Z, Phase])```.

ML-LPA can save the file even if the phases are not included in the system. It will just omit them
from the output file.
{: .notice--warning}

To be able to save these data, the user will have to select the format to use.

### Choice of file format

ML-LPA is capable of storing the instance of System class in different file formats:

* **Comma-separated values (.csv) files**, to be easily opened in spreadsheet softwares.

* **Extensible markup language (.xml) files**, to keep a hierarchical structure in the data saved while saving in a text file.

* **Hierarchical data format 5 (.h5) files**, to directly save in a binary file and keep the data formats.

The choice of the output format is entirely up to the user and to what is convenient for them.
By default, the format used by ML-LPA is the .csv file.
{: .notice--info}

### Details on the formats

The **same data** are being stored in the different format. Only the structure inside the file changes.

#### .csv files

A .csv file can only take as an input **2-D arrays**. This means that the COMs + phases array, which is a **3-D array**,
cannot be saved directly in the file. The 3-D array will be flattened in a 2-D one, by saving each frames one after the other.
The name and IDs of the molecules will also be added to the resulting array.

The typical array of N molecules saved in a .csv file is based on the following table:

| Row index | Name | Frame | Molecule ID | COM x | COM y | COM z | Phase |
|---|---|---|---|---|---|---|---|
| 0 | Mol. A | 0 | 0 | x position | y position | z position | phase |
| 1 | Mol. A | 0 | 1 | x position | y position | z position | phase |
| 2 | Mol. B | 0 | 2 | x position | y position | z position | phase |
| ... | ... | ... | ... | ... | ... | ... | ... |
| N | Mol. C | 0 | N | x position | y position | z position | phase |
| N+1 | Mol. A | 1 | 0 | x position | y position | z position | phase |
| N+2 | Mol. A | 1 | 1 | x position | y position | z position | phase |
| N+3 | Mol. B | 1 | 2 | x position | y position | z position | phase |
| ... | ... | ... | ... | ... | ... | ... | ... |
| 2N | Mol. C | 1 | N | x position | y position | z position | phase |
| 2N+1 | Mol. A | 2 | 0 | x position | y position | z position | phase |
| ... | ... | ... | ... | ... | ... | ... | ... |

#### .xml files

In an .xml file, the representation of **each frame** of the simulation **is saved in a different branch** of the .xml tree.
Each frame branch also carries the **dimension of the simulation box**.
Inside the frame branch, **each molecule is defined in its own sub-branch**. The sub-branch of the molecule will contain:
(i) its ID, (ii) its name, (iii) its phase and (iv) the X, Y and Z coordinates of its COM.

The typical .xml tree will look like

```bash
├── frame 0, box x, box y, box z
│   ├── 0, Mol. A, phase, x, y, z
│   ├── 1, Mol. B, phase, x, y, z
│   ...
│   └── N, Mol. C, phase, x, y, z
├── frame 1, box x, box y, box z
│   ├── 0, Mol. A, phase, x, y, z
│   ├── 1, Mol. B, phase, x, y, z
│   ...
│   └── N, Mol. C, phase, x, y, z
...
```

#### .h5 files

Since the HDF5 format is a hierarchical format close to .xml format, we will typically find the same structure
in this format as well. However, since more informations and different types of data can be stored in a HDF5 file, the informations one
can find inside are more complete than in the .xml file.

First, the ID and names arrays are only **saved once in the file**, and not once per frame, to save some space.

The **COMs** and **arrays** are saved separately in two elements, since they keep their respective dimensions of ```(# Frames, # Molecules, [X,Y,Z])```
and ```(# Frames, # Molecules)```.

The **dimensions of the simulations box** are also saved in another element as an array of dimension ```(# Frames, [X,Y,Z])```

HDF5 (.h5) files can opened with softwares such as HDFView. However, we recommend to use Python
to open the file again and read their content. Please use the scientific library [h5py](https://www.h5py.org) for that purpose.
{: .notice--info}

## Save in a file

Once your systems are ready to be saved and once you have selected your desired output format, you
can save the instances of the System class using the function *saveSystems()*.

```python
import mllpa

mllpa.saveSystems(unknown_system, file_path="processed_system.h5")
```

ML-LPA automatically detect the extension given in the *file_path=* keyword-argument to determine
the format to use. If no extension is found, ML-LPA will automatically use the **default .csv format**. The default format
can be selected by using the keyword-argument *format=*.

ML-LPA can also be set to generate automatically the file name. This is done by not including the *file_path=* keyword argument.
In this case, the name generated will be the date and time of the generation, in the format *YYMMDD_HHMMSS*.

```python
mllpa.saveSystems(unknown_system, format=".xml")
```

## What is next?

* Now that you know how to save the instances of the System class, you can check how to save the instance
of the [Tessellation class](/mllpa/documentation/tutorials/outputs/3-save-voronoi/).

## Check the API

The following elements have been used in this tutorial:

* [saveSystems()](/mllpa/documentation/api/common/savesystems/)
