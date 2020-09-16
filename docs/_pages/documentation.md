---
title: "Documentation"
permalink: /documentation/
author_profile: false
sidebar:
  nav: "sidebar-documentation"
---

You can find on this page several **tutorials** to get started with ML-LPA. For detailed
information on all the functions of the software, please read the **API**.

## Tutorials

The tutorials are **step-by-step guides** to illustrate how ML-LPA can and should be used.
The tutorials have been organised in **different chapters** covering the main use of ML-LPA.

### Loading simulation

{% assign tutorials = site.documentation | where:"section", "tutorials/loading-files" %}
{% for item in tutorials %}
  1. [{{ item.title }}]({{ site.baseurl }}/{{ item.collection }}/{{ item.section }}/{{ item.slug }})
{% endfor %}

### The System class

### Predicting phases

## API
