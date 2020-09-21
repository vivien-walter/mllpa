from MDAnalysis import Universe
import numpy as np
from tqdm import tqdm
import warnings

from mllpa.configurations.distances import _map_molecule
from mllpa.input_output import _check_input_file, _check_extension
from mllpa.interface_communication import _is_int, _is_boolean, _is_dict, _error_input_type, _error_molecule_type, _error_out_of_range

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ----------------------------------------
# Coerce the values for trajectory reading
def _coerce_trajectory(begin, end, step, max_length):

    # Check the first frame
    if not _is_int(begin):
        _error_input_type('First frame',str(int))
    elif begin < 0 or begin >= max_length:
        _error_out_of_range(begin, 'First frame', 0, max_length-1)

    # Coerce the last frame
    if end is None:
        end = max_length

    else:
        if not _is_int(end):
            _error_input_type('Last frame',str(int))
        elif end <= begin or end > max_length:
            _error_out_of_range(end, 'Last frame', begin+1, max_length)

    # Check the step
    if not _is_int(step):
        _error_input_type('Frame step',str(int))
    elif step <= 0:
        _error_out_of_range(step, 'Frame step', 1, "inf")

    return begin, end, step

##-\-\-\-\-\-\-\-\-\
## EXTRACT THE SYSTEM
##-/-/-/-/-/-/-/-/-/

# ---------------------------------------------------------
# Extract the positions of the atoms in the box coordinates
def _get_positions(coordinates_file, type=None, trj=None, heavy=True, type_info=None, begin=0, end=None, step=1):

    # ---------------------
    # CHECK THE USER INPUTS

    # Check the files extensions
    _check_input_file(coordinates_file, extensions=[".gro"])
    if trj is not None:
        _check_input_file(trj, extensions=[".xtc", ".trr"])

    # Load the system and set the time limits
    if trj is None:
        system = Universe(coordinates_file)
        begin, end, step = 0, 1, 1
    else:
        system = Universe(coordinates_file, trj)
        begin, end, step = _coerce_trajectory(begin, end, step, len(system.trajectory))

    # Check if the molecule type exists
    _error_molecule_type(type, np.unique( system.select_atoms("all").resnames ))

    # Check if the other kwargs have the good format
    if not _is_boolean(heavy):
        _error_input_type('Heavy atom selection', str(bool))
    if type_info is not None:
        if not _is_dict(type_info):
            error_input_type('Molecule type information dictionary', str(dict))

    # ----------------
    # RUN THE FUNCTION

    # Create the selection
    selection_text = "resname "+type
    if heavy:
        selection_text += " and not type H"
    selected_molecules = system.select_atoms(selection_text)

    # Extract the required informations
    if type_info is None:
        n_molecules = np.unique( selected_molecules.resids ).shape[0]
    else:
        n_molecules = type_info['n_molecules']

    # Read all the frames
    all_frames = []
    all_boxes = []
    for i_frame in tqdm(range(begin, end, step), desc='Extracting '+type+' positions...'):

        # Move to the selected frame
        system.trajectory[i_frame]

        # Extract the positions
        current_positions = selected_molecules.positions

        # Reshape the positions
        n_frames = 1
        n_atoms = int(current_positions.shape[0] / n_molecules)
        current_positions = np.reshape(current_positions, (n_molecules, n_atoms, 3))

        # Get the box dimensions
        box_size = system.dimensions[0:3]

        # Save the positions
        all_frames.append( current_positions )
        all_boxes.append( np.copy(box_size) )

    # Get the array
    positions = np.array(all_frames)
    boxes = np.array(all_boxes)

    return positions, boxes

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## GET THE INFO ON THE SYSTEM
##-/-/-/-/-/-/-/-/-/-/-/-/-/

# ----------------------------------------------------------
# Extract the list of all unique residue types in the system
def _list_types(coordinates_file):

    # Check the extension
    _check_input_file(coordinates_file, extensions=[".gro"])

    # Load the system
    system = Universe(coordinates_file)

    # List the residue names
    resnames = system.select_atoms("all").resnames

    return np.unique(resnames)

# ------------------------------------------------------
# Get all the relevant informations on the molecule type
def _get_type_info(structure_file, type):

    # ---------------------
    # CHECK THE USER INPUTS

    # Check the extension
    _check_input_file(structure_file, extensions=[".tpr"])

    # Load the system
    with warnings.catch_warnings():
        warnings.simplefilter("ignore") # NOTE: Remove auto warning when loading a .tpr file in MDAnalysis
        system = Universe(structure_file)

    # Check that the type exists
    _error_molecule_type(type, np.unique( system.select_atoms("all").resnames ))

    # ----------------
    # RUN THE FUNCTION

    # Get the residue IDs
    resids = np.unique( system.select_atoms("resname "+type).resids )
    n_molecules = resids.shape[0]

    # Get the atom selections
    atom_selection = system.select_atoms("resid "+str(resids[0]))
    heavy_atom_selection = system.select_atoms("resid "+str(resids[0])+" and not type H*")

    # Get the names
    atom_names = atom_selection.names
    n_atoms = atom_names.shape[0]
    heavy_atom_names = heavy_atom_selection.names
    n_heavy_atoms = heavy_atom_names.shape[0]

    # Get the masses
    atom_masses = atom_selection.masses
    heavy_atom_masses = heavy_atom_selection.masses

    # Get the IDs of the heavy atoms
    heavy_atom_ids = np.array( [i for i, name in enumerate(atom_names) if name in heavy_atom_names] )

    # Get the bonds
    with warnings.catch_warnings():
        warnings.simplefilter("ignore") # NOTE: Warning on deprecation! Check how to fix it then remove the warning disabling
        atom_bonds, heavy_atom_bonds = _map_molecule(atom_selection, heavy_atom_selection)

    # Generate the dictionary
    molecule_info = {
    'resids': resids,
    'n_molecules': n_molecules,
    'atoms':{
        'names': atom_names,
        'number': n_atoms,
        'masses': atom_masses,
        'bonds': atom_bonds,
        },
    'heavy_atoms':{
        'names': heavy_atom_names,
        'number': n_heavy_atoms,
        'masses': heavy_atom_masses,
        'ids': heavy_atom_ids,
        'bonds': heavy_atom_bonds,
        }
    }

    return molecule_info
