import numpy as np
import os
import sys

##-\-\-\-\-\
## CHECK TYPE
##-/-/-/-/-/

# ----------
# If boolean
def _is_boolean(data):
    return isinstance(data, bool)

# ----------
# If integer
def _is_int(data):
    return isinstance(data, int) or isinstance(data, np.int64)

# --------
# If float
def _is_float(data, **kwargs):

    # Read the kwargs
    strict = kwargs.get('strict', False)

    # Accept integers as well
    if not strict:
        try:
            data = float(data)
        except:
            pass

    return isinstance(data, float)

# ---------
# If string
def _is_string(data):
    return isinstance(data, str)

# -------
# If list
def _is_list(data, check_array=True):

    # Check array too
    if check_array:
        if isinstance(data, list) or _is_array(data):
            return True
        else:
            return False

    else:
        isinstance(data, list)

# --------
# If array
def _is_array(data):
    return isinstance(data, np.ndarray)

# -------------
# If dictionary
def _is_dict(data):
    return isinstance(data, dict)

# ---------------
# If System class
def _is_system(data):
    return str(type(data)).split("'")[1] == "mllpa.system_class.System"

# ---------------------
# If Tessellation class
def _is_tessellation(data):
    return str(type(data)).split("'")[1] == "mllpa.system_class.Tessellation"

# -------
# If file
def _is_file(data):
    return os.path.isfile(str(data))

# ----------------
# If file is (...)
def _is_file_is(data, extensions=['.csv'], exist=True, no_extension=False):

    # Check if file exist
    if exist and not _is_file(data):
        return False

    # Check the extension
    else:

        # Get the extension
        file_name, file_ext = os.path.splitext(data)

        # Check if an extension exists
        if file_ext == "":
            return no_extension

        # Check the type of extension
        else:
            return file_ext in extensions

# ---------------------------
# If list (or array) of (...)
def _is_list_of(data, type='string', check_array=True, recursive=True, **kwargs):

    # Check if is a list
    if _is_list(data, check_array=check_array):

        # Get the first element
        item = data[0]

        # Check recursively for the first non-list element
        if recursive:
            while _is_list(item, check_array=check_array):
                item = item[0]

        # Check the type of the element
        if type == 'int':
            return _is_int(item)

        elif type == 'float':
            return _is_float(item, **kwargs)

        elif type == 'string':
            return _is_string(item)

        elif type == 'system':
            return _is_system(item)

    else:
        return False

# -----------------
# If array of (...)
def _is_array_of(data, type='string', recursive=True, **kwargs):

    # Check if is a list
    if _is_array(data):

        # Get the first element
        item = data[0]

        # Check recursively for the first non-list element
        if recursive:
            while _is_array(item):
                item = item[0]

        # Check the type of the element
        if type == 'int':
            return _is_int(item)

        elif type == 'float':
            return _is_float(item, **kwargs)

        elif type == 'string':
            return _is_string(item)

    else:
        return False

##-\-\-\-\-\-\-\
## ERROR MESSAGES
##-/-/-/-/-/-/-/

# ------------------------
# Get the decision message
def _error_decision_message(stop=True, extensions=['.gro']):

    if stop:
        decision_text = " The program will now be interrupted."
    else:
        decision_text = " The extension will be changed to "+extensions[0]+"."

    return decision_text

# -------------------------------------------------------------------------------------
# Display the error message if the array shape has not the correct number of dimensions
def _error_array_shape(array_shape, dimensions, description):
    if len(array_shape) != dimensions:  raise TypeError("The input array has not the correct shape ()"+str(array_shape)+"). The expected dimensions are "+description+".")

# ----------------------------------------------------------
# Display the error message if the array shapes do not match
def _error_array_shape_match(array, reference_shape):

    # Check the dimension of the shape
    if array.shape != reference_shape:
        raise IndexError("The input array has not the correct shape "+str(array.shape)+". The expected shape is "+str(reference_shape)+".")

# -------------------------------------------------------
# Display the error message if the extension is incorrect
def _error_extension(file_extension, extensions=None, stop=False, error=True): # Kwargs deprecated - to remove
    raise ValueError("The file extension "+file_extension+" cannot be processed by the required function.")

# ----------------------------------------------------------
# Display the error message if the input file does not exist
def _error_input_file(file):
    raise FileNotFoundError("The input file "+file+" does not exist.")

# -------------------------------------------------------------
# Display the error message when an input value is out of range
def _error_out_of_range(value, value_type, v_min, v_max):
    raise IndexError("The input value for "+value_type+" ("+str(value)+") is out of range ("+str(v_min)+";"+str(v_max)+")")

# -------------------------------------------------------
# Display the error message if an integer is not provided
def _error_input_integer():
    raise TypeError("An integer is expected.")

# -------------------------------------------------------
# Display the error message if the file type is incorrect
def _error_input_type(input_value, type_expected):
    raise TypeError("The "+input_value+" is not a "+str(type_expected))

# -----------------------------------------------------------------
# Display the error message if the molecule type is not in the list
def _error_molecule_type(resname, list_residue):

    # Check the input format
    if not _is_string(resname):
        _error_input_type('Molecule type',str(str))

    # Check the type
    if resname not in list_residue:
        text = "The molecule type "+resname+" cannot be found in the list of residues of the simulation ("+list_residue[0]

        # Add all the types
        if len(list_residue) > 1:
            for residue in list_residue[1:]:
                text += ", "+residue

        # Complete the text
        text += ")."

        raise ValueError(text)

# ------------------------------------------------------------
# Display the error message if the systems cannot be be merged
def _error_system_merged(systems):

    # Check that the input is a list of systems
    if not _is_list_of(systems, type='system', check_array=True):
        _error_input_type('Systems', 'list of System classes')

    # Initialise the arrays
    mol_types = []
    n_molecules = []
    n_distances = []
    n_rank = []

    # Gather all the informations that can prevent merging
    for system in systems:
        mol_types.append( system.type )
        n_molecules.append( system.coordinates.shape[0]*system.coordinates.shape[1] )
        n_molecules.append( system.distances.shape[0]*system.distances.shape[1] )
        n_distances.append( system.distances.shape[2] )
        n_rank.append( system.rank )

    # Check that the systems can be merged
    verification = 1
    verification *= len(set(mol_types))
    verification *= len(set(n_molecules))
    verification *= len(set(n_distances))
    verification *= len(set(n_rank))

    # Interrupt and raise error if cannot be merged
    if verification != 1:
        raise ValueError("The provided systems cannot be merged as they do not satisfy all the following conditions: (i) Same molecule types extracted, (ii) Same number of molecules, (iii) Same number of distances and/or (iv) Same rank.")

# ------------------------------------------------------------------------------------
# Display the error message if the validation size and the training sets are too small
def _error_training_size(system_size, validation_size):

    # Check the number of sample in the validation subset
    subset_size = system_size * validation_size

    # Raise an error if < 100
    if subset_size < 100:
        raise ValueError("The provided systems and validation size will generate a training subset with "+str(subset_size)+" molecules. A subset of more than 100 molecules is required for a proper training.")
