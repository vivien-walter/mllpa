# ML-LPA

Machine Learning-assisted Lipid Phase Analysis

## General informations

Version : alpha

Date : 22/12/2018

Author : Vivien WALTER (walter.vivien@gmail.com)

## Description

ML-LPA is a TUI Python 3 module, developed to predict the thermodynamic phase of individual lipids in a bilayer obtained from molecular dynamics simulation.

**DISCLAIMER: This module is an alpha version released to support the article published in PCCP. A new version, corrected for enhanced user experience, processing efficiency and to work with any lipid type, is currently under development and will published soon (current schedule: August 2020). However, please be aware that the general analysis algorithms will remains identical as the ones used in the alpha version.**

**DISCLAIMER 2: The alpha version is only kept for keeping record of the codes used in the published PCCP article. Alpha version is no longer maintained to focus resources on the development of the version 1.0.**

ML-LPA has two main parts:
- The training sets of scripts, located in the training/ folder
- The analysis sets of scripts, located in the analysis/ folder

Only the analysis sets is using a TUI.

This work has been published in *(put future REF/LINK here)*.

## Installation

### Training

1. Install the required dependencies automatically by installing the Analysis part of the module first
2. Copy the two scripts in the folder 'analysis'
3. See section **How to** for using the scripts

### Analysis

1. Download the folder 'analysis'
2. Open a terminal and go to /analysis
3. Type *python3 setup.py install*

## How to

### Train a model ###

1. Add 3 .gro files for each phase to train in the training folder, naming them *gel_i.gro* and *fluid_i.gro* (e.g. gel_1.gro)
2. Run the script *generate_dataset.py* to create a .csv file with all training configurations.
3. Run the script *generate_model.py* to train the ML models on the .csv file and generate a model file.
4. Put the model file generated in the folder /analysis/mllpa/model/ and re-install the module (see section **Installation > Analysis above**)

### Analyse simulation files ###

ML-LPA is equiped with a TUI. Type *mllpa* in the terminal to start it.

The /analysis/mllpa/model/ folder is provided with the trained model used in the PCCP paper.

## Known issues

* The alpha version only works with **Python 3.6.5** and below.

* The alpha version only works with DPPC.

* The alpha version do not handle PBC, which leads to extremely wrong predictions of the lipid thermodynamic states. Always remove the PBC before analysis.

* The alpha version have strong compatibility version with Scikit-Learn, and it can only works with the version 0.19.1 and Numpy version 1.18.1. If you want to use the alpha version, it is recommended to use a virtual environment.

## Dependencies

* *numpy*
* *matplotlib*
* *scikit-learn*
* *pickle*
* *tqdm*
* *MDAnalysis*
* *scikit-image*
