---
title: "About ML-LPA"
permalink: /about-mllpa/
author_profile: false
---

## Contributor(s)

ML-LPA have been designed and is maintained by the following persons:

{% for item in site.authors %}
* {{ item.name }}{% if item.orcid != "none" %}<a href="{{ item.orcid }}">![ORCID](/mllpa/assets/images/orcid_logo.png)</a>{% endif %}, *{{ item.affiliation }}*{% if item.website != "none" %} --- [Website]({{ item.website }}){% endif %}
{% endfor %}

## Cite us

You can cite ML-LPA by citing the following article

> Walter Vivien, Ruscher Celine, Benzerara Olivier and Thalmann Fabrice, MLLPA: A Machine Learning‐assisted Python module to study phase‐specific events in lipid membranes,
J. Comp. Chem. (2021)

Moreover, the authors kindly ask you to cite their initial work in which the method was initially published

> Walter Vivien, Ruscher Celine, Benzerara Olivier, Marques Carlos M and Thalmann Fabrice, A machine learning study of the two states model for lipid bilayer phase transitions,
Phys. Chem. Chem. Phys. (2020), **22**, 19147-19154

## Reference(s)

The following articles are using ML-LPA:

{% assign sorted = site.references | sort: 'year' | reverse %}
{% for item in sorted %}
* {{ item.authors }}, *{{ item.title }}*, (**{{ item.year }}**), {{ item.reference }}
    DOI: [{{ item.doi }}]({{ item.doi-link }})
{% endfor %}
