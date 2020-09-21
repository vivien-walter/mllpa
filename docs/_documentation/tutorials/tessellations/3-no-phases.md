---
title: "Analysis without phases"
section: "tutorials/tessellations"
path: ""
category:
  - tutorial
tags:
  - voronoi
  - tessellations
  - neighbors
toc: true
toc_sticky: true
sidebar:
  nav: "sidebar-tutorials"
---

While ML-LPA has been ultimately designed and developed to analyse the **lipid phases**,
the tools used to analyse the local environment can be used investigate **other types of environment** than the phases.

## Setting

In this tutorial, we will see how to do that by analysing a mixture of DLPC and DOPC, with some cholesterol inserted in the bilayer.
At room temperature, both molecules are found in the fluid phase, so doing a ML prediction here is supposedly meaningless. Instead,
we want to check if the cholesterol **has a preference for the double bonds of the DOPC molecules or not**.

## Performing the analysis

The codelines of the whole analysis are given below. Comments have been added to help understanding
the process.

{% highlight python linenos %}
import mllpa

# Load the simulation files and extract the three systems of interest
unknown_system_dlpc = mllpa.openSystem('unknown.gro', 'unknown.tpr', 'DLPC')
unknown_system_dopc = mllpa.openSystem('unknown.gro', 'unknown.tpr', 'DOPC')
unknown_system_chol = mllpa.openSystem('unknown.gro', 'unknown.tpr', 'CHL1')

# Assign manually the label of the molecules
unknown_system_dlpc.setPhases("saturated")
unknown_system_dopc.setPhases("unsaturated")
unknown_system_chol.setPhases("cholesterol")

# Do the tessellation of the bilayer in 3D - we exclude the cholesterol from the ghost generation
unknown_tessellation = mllpa.doVoro([unknown_system_dlpc, unknown_system_dopc, unknown_system_chol], geometry='bilayer_3d', exclude_ghost=[2])
{% endhighlight %}

All the results have been saved in the instance of the Tessellation class named *unknown_tessellation* here.
More details can be found in a [previous tutorial](/mllpa/documentation/tutorials/tessellations/2-local-environment/).

## What is next?

* Now that the local environment has been mapped, the last step is to
[save all the results](/mllpa/documentation/tutorials/outputs/3-save-voronoi/) in a file.

## Check the API

The following elements have been used in this tutorial:

* [openSystem()](/mllpa/documentation/api/common/opensystem/)

* [setPhases()](/mllpa/documentation/api/common/setphases/)

* [doVoro()](/mllpa/documentation/api/common/dovoro/)
