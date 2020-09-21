---
title: "readModelFile()"
section: "api/advanced"
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

readModelFile() is a function used to open a .lpm model file and extract its content. The content will be returned in
variables, but can also be output in the Terminal.

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Model file | | str | Relative path to the model file to load and read. |
| Training sets | train_sets= | bool | (Opt.) Load the training sets (arrays) from the file too. Default is False. |
| Display | display= | bool | (Opt.) Load the training sets (arrays) from the file too. Default is False. |

### Output(s)

| Name | Type | Description |
|---|---|---|
| Metadata | dict | Metadata used and collected during the training. |
| Coordinates | np.ndarray | (Opt.) Array of the coordinates of the atoms of the molecules. Dimension(s) are in (n_frames, n_molecules, n_atoms_per_molecule, 2). Is only returned if *train_sets=* is set to True. |
| Distances | np.ndarray | (Opt.) Array of the distances of the atoms of the molecules. Dimension(s) are in (n_frames, n_molecules, n_distances). Is only returned if *train_sets=* is set to True. |
| Phases | np.ndarray | (Opt.) Array of all the molecule phases labeled in the system. Dimension(s) are in (n_frames, n_molecules). Is only returned if *train_sets=* is set to True. |

## Examples

### Extract the metadata of a file

The following example will open the file *test_model.lpm* and return the metadata defined inside
it into the dictionary *metadata_dict*.

```python
import mllpa

metadata_dict = mllpa.readModelFile('test_model.lpm')
```

### Extract the metadata and training sets from a file

The following example will open the file *test_model.lpm* and return the metadata defined inside
it into the dictionary *metadata_dict*, as well as the *coordinates*, *distances* and *phases* array used to train the model.

```python
metadata_dict, coordinates, distances, phases = mllpa.readModelFile('test_model.lpm', train_sets=True)
```

### Extract and display the metadata from a file

The following example will open the file *test_model.lpm* and display the metadata
in the Terminal.

```python
mllpa.readModelFile('test_model.lpm', display=True)
```

## Related tutorials

The following tutorial(s) detail further the use of the *readModelFile()* function:

* [The .lpm model file](/mllpa/documentation/tutorials/outputs/1-model-file/)
