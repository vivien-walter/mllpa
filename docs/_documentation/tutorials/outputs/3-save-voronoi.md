---
title: "Save the Tessellation class"
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

Similarly to the instances of the System class, the **instances of the Tessellation class**
can be stored in a file, and saved in **multiple formats**. This tutorial develops how
this should be done.

All the file formats will generate files will similar contents to the ones saved from
an instance of the System class. For more information, check the [related tutorial](/mllpa/documentation/tutorials/outputs/2-save-system/#pick-the-file-format).

## Save the instance

Once your systems are ready to be saved and once you have selected your desired output format, you
can save the instances of the Tessellation class using the function *saveVoro()*.

```python
import mllpa

mllpa.saveVoro(voronoi, file_path="processed_system.h5")
```

ML-LPA automatically detect the extension given in the *file_path=* keyword-argument to determine
the format to use. If no extension is found, ML-LPA will automatically use the **default .csv format**. The default format
can be selected by using the keyword-argument *format=*.

ML-LPA can also be set to generate automatically the file name. This is done by not including the *file_path=* keyword argument.
In this case, the name generated will be the date and time of the generation, in the format *YYMMDD_HHMMSS*.

```python
mllpa.saveVoro(voronoi, format=".xml")
```

## Check the API

The following elements have been used in this tutorial:

* [saveVoro()](/mllpa/documentation/api/common/savevoro/)
