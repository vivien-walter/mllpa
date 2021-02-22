from datetime import datetime
import h5py
import MDAnalysis
import numpy as np
import os
import pandas as pd
import platform
import sklearn
import sys
from tqdm import tqdm
import xml.etree.ElementTree as xml
import zipfile

from mllpa.interface_communication import _is_file, _is_file_is, _error_extension, _error_input_file, _error_input_type

##-\-\-\-\-\-\-\-\
## FILE MANAGEMENT
##-/-/-/-/-/-/-/-/

# -----------------------------
# Check the input file provided
def _check_input_file(file, extensions=[".gro"]):

    # Check if the file exists
    if not _is_file(file):
        _error_input_file(file)

    # Check the extension
    if not _is_file_is(file, extensions=extensions, exist=True, no_extension=False):
        _error_extension(os.path.splitext(file)[1])

# -------------------------------
# Check the extension of the file
def _check_extension(file, extensions=[".gro"], stop=False, error=True): # argument(s) error is now deprecated. Please remove

    # Check the extension
    if not _is_file_is(file, extensions=extensions, exist=stop, no_extension=stop):
        _error_extension(os.path.splitext(file)[1])

    # Split the elements
    file_name, file_ext = os.path.splitext(file)
    if file_ext == "" and not stop:
        file = file_name + extensions[0]

    return file

# --------------------------------------------
# Control the input type and select what to do
def _select_input_type(input, type_A, type_B):

    # Check if the input type is of type A
    if isinstance(input, type_A):
        is_A = True

    # Check if the input type is of type B
    elif isinstance(input, type_B):
        is_A = False

    # Raise an error
    else:
        is_A = False
        _error_input_type()

    return is_A

# ----------------------------
# Generate a default file name
def _generate_file_name(type=None, extension=".lpm", hms=False):

    # Get the formatted date
    if hms:
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        current_date = datetime.now().strftime("%Y%m%d")

    # Get the name
    file_name = current_date
    if type is not None:
        file_name += "_" + type.upper()
    file_name += extension

    return file_name

# -----------------------------------------
# Check or generate a default name and type
def _generate_file_type(name, format='.csv', extensions=[".csv", ".xml", ".h5"]):

    # Generate a default file name if none is provided
    if name is None:
        name = _generate_file_name(type=None, extension=format, hms=True)

    # Check and correct the extension if needed
    name = _check_extension(name, extensions=extensions, stop=False)

    return name

##-\-\-\-\-\
## XML FILES
##-/-/-/-/-/

# ------------------------------------
# Write all the scores in the XML tree
def _score2xml(score_data, training_scores, training_errors, states):

    total_score = xml.SubElement(score_data, 'final')
    total_score.set('total', str(training_scores['final_score']['total'])+" ± "+str(training_errors['final_score']['total']) )
    for state in states:
        total_score.set(state, str(training_scores['final_score'][state])+" ± "+str(training_errors['final_score'][state]) )

    initial_score = xml.SubElement(score_data, 'initial')

    svmc_score = xml.SubElement(initial_score, 'svm_coordinates')
    svmc_score.set('total', str(training_scores['SVM_Coordinates']['total'])+" ± "+str(training_errors['SVM_Coordinates']['total']) )
    for state in states:
        svmc_score.set(state, str(training_scores['SVM_Coordinates'][state])+" ± "+str(training_errors['SVM_Coordinates'][state]) )

    knnc_score = xml.SubElement(initial_score, 'knn_coordinates')
    knnc_score.set('total', str(training_scores['KNN_Coordinates']['total'])+" ± "+str(training_errors['KNN_Coordinates']['total']) )
    for state in states:
        knnc_score.set(state, str(training_scores['KNN_Coordinates'][state])+" ± "+str(training_errors['KNN_Coordinates'][state]) )

    svmd_score = xml.SubElement(initial_score, 'svm_distances')
    svmd_score.set('total', str(training_scores['SVM_Distances']['total'])+" ± "+str(training_errors['SVM_Distances']['total']) )
    for state in states:
        svmd_score.set(state, str(training_scores['SVM_Distances'][state])+" ± "+str(training_errors['SVM_Distances'][state]) )

    nbd_score = xml.SubElement(initial_score, 'nb_distances')
    nbd_score.set('total', str(training_scores['NB_Distances']['total'])+" ± "+str(training_errors['NB_Distances']['total']) )
    for state in states:
        nbd_score.set(state, str(training_scores['NB_Distances'][state])+" ± "+str(training_errors['NB_Distances'][state]) )

# -------------------------------------
# Create the metadata file of the model
def _generate_metadata_content(general_info, system_info, training_info, training_scores, training_errors):

    # Initialise the tree
    model_data = xml.Element('model')

    # Save the general data
    general_data = xml.SubElement(model_data, 'general')

    general_data.set('type', general_info['type'] )
    general_data.set('date', datetime.now().strftime("%d/%m/%Y-%H:%M:%S") )
    general_data.set('python-version', str(platform.python_version()))
    general_data.set('scikit-learn-version', str(sklearn.__version__))
    general_data.set('mdanalysis-version', str(MDAnalysis.__version__))
    general_data.set('mllpa-version', "beta")

    state_list = general_info['phases']
    state_text = state_list[0]
    for state in state_list[1:]:
        state_text += "," + state

    general_data.set('phases', state_text )

    # Save the training set data
    training_data = xml.SubElement(model_data, 'training')

    training_data.set('n_molecules',system_info['n_molecules'])
    training_data.set('n_atoms_per_molecule', system_info['n_atoms_per_molecule'])
    training_data.set('n_distances_per_molecule', system_info['n_distances_per_molecule'])
    training_data.set('rank', system_info['rank'])
    training_data.set('validation_size', training_info['validation_size'])
    training_data.set('seed', training_info['seed'])
    training_data.set('n_splits', training_info['n_splits'])

    # Save the scores data
    score_data = xml.SubElement(model_data, 'scores')
    _score2xml(score_data, training_scores, training_errors, state_list)

    return xml.tostring(model_data, encoding='unicode')

# ---------------------------------------------
# Create the .xml version of the representation
def _generate_representation_content(representation):

    # Initialise the tree
    representation_data = xml.Element('representation')

    # Save the general data
    for frame in tqdm(range(representation.positions.shape[0]), desc='Writing frames as .xml...'):

        # Initialise the frame
        current_frame = xml.SubElement(representation_data, 'frame')
        current_frame.set('index',str(frame))
        current_frame.set('box_x',str(representation.boxes[frame, 0]))
        current_frame.set('box_y',str(representation.boxes[frame, 1]))
        current_frame.set('box_z',str(representation.boxes[frame, 2]))

        # Save all the molecules
        for molecule in range(representation.positions.shape[1]):

            # Save the molecule infos
            current_molecule = xml.SubElement(current_frame, 'molecule')
            current_molecule.set("name", str(representation.names[molecule]))
            current_molecule.set("id", str(representation.ids[molecule]))
            current_molecule.set("x", str(representation.positions[frame, molecule, 0]))
            current_molecule.set("y", str(representation.positions[frame, molecule, 1]))
            current_molecule.set("z", str(representation.positions[frame, molecule, 2]))
            current_molecule.set("state", str(representation.phases[frame, molecule]))

            # Add the volumes
            if representation.volumes is not None:
                current_molecule.set("volume", str(representation.volumes[frame, molecule]))


            # Add the neighbour states
            if representation.neighbors_phases is not None:

                # Process all states
                for i, state in enumerate(representation.phases_list):
                    column_name = 'neighbors_' + state
                    current_molecule.set(column_name, str(representation.neighbors_phases[frame, molecule, i]))

            # Add the neighbour list
            if representation.neighbors is not None:

                # Create the string
                current_neighbors_list = representation.neighbors[frame][molecule]
                current_neighbors_string = str(current_neighbors_list[0])
                for neighbor_id in current_neighbors_list[1:]:
                    current_neighbors_string += ',' + str(neighbor_id)

                # Write in file
                current_molecule.set('neighbors', current_neighbors_string)

            # Add the cell vertices
            if representation.vertices is not None:

                # Get the vertices
                vertices_list = representation.vertices[frame][molecule]

                # Create the vertices list
                for j, vertices in enumerate(vertices_list):
                    current_vertice = xml.SubElement(current_molecule, 'vertices')
                    current_vertice.set("index", str(j))
                    current_vertice.set("x", str(vertices[0]))
                    current_vertice.set("y", str(vertices[1]))
                    current_vertice.set("z", str(vertices[2]))

        # Save the box dimensions
        current_box = xml.SubElement(current_frame, 'box')
        current_box.set("x", str(representation.boxes[frame, 0]))
        current_box.set("y", str(representation.boxes[frame, 1]))
        current_box.set("z", str(representation.boxes[frame, 2]))

    return xml.tostring(representation_data, encoding='unicode')

# ------------------------------------
# Get the content of the metadata file
def _get_metadata_content(xml_file):

    # Load the XML tree
    tree = xml.parse(xml_file)
    root = tree.getroot()

    # Extract the attributes
    for child in root:

        # Extract the general informations
        if child.tag == 'general':

            # Extract the dictionary
            general_infos = dict(child.attrib)

            # Convert some values
            general_infos['phases'] = general_infos['phases'].split(",")

        # Extract the information on the training
        elif child.tag == 'training':

            # Extract the dictionary
            training_infos = dict(child.attrib)

            # Convert the values
            for key in training_infos.keys():
                if key == 'validation_size':
                    training_infos[key] = float( training_infos[key] )
                else:
                    training_infos[key] = int( training_infos[key] )

        # Extract the training scores
        elif child.tag == 'scores':

            # Initialise the dictionaries
            training_scores = {}
            training_errors = {}

            # Process the scores
            for subchild in child:

                # Get the final score
                if subchild.tag == 'final':

                    # Initialise
                    training_scores['final'] = {}
                    training_errors['final'] = {}

                    # Extract the dictionary
                    final_score_dict = dict(subchild.attrib)

                    # Extract and convert the values
                    for key in final_score_dict.keys():

                        # Get value and score
                        score, error = final_score_dict[key].split('±')

                        # Save
                        training_scores['final'][key] = float(score)
                        training_errors['final'][key] = float(error)

                # Get the first step training scores
                elif subchild.tag == 'initial':

                    # Process all algorithms
                    for algorithm in subchild:

                        # Initialise
                        training_scores[algorithm.tag] = {}
                        training_errors[algorithm.tag] = {}

                        # Extract the dictionary
                        algorithm_score_dict = dict(algorithm.attrib)

                        # Extract and convert the values
                        for key in algorithm_score_dict.keys():

                            # Get value and score
                            score, error = algorithm_score_dict[key].split('±')

                            # Save
                            training_scores[algorithm.tag][key] = float(score)
                            training_errors[algorithm.tag][key] = float(error)

    return general_infos, training_infos, training_scores, training_errors

##-\-\-\-\-\
## HTF5 FILES
##-/-/-/-/-/

# ---------------------------------------------
# Create the .htf5 version of the representation
def _generate_representation_binary(representation, file_path):

    # Initialise the tree
    representation_output = h5py.File(file_path, 'w')

    # Prepare the string arrays for the names
    molecule_names = list( np.unique(representation.names) )
    molecule_names_by_ID = np.zeros(representation.names.shape).astype(np.uint8)

    for i, name in enumerate(molecule_names):
        molecule_names_by_ID[representation.names == name] = i

    representation_output.attrs['molecule_names'] = molecule_names

    # Prepare the string arrays for the states
    molecule_states = list( np.unique(representation.phases) )
    molecule_states_by_ID = np.zeros(representation.phases.shape).astype(np.uint8)

    for i, state in enumerate(molecule_states):
        molecule_states_by_ID[representation.phases == state] = i

    representation_output.attrs['molecule_phases'] = molecule_states

    # Save the data
    representation_output.create_dataset('names', data=molecule_names_by_ID)
    representation_output.create_dataset('ids', data=representation.ids)
    representation_output.create_dataset('center_of_masses', data=representation.positions)
    representation_output.create_dataset('states', data=molecule_states_by_ID)
    representation_output.create_dataset('boxes', data=representation.boxes)

    # Save the volumes
    if representation.volumes is not None:
        representation_output.create_dataset('volumes', data=representation.volumes)

    # Save the neighbour states
    if representation.neighbors_phases is not None:

        # Save the list of states
        representation_output.attrs['phases_list'] = list(representation.phases_list)

        # Save the composition of the neighbour states
        representation_output.create_dataset('neighbors_phases', data=representation.neighbors_phases)

    # Save and close the file
    representation_output.close()

##-\-\-\-\-\-\
## MODEL FILES
##-/-/-/-/-/-/

# -------------------------------------
# Create the file to store the model in
def generateModelFile(coordinates, distances, phases, general_info, system_info, training_info, training_scores, training_errors, file_path=None):

    # Get the file name
    if file_path is None:
        file_path = _generate_file_name(general_info['type'], extension='.lpm')
    file_path = _check_extension(file_path, extensions=[".lpm"], stop=False)

    # Get the file root path
    root_path = os.path.dirname(file_path)

    # Generate the metadata file
    metadata_content = _generate_metadata_content(general_info, system_info, training_info, training_scores, training_errors)
    metadata_file = os.path.join(root_path, 'model_data.xml')
    with open( metadata_file, "w" ) as xml_file:
        xml_file.write(metadata_content)

    # Generate the training set files
    coordinates_file = os.path.join(root_path, 'model_coordinates.csv')
    distances_file = os.path.join(root_path, 'model_distances.csv')
    phases_file = os.path.join(root_path, 'model_phases.csv')

    np.savetxt(coordinates_file, coordinates, delimiter=',')
    np.savetxt(distances_file, distances, delimiter=',')
    np.savetxt(phases_file, phases, delimiter=',', fmt="%s")

    # Zip the files
    compressed_file = zipfile.ZipFile(file_path, mode='w')

    compressed_file.write(coordinates_file)
    compressed_file.write(distances_file)
    compressed_file.write(phases_file)
    compressed_file.write(metadata_file)

    compressed_file.close()

    # Remove the original files after compression
    os.remove(coordinates_file)
    os.remove(distances_file)
    os.remove(phases_file)
    os.remove(metadata_file)

# -----------------------------------------------------
# Open and extract the informations from the model file
def openModelFile(file_path):

    # Check the extension of the file
    _check_extension(file_path, extensions=[".lpm"], stop=True)

    # Get the file from the archive
    compressed_file = zipfile.ZipFile(file_path)

    # Process all the data files
    for file in compressed_file.namelist():

        current_data = compressed_file.read(file)

        current_file = open(file, 'w')
        current_file.write(current_data.decode("utf-8"))
        current_file.close()

    # Extract the training sets from the file
    coordinates = np.loadtxt('model_coordinates.csv', delimiter=',')
    distances = np.loadtxt('model_distances.csv', delimiter=',')
    phases = np.loadtxt('model_phases.csv', delimiter=',', dtype=str)

    # Extract the training parameters from the file
    general_info, training_infos, training_scores, training_errors = _get_metadata_content('model_data.xml')
    metadata_content = {
    'general': general_info,
    'training': training_infos,
    'scores': {
    'scores' : training_scores,
    'errors' : training_errors
    }
    }

    # Delete the files after loading informations
    for file in compressed_file.namelist():
        os.remove(file)
    compressed_file.close()

    return coordinates, distances, phases, metadata_content

# ---------------------------------------------------
# Display the content of the metadata in the terminal
def _display_metadata(metadata_content):

    # General content
    general_text = """
-------
GENERAL
-------
Date: """ +str(metadata_content['general']['date'])+  """

# VERSIONS
*) Python: """ + str(metadata_content['general']['python-version']) + """
*) ML-LPA: """ + str(metadata_content['general']['mllpa-version']) + """
*) Scikit-Learn: """ + str(metadata_content['general']['scikit-learn-version']) + """
*) MDAnalysis: """ + str(metadata_content['general']['mdanalysis-version']) + """

# TRAINED SYSTEMS
*) Molecule Type: """ + str(metadata_content['general']['type']) + """
*) Phases: """ + str(metadata_content['general']['phases'])
    print(general_text)

    # Training content
    training_text = """
----------------
MODEL GENERATION
----------------

# MOLECULES
*) Nbr Molecules: """ + str(metadata_content['training']['n_molecules']) + """
*) Nbr Atoms per molecule: """ + str(metadata_content['training']['n_atoms_per_molecule']) + """
*) Nbr Distances per molecule: """ + str(metadata_content['training']['n_distances_per_molecule']) + """
(Rank: """ + str(metadata_content['training']['rank']) + """)

# TRAINING
*) Subset size: """ + str(metadata_content['training']['validation_size']) + """
*) Nbr Repetitions: """ + str(metadata_content['training']['n_splits']) + """
*) Random Seed: """ + str(metadata_content['training']['seed'])
    print(training_text)

    # Training scores
    scores_dict = metadata_content['scores']['scores']
    errors_dict = metadata_content['scores']['errors']

    scores_text = """
---------------
TRAINING SCORES
---------------

# FINAL SCORES
*) Total: """ + str(scores_dict['final']['total']) + " ± " + str(errors_dict['final']['total'])

    # Add the phases
    for key in scores_dict['final'].keys():
        if key != "total":
            scores_text += "\n*) "+str(key)+": " + str(scores_dict['final'][key]) + " ± " + str(errors_dict['final'][key])

    scores_text +="""

# 1st MODELS SCORES"""

    # Add the first models
    for model_name in scores_dict.keys():
        if model_name != "final":

            # Print the name and total score
            scores_text += """
- """ + str(model_name.upper()) + """
*) Total: """ + str(scores_dict[model_name]['total']) + " ± " + str(errors_dict[model_name]['total'])

            # Add the phases
            for key in scores_dict[model_name].keys():
                if key != "total":
                    scores_text += "\n*) "+str(key)+": " + str(scores_dict[model_name][key]) + " ± " + str(errors_dict[model_name][key])

    print(scores_text)

##-\-\-\-\-\-\-\-\-\-\
## REPRESENTATION FILES
##-/-/-/-/-/-/-/-/-/-/

# -------------------------------
# Save the representation in file
def saveRepresentation(representation, file_path=None, format='.csv'):

    # Get the file name
    file_path = _generate_file_type(file_path, format=format, extensions=[".h5", ".xml", ".csv"])

    # Create the file
    file_name, file_extension = os.path.splitext(file_path)

    # Save in a .CSV file
    if file_extension == ".csv":
        representation_content = representation.toTable()
        representation_content.to_csv(file_path)

    # Save in a structured file (XML)
    elif file_extension == ".xml":
        representation_content = _generate_representation_content(representation)
        with open( file_path, "w" ) as xml_file:
            xml_file.write(representation_content)

    # Save in a structured file (HTF5)
    else:
        _generate_representation_binary(representation, file_path)
