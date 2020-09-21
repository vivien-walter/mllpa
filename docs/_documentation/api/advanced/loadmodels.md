---
title: "loadModels()"
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

loadModels() is a function used to open a .lpm model file and load the models from it.
The trained models are returned in a dictionary, as well as the training parameters.

## Argument, keywords and outputs

### Input(s) / Argument(s)

| Name | Flag | Type | Description |
|---|---|---|---|
| Model file | | str | Relative path to the model file to load and read. |

### Output(s)

| Name | Type | Description |
|---|---|---|
| Models | dict | Scikit-learn models trained on the input systems for molecule classification. |
| Training Parameters | dict | Parameters used for the model training. |

## Examples

### Load the model from a file

The following example will open the file *test_model.lpm* and return the trained models defined inside
it into the model dictionary *models_dict* as well as the training parameters *training_params*.

```python
import mllpa

models_dict, training_params = mllpa.loadModels('test_model.lpm')
```
