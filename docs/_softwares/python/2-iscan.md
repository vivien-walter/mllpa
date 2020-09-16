---
title: "iSCAN"
language: "python"
slug: "2-iscan"
navslug: "iscan"
github-enable: true
github-link: "https://github.com/vivien-walter/iscan"
version: beta
release: 2019
python-version: 3
support: true
excerpt_separator: <!--more-->
tagline: "Image processing for iSCAT microscopy"
header:
  overlay_image: /assets/images/header-software.jpg
  caption: "Source: Codelines of MLLPA"
toc: true
toc_sticky: true
---

<img src="https://img.shields.io/badge/version-{{ page.version }}-f39f37">
<img src="https://img.shields.io/badge/release-{{ page.release }}-0377fc">
<img src="https://img.shields.io/badge/python-{{ page.python-version }}-3b9c46">
<img src="https://img.shields.io/badge/support-{{ page.support }}-8c8c8c">

iSCAN is a Python software running with a GUI that is used to **analyse the images and sequences collected**
with an interferometric scattering (**iSCAT**) microscope. It can be used to calculate the **contrast** of
the objects imaged and **track particles** diffusing in the image.

<!--more-->

<center><img src="{{ site.baseurl }}/assets/images/softwares/python-iscan-logo.png" width='200' height='200'/></center>
<center><sub>Logo of iSCAN.</sub></center>

## Presentation

iSCAN is a complete **Python 3 software** - no terminal lines required - used to analyse images
collected in **interferometric scattering (iSCAT) microscopy**. The graphic user interface (GUI) of iSCAN is powered by **PyQt5**.

<center><img src="{{ site.baseurl }}/assets/images/softwares/python-iscan-interface.png" width='600' height='600'/></center>
<center><sub>Main interface of iSCAN during a contrast analysis.</sub></center>
<br>

The software has two main functions:
* Measure the intensity of the signals found in the image and calculate the **contrast of the signal**.
* **Track particles** diffusing in the image and calculate their diffusitivity.

The different menus found in iSCAN also allows the user to **correct** the image or
run some **statistical measurements** on the data collected.

## Installation

The **documentation** on how to install and launch the software can be found on the related [GitHub page](https://github.com/vivien-walter/iscan).
