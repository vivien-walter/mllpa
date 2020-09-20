---
title: "getMolInfos()"
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

getMolInfos() is a function used to extract all the relevant information on the molecule type selected
from a structure file. The information are returned as a dictionary.

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Structure file | | str | Relative path to the structure file of the system (e.g. .tpr file). |
| Type | | str | Name of the molecule type to extract the information from. The type should be similar as the one listed in getTypes(). |

### Output(s)

| Name | Type | Description |
|---|---|---|
| Molecule Infos | dict | Dictionary containing all the informations on the molecule type. |

## Examples

### Retrieve the information on a specific molecule type

The following example will open a structure file, *test.tpr*, and return the information
on the molecule type *DPPC* in the variable *mol_infos*.

```python
import mllpa

mol_infos = mllpa.getMolInfos('test.tpr', 'DPPC')
```

## Related tutorials

The following tutorial(s) detail further the use of the *getMolInfos()* function:

* [Load from position array](/mllpa/documentation/tutorials/loading-files/2-positions/)
