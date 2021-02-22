import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

from mllpa.configurations.coordinates import rotateMolecules, cartesian2Polar, getCOM
from mllpa.configurations.distances import computeDistances, listPairs
from mllpa.input_output import _select_input_type, saveRepresentation
from mllpa.interface_communication import _is_int, _is_boolean, _is_string, _is_system, _is_list_of, _is_array_of, _is_array, _is_dict, _is_file_is, _error_input_type, _error_array_shape_match
from mllpa.model_generation import makePredictions, _format_input, _get_models_from_source
from mllpa.neighbour_analysis import findLeaflets, generateGhosts, findTessellations, neighborStates

##-\-\-\-\
## CLASSES
##-/-/-/-/

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Class to store the informations on the system
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class System:

    # Load the system
    def __init__( self, type, positions, infos, boxes ):

        # Check the input of the function
        if not _is_string(type):
            _error_input_type('Molecule type', str(str))
        if not _is_array(positions):
            _error_input_type('Atom positions', str(np.ndarray))
        if not _is_dict(infos):
            _error_input_type('Molecule type information dictionary', str(dict))
        if not _is_array(boxes):
            _error_input_type('Simulation box dimensions', str(np.ndarray))

        # Save the parameters
        self.type = type
        self.positions = positions
        self.boxes = boxes
        self.infos = infos

        # Initialize the other variables
        self.coordinates = None
        self.distances = None
        self.phases = None
        self.rank = -1

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## LOAD THE CONFIGURATIONS
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # -------------------
    # Get the coordinates
    def getCoordinates(self, **kwargs):

        # Extract the kwargs
        up = kwargs.get('up', True)
        if not _is_boolean(up):
            _error_input_type('Up', str(bool))

        # Centre and rotate the positions
        rotated_positions = rotateMolecules(self.positions, self.infos, up=up)

        # Convert to polar coordinates
        self.coordinates = cartesian2Polar(rotated_positions)

        return self.coordinates

    # -----------------
    # Get the distances
    def getDistances(self, **kwargs):

        # Extract the kwargs
        rank = kwargs.get('rank', 6)
        if not _is_int(rank):
            _error_input_type('Rank', str(int))

        # Get the bonds indices at the given rank
        bonds_ids = listPairs(self.infos, rank=rank)

        # Compute all the distances using the map
        self.distances = computeDistances(self.positions, bonds_ids)
        self.rank = rank

        return self.distances

    ##-\-\-\-\-\-\-\-\-\
    ## PREDICT THE STATE
    ##-/-/-/-/-/-/-/-/-/

    # --------------------------------------------------------
    # Predict the state of the molecules using the input model
    def getPhases(self, models):

        # Check that the configurations have been extracted
        if self.coordinates is None or self.distances is None:
            raise ValueError("Coordinates and Distances space are missing. Please use the function openSystem() to generate the instance of the System class.")

        # Check and extract the models
        trained_models, training_parameters = _get_models_from_source(models)

        # Format the configurations
        coordinates, distances = _format_input(self.coordinates, self.distances)

        # Predict the states of the lipids
        phases = makePredictions(coordinates, distances, trained_models)

        # Reshape the states
        self.phases = np.reshape(phases, (self.positions.shape[0], self.positions.shape[1]))

        return self.phases

    # --------------------------------------
    # Assign given state(s) to the molecules
    def setPhases(self, phases):

        # Assign a single state to all molecules
        if _is_string(phases):
            self.phases = np.array( [ [phases] * self.positions.shape[1] ] * self.positions.shape[0] )

        # Assign the array of states to the system
        elif _is_array(phases):
            _error_array_shape_match(phases, tuple((self.positions.shape[0], self.positions.shape[1])))
            self.phases = phases

        # Raise error on wrong input type
        else:
            _error_input_type("Phases","string or an array of strings")

        return self.phases

    ##-\-\-\-\-\-\-\-\
    ## OUTPUT FUNCTIONS
    ##-/-/-/-/-/-/-/-/

    # -------------------------
    # Save the system in a file
    def save(self, file_path=None, format='.csv'):

        # Extract the information from the system(s)
        representation = _system_to_tessellation(self)

        # Save the system in file
        saveRepresentation(representation, file_path=file_path, format=format)

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Class to prepare and process Voronoi tessellations
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class Tessellation:
    def __init__ (self, names, ids, positions, boxes, phases):

        # Check the input of the function
        if not _is_array_of(names, type='string', recursive=True):
            _error_input_type('Molecule names', "Array of string")
        if not _is_array_of(ids, type='int', recursive=True):
            _error_input_type('Molecule IDs', "Array of int")
        if not _is_array_of(positions, type='float', recursive=True):
            _error_input_type('Molecule positions', "Array of float")
        if not _is_array_of(boxes, type='float', recursive=True):
            _error_input_type('Simulation boxes', "Array of float")
        if not _is_array_of(phases, type='string', recursive=True):
            _error_input_type('Molecule phases', "Array of string")

        # Save the parameters
        self.names = names
        self.ids = ids
        self.positions = positions
        self.boxes = boxes
        self.phases = phases

        # Initialize the other variables
        self.leaflets = None
        self.ghosts = None
        self.volumes = None
        self.vertices = None
        self.neighbors = None
        self.geometry = None
        self.threshold = None
        self.neighbors_phases = None
        self.phases_list = None

    ##-\-\-\-\-\-\-\-\-\
    ## ANALYSE THE SYSTEM
    ##-/-/-/-/-/-/-/-/-/

    # ------------------------------
    # Get the leaflets of the lipids
    def getLeaflets(self, geometry='bilayer'):

        # Find the leaflets
        self.leaflets = findLeaflets(self.positions, geometry=geometry)

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## MAKE THE TESSELLATION
    ##-/-/-/-/-/-/-/-/-/-/-/

    # --------------------------------------------
    # Make the Voronoi tessellations on the system
    def doVoronoi(self, geometry='bilayer', threshold=0.01):

        # Save the tessellation settings
        self.geometry = geometry
        self.threshold = threshold

        # Generate the tessellations
        self.volumes, self.vertices, self.neighbors = findTessellations(self.positions, self.boxes, self.ids, self.leaflets, self.ghosts, geometry=geometry, threshold=threshold)

    # -----------------------------------------------------
    # Analyse the states of the neighbours of each molecule
    def checkNeighbors(self):

        # Extract the composition of the neighbours states
        neighbors_phases, phases_list = neighborStates(self.neighbors, self.phases)

        # Assign them as class attributes
        self.neighbors_phases = neighbors_phases
        self.phases_list = phases_list

        return neighbors_phases, phases_list

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## EXPORT THE REPRESENTATION
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/

    # --------------------------------------
    # Format the representation into a table
    def toTable(self):

        # Prepare the arrays
        formatted_frames = []
        formatted_names = []
        formatted_IDs = []
        formatted_COM_x = []
        formatted_COM_y = []
        formatted_COM_z = []
        formatted_states = []
        formatted_volumes = []
        formatted_neighbors = []

        # Process all the frames
        for frame in range(self.positions.shape[0]):

            # Get the frame and IDs
            formatted_names.append( np.copy(self.names) )
            formatted_IDs.append( np.copy(self.ids) )
            formatted_frames.append( np.array( [frame] * self.ids.shape[0] ) )

            # Get the COMs
            formatted_COM_x.append( self.positions[frame,:,0] )
            formatted_COM_y.append( self.positions[frame,:,1] )
            formatted_COM_z.append( self.positions[frame,:,2] )

            # Get the states
            formatted_states.append( self.phases[frame] )

            # Get the volumes
            if self.volumes is not None:
                formatted_volumes.append( self.volumes[frame] )

            # Get the neighbours states
            if self.neighbors_phases is not None:
                formatted_neighbors.append( self.neighbors_phases[frame] )

        # Concatenate the extracted values
        formatted_frames = np.concatenate(formatted_frames)
        formatted_names = np.concatenate(formatted_names)
        formatted_IDs = np.concatenate(formatted_IDs)
        formatted_COM_x = np.concatenate(formatted_COM_x)
        formatted_COM_y = np.concatenate(formatted_COM_y)
        formatted_COM_z = np.concatenate(formatted_COM_z)
        formatted_states = np.concatenate(formatted_states)

        # Generate the information dictionary
        data_dict = {
        'name': formatted_names,
        'frame':formatted_frames,
        'id':formatted_IDs,
        'com_x':formatted_COM_x,
        'com_y':formatted_COM_y,
        'com_z':formatted_COM_z,
        'phase':formatted_states,
        }

        # Append the volumes
        if self.volumes is not None:
            formatted_volumes = np.concatenate(formatted_volumes)
            data_dict['volumes'] = formatted_volumes

        # Append the neighbour states
        if self.neighbors_phases is not None:
            formatted_neighbors = np.concatenate(formatted_neighbors)

            # Append each states
            for i, state in enumerate(self.phases_list):
                column_name = 'neighbors_' + state
                data_dict[column_name] = formatted_neighbors[:,i]

        # Generate the dataframe
        table = pd.DataFrame(data_dict)

        return table

    ##-\-\-\-\-\-\-\-\
    ## OUTPUT FUNCTIONS
    ##-/-/-/-/-/-/-/-/

    # -------------------------
    # Save the system in a file
    def save(self, file_path=None, format='.csv'):
        saveRepresentation(self, file_path=file_path, format=format)

##-\-\-\-\-\-\-\-\-\-\
## CONVERSION FUNCTIONS
##-/-/-/-/-/-/-/-/-/-/

# -------------------------------------------
# Convert ML system(s) to systems for Voronoi
def _system_to_tessellation(systems):

    # Convert single system in list
    if _is_system(systems):
        systems = [ systems ]

    # Check the format
    if not _is_list_of(systems, type='system', check_array=True, recursive=False):
        _error_input_type('Systems', 'List of System (or single System)')

    # Extract all the system(s)
    all_IDs = []
    all_names = []
    all_COMs = []
    all_states = []
    for molecule in systems:

        # Get the molecule names and IDs
        current_IDs = molecule.infos['resids']
        current_names = np.array( [molecule.type]*current_IDs.shape[0] )

        # Get the positions
        current_COMs = getCOM( molecule.positions, molecule.infos['heavy_atoms']['masses'] )

        # Get the states
        current_states = molecule.phases

        # Store the results
        all_names.append( current_names )
        all_IDs.append( current_IDs )
        all_COMs.append( current_COMs )
        all_states.append( current_states )

    # Merge the system(s)
    all_names = np.concatenate( all_names )
    all_IDs = np.concatenate( all_IDs )
    all_COMs = np.concatenate( all_COMs, axis=1 )
    all_states = np.concatenate( all_states, axis=1 )

    # Sort the arrays according to the molecule IDs
    sorting_ids = all_IDs.argsort()
    all_names = all_names[sorting_ids]
    all_IDs = all_IDs[sorting_ids]
    all_COMs = all_COMs[:,sorting_ids,:]
    all_states = all_states[:,sorting_ids]

    # Create the instance of the Tessellation class
    representation = Tessellation(all_names, all_IDs, all_COMs, systems[0].boxes, all_states)

    return representation

# ----------------------------------------------
# Convert centers of mass to classes for Voronoi
def _coms_to_tessellation(positions, boxes, states="unknown", names="unknown", ids=None):

    # Generate the state array from string
    if _select_input_type(states, str, np.ndarray):
        states_array = np.zeros(positions.shape).astype(str)
        states_array[:] = states

        states = np.copy(states_array)

    # Generate the name array from string
    if _select_input_type(names, str, np.ndarray):
        names_array = np.zeros(positions.shape[1]).astype(str)
        names_array[:] = names

        names = np.copy(names_array)

    # Generate the ID array
    if ids is None:
        ids = np.arange(0, positions.shape[1], 1)

    # Create the instance of the Tessellation class
    representation = Tessellation(names, ids, positions, boxes, states)

    return representation
