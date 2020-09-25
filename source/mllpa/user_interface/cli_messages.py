import datetime
import time

##-\-\-\-\-\-\-\
## HELP MESSAGES
##-/-/-/-/-/-/-/

# ---------------------------------
# Display the main message of MLLPA
def _main_message():
    text = """
      ___           ___       ___       ___           ___
     /\__\         /\__\     /\__\     /\  \         /\  \\
    /::|  |       /:/  /    /:/  /    /::\  \       /::\  \\
   /:|:|  |      /:/  /    /:/  /    /:/\:\  \     /:/\:\  \\
  /:/|:|__|__   /:/  /    /:/  /    /::\~\:\  \   /::\~\:\  \\
 /:/ |::::\__\ /:/__/    /:/__/    /:/\:\ \:\__\ /:/\:\ \:\__\\
 \/__/~~/:/  / \:\  \    \:\  \    \/__\:\/:/  / \/__\:\/:/  /
       /:/  /   \:\  \    \:\  \        \::/  /       \::/  /
      /:/  /     \:\  \    \:\  \        \/__/        /:/  /
     /:/  /       \:\__\    \:\__\                   /:/  /
     \/__/         \/__/     \/__/                   \/__/

Welcome to the Command Line Interface of ML-LPA.

To start using this software, please use one of the following commands:
mllpa train_model
mllpa read_phases
mllpa do_voronoi
mllpa read_model

For further information, please read the documentation inside the commands
(e.g. mllpa train_model -h) or visit the website of the project
at https://vivien-walter.github.io/mllpa/"""

    return text

# ---------------------------------------------------
# Return the text for the description of the function
def _train_model_description():
    text = "train_model is a ML-LPA command that can be used to generate model files to "
    text += "later predict the phases of lipid molecules. It takes as an input different "
    text += "simulation files (coordinates, structure and optionnaly trajectory), "
    text += "extract one specific molecule type of the file and use all the molecules "
    text += "found to train a serie of Machine Learning classification algorithms."
    text += "\n\n"
    text += "train_model is based on the following function(s): openSystem() and generateModel(). "
    text += "An extensive documentation on the command and the function(s) can be found "
    text += "on the ML-LPA website: https://vivien-walter.github.io/mllpa/"

    return text

# ---------------------------------------------
# Return the text for the usage of the function
def _train_model_usage():
    text = """mllpa train_model [-h] -c COORDINATES [COORDINATES ...] -s STRUCTURE
             [STRUCTURE ...] -mol MOLECULE_TYPE [-p PHASES [PHASES ...]]
             [-t TRAJECTORY [TRAJECTORY ...]] [-b BEGIN] [-e END] [-step STEP]
             [-o OUTPUT_FILE] [-heavy] [-up] [-rk RANK]
             [-vsize VALIDATION_SIZE] [-sd RANDOM_SEED]
             [-nr NUMBER_REPETITIONS]"""

    return text

# ---------------------------------------------------
# Return the text for the description of the function
def _read_phases_description():
    text = "read_phases is a ML-LPA command that can be used to find the phases of the "
    text += "molecules in simulation file(s), based on a pre-trained Machine Learning model. "
    text += "The results are returned inside a file containing the centers of mass of all "
    text += "the particles in the system."
    text += "\n\n"
    text += "read_phases is based on the following function(s): openSystem(), getPhases(), "
    text += "setPhases() and saveSystems(). "
    text += "An extensive documentation on the command and the function(s) can be found "
    text += "on the ML-LPA website: https://vivien-walter.github.io/mllpa/"

    return text

# ---------------------------------------------
# Return the text for the usage of the function
def _read_phases_usage():
    text = """mllpa read_phases [-h] -c COORDINATES -s STRUCTURE -mol MOLECULE_TYPES
             [MOLECULE_TYPES ...] -m MODELS [MODELS ...] [-t TRAJECTORY]
             [-b BEGIN] [-e END] [-step STEP] [-o OUTPUT_FILE] [-heavy] [-up]
             [-rk RANK]"""

    return text

# ---------------------------------------------------
# Return the text for the description of the function
def _do_voronoi_description():
    text = "do_voronoi is a ML-LPA command that can be used to analyse the local "
    text += "environment of the molecules using a Voronoi tessellations to map the neighbors. "
    text += "The results are returned inside a file containing the centers of mass of all "
    text += "the particles in the system."
    text += "\n\n"
    text += "do_voronoi is based on the following function(s): openSystem(), getPhases(), "
    text += "setPhases(), doVoro() and saveVoro(). "
    text += "An extensive documentation on the command and the function(s) can be found "
    text += "on the ML-LPA website: https://vivien-walter.github.io/mllpa/"

    return text

# ---------------------------------------------
# Return the text for the usage of the function
def _do_voronoi_usage():
    text = """mllpa do_voronoi [-h] -c COORDINATES -s STRUCTURE -mol MOLECULE_TYPES
             [MOLECULE_TYPES ...] -m MODELS [MODELS ...] [-t TRAJECTORY]
             [-b BEGIN] [-e END] [-step STEP] [-geo GEOMETRY]
             [-excl EXCLUDE_GHOSTS [EXCLUDE_GHOSTS ...]] [-o OUTPUT_FILE]
             [-local] [-heavy] [-up] [-rk RANK] [-th THRESHOLD]"""

    return text

# ---------------------------------------------------
# Return the text for the description of the function
def _read_model_description():
    text = "read_model is a ML-LPA command that can be used to read the content of "
    text += "a model file and display all the values stored inside it."
    text += "\n\n"
    text += "read_model is based on the following function(s): readModelFile(). "
    text += "An extensive documentation on the command and the function(s) can be found "
    text += "on the ML-LPA website: https://vivien-walter.github.io/mllpa/"

    return text

# ---------------------------------------------
# Return the text for the usage of the function
def _read_model_usage():
    text = """mllpa read_model [-h] -m MODELS"""

    return text

##-\-\-\-\-\-\-\-\-\
## HEADER AND FOOTER
##-/-/-/-/-/-/-/-/-/

# ----------------------------------
# Display the header of the function
def _get_header():
    text = "=========================================================================="
    return text

# ----------------------------------
# Display the footer of the function
def _get_footer(start_time):

    # Prepare the timing
    total_time = time.time() - start_time

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    # Generate the text
    text = """
==========================================================================
ML-LPA was executed in """+ "{:.4f}".format(total_time) + " sec. ("+date+""")
=========================================================================="""

    return text

##-\-\-\-\-\-\-\
## ERROR MESSAGES
##-/-/-/-/-/-/-/

# ---------------------------------------------------
# Raise an error when an incorrect function is called
def _error_function_selection(func_name):
    raise KeyError("The command "+str(func_name)+ " does not exist in ML-LPA.")
