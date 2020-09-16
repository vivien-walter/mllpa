---
title: "AutoCorrelation Function"
language: "java"
slug: "1-acf"
navslug: "acf"
github-enable: true
github-link: "https://github.com/vivien-walter/autocorrelation"
version: 1.0
release: 2017
java-type: "ImageJ"
support: false
excerpt_separator: <!--more-->
tagline: "Measure the space and time autocorrelation on image sequences"
header:
  overlay_image: /assets/images/header-software.jpg
  caption: "Source: Codelines of MLLPA"
toc: true
toc_sticky: true
---

<img src="https://img.shields.io/badge/version-{{ page.version }}-f39f37">
<img src="https://img.shields.io/badge/release-{{ page.release }}-0377fc">
<img src="https://img.shields.io/badge/type-{{ page.java-type }}-3b9c46">
<img src="https://img.shields.io/badge/support-{{ page.support }}-8c8c8c">

The AutoCorrelation function (ACF) is a **plugin** made for **ImageJ** which enable
the user to perform autocorrelation calculations in **both space and time** on an
image or a sequence of images. The plugin returns the *characteristic time and distance*
of the images.

<!--more-->

## Description

The ACF plugin reads an **image or sequence of images** and uses the pixel values to
measure the **characteristic autocorrelation times and distances**.

<center><img src="{{ site.baseurl }}/assets/images/softwares/java_acf.png" width='500' height='500'/></center>
<center><sub>Interface of the ACF plugin, with the typical result obtained on an analysis.</sub></center>
<br>

These characteristic times and distances can be seen as the *average period or distances at which one pixel value will be repeated*.
They can be used to calculate the typical frequency of a fluctuation or the size of domains on an image.

ACF can also perform the measurement of the autocorrelation in time after doing the **Fourier transform** of the image.
By doing so, the different ranges of spatial frequencies are analysed separately to extract their
period of oscillation in time.

## Algorithms

### Space correlation

The correlation in space, which is an 2-D ACF, can be calculated via **two different algorithms**:

* A fast calculation can be made by computing the **FFT** of the image first. The **Wiener-Khinchin theorem**
indeed specify that the autocorrelation is simply given by the [Fourier transform of the absolute square of the signal](https://mathworld.wolfram.com/Wiener-KhinchinTheorem.html).
Unfortunately, the FFT in ImageJ can only be made on images with a size N = 2^k, which means that images
with a different size will need to be resized first. It also raises problem at the edge of the region
of interest where the signal stops brutally.
* The second method to calculate the ACF is to use the rough definition and **multiply each pixel value Ixy with all the other pixel values Ix'y'**,
such as the distance xy to x'y' is equal to a given radius r. With this methods, there is no issue on the
edge of the image but the calculation is relatively slow.

### Time correlation

The time correlation, which is a 1-D ACF, is simply done by **multiplying each pixel value Ixy(t) with all the other pixel values Ixy(t+t')**.

## Download

The whole plugin is free to download. Use the link below to start the download (10MB). The source code can also be obtained from
its GitHub page.

<a href="https://mega.nz/file/DN9DHBRD#EQbYkdIygn4P1uIDy714eoyWxP8NJOE9ajYXwoW7HEU" class="btn btn--success"><b>DOWNLOAD</b></a>
<a href="{{ page.github-link }}" class="btn btn--info"><b>GitHub</b></a>

<sub>*Please remember that full support is not provided for this software. You are still free to contact me if you have specific questions on the code, but I cannot guarantee that I will be able to help you.*</sub>
