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

We would recommend you to read all the tutorials below to understand exactly how to use
ML-LPA. However, you can refer to the [Quick & Dirty tutorial](/mllpa/documentation/tutorials/quick-and-dirty/) if you want to quickly see how
ML-LPA can be used.
{: .notice--info}

### A - Loading simulation

{% assign tutorials = site.documentation | where:"section", "tutorials/loading-files" %}
{% for item in tutorials %}
  1. [{{ item.title }}]({{ site.baseurl }}/{{ item.collection }}/{{ item.section }}/{{ item.slug }})
{% endfor %}

### B - The System class

If you are only interested in getting ML-LPA to work quickly, we recommend to skip the tutorials on the System class.
{: .notice--info}

{% assign tutorials = site.documentation | where:"section", "tutorials/system-class" %}
{% for item in tutorials %}
  1. [{{ item.title }}]({{ site.baseurl }}/{{ item.collection }}/{{ item.section }}/{{ item.slug }})
{% endfor %}

### C - Predicting phases

{% assign tutorials = site.documentation | where:"section", "tutorials/phase-prediction" %}
{% for item in tutorials %}
  1. [{{ item.title }}]({{ site.baseurl }}/{{ item.collection }}/{{ item.section }}/{{ item.slug }})
{% endfor %}

### D - Local environment analysis

{% assign tutorials = site.documentation | where:"section", "tutorials/tessellations" %}
{% for item in tutorials %}
  1. [{{ item.title }}]({{ site.baseurl }}/{{ item.collection }}/{{ item.section }}/{{ item.slug }})
{% endfor %}

### E - Save the outputs

{% assign tutorials = site.documentation | where:"section", "tutorials/outputs" %}
{% for item in tutorials %}
  1. [{{ item.title }}]({{ site.baseurl }}/{{ item.collection }}/{{ item.section }}/{{ item.slug }})
{% endfor %}

## API Reference

The API reference lists and describes all the **functions** and **classes** implemented in ML-LPA.
Along examples, all arguments, keyword-arguments and outputs are detailed and explained.

### Common functions

{% assign api = site.documentation | where:"section", "api/common" %}
{% for item in api %}
  * [{{ item.title }}]({{ site.baseurl }}/{{ item.collection }}/{{ item.section }}/{{ item.slug }})
{% endfor %}

### Advanced functions

{% assign api = site.documentation | where:"section", "api/advanced" %}
{% for item in api %}
  * [{{ item.title }}]({{ site.baseurl }}/{{ item.collection }}/{{ item.section }}/{{ item.slug }})
{% endfor %}

### Classes

{% assign api = site.documentation | where:"section", "api/classes" %}
{% for item in api %}
  * [{{ item.title }}]({{ site.baseurl }}/{{ item.collection }}/{{ item.section }}/{{ item.slug }})
{% endfor %}
