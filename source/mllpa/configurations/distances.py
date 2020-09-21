import numpy as np
from pylab import arange, hstack
from tqdm import tqdm

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## CONSTRUCT THE MAP OF THE MOLECULE
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# ------------------------------
# Create the map of the molecule
def _map_molecule(selection, heavy_selection):

    # Load the information arrays from the file
    atom_name_array = selection.names
    atom_id_array = selection.atoms.ids
    nonH_id_array = heavy_selection.atoms.ids
    bonds_id_array = heavy_selection.bonds._bix

    # Build the index-name dictionaries
    atom_name_dict = {atom_id_array[k]: v for k, v in enumerate(atom_name_array)}
    nonH_id_dict = {k: v for v, k in enumerate(nonH_id_array)}

    # Construct the bonds array by name
    bonds_name_array = np.zeros(bonds_id_array.shape).astype(str)
    for old_index, new_index in atom_name_dict.items():
        bonds_name_array[bonds_id_array == old_index] = new_index

    # Clean the bond name array from hydrogens
    cleaned_bonds_id_array = []
    cleaned_bonds_names_array = []

    for i, pair in enumerate(bonds_name_array):
        a, b = pair
        if 'H' not in a and 'H' not in b:
            cleaned_bonds_id_array.append(bonds_id_array[i])
            cleaned_bonds_names_array.append(pair)

    cleaned_bonds_id_array = np.array(cleaned_bonds_id_array)
    cleaned_bonds_names_array = np.array(cleaned_bonds_names_array)

    # Construct the bond array by id
    nonH_bonds_id_array = np.copy(cleaned_bonds_id_array)

    for old_index, new_index in nonH_id_dict.items():
        nonH_bonds_id_array[cleaned_bonds_id_array == old_index] = new_index

    nonH_bonds_id_array = [(a, b) for a, b in nonH_bonds_id_array]

    # Generate the dictionaries
    heavy_atoms = {
    'names': cleaned_bonds_names_array,
    'ids': np.array(nonH_bonds_id_array),
    'old_ids': cleaned_bonds_id_array,
    }

    all_atoms = {
    'names': bonds_name_array,
    'ids': bonds_id_array,
    }

    return all_atoms, heavy_atoms

# ------------------------------
# Get bonded atoms from the list
def _get_bonded_atoms(molecule_bonds, atom):

    # Keep bonds including the reference atom only
    bonds = [(x,y) for x,y in molecule_bonds if (x == atom)|(y == atom)]

    # Keep atoms different from the reference atom
    bonded_atoms = []
    for x,y in bonds:
        if x == atom: bonded_atoms.append(y)
        else: bonded_atoms.append(x)

    return bonded_atoms

# ---------------------------------------------------------------
# Create the mask array for distance calculation at the n-th rank
def _generate_distance_list(molecule_bonds , neighbor_rank=6):

    # Calculate the number of atoms
    number_atoms = np.amax(molecule_bonds)

    # Build the ranked neighbor dictionnary for each atom
    neighbor_dictionnary = {} # Ranked neighbors dictionnary
    recorded_neighbors = {} # Dictionnary to avoid duplicates in the map ie an atom counting itself

    # Scan the molecule until the required rank is reached
    for i in range(1, neighbor_rank + 1):

        # Loop over all the atoms
        for atom in range(number_atoms):

            # Initialize the dictionnaries
            if atom not in neighbor_dictionnary.keys():
                neighbor_dictionnary[atom] = {}
                recorded_neighbors[atom] = []

            # First rank
            if i == 1:
                new_neighbors = _get_bonded_atoms(molecule_bonds, atom)
                neighbor_dictionnary[atom][i] = new_neighbors.copy()  # Append the list of neighbors to the dictionary
                recorded_neighbors[atom] = new_neighbors.copy()

            # Higher ranks
            else:
                lower_rank_neighbors = neighbor_dictionnary[atom][i - 1]
                higher_rank_neighbors = []

                # Save all the new neighbors
                for neighbor in lower_rank_neighbors:
                    new_rank_neighbors = [x for x in _get_bonded_atoms(molecule_bonds, neighbor) if (x != atom) & (x not in recorded_neighbors[atom])]

                    for new_neighbors in new_rank_neighbors:
                        higher_rank_neighbors.append(new_neighbors)
                        recorded_neighbors[atom].append(new_neighbors)

                neighbor_dictionnary[atom][i] = higher_rank_neighbors

    # Build the list from the dictionnary
    distance_list = []

    for atom in range(number_atoms):

        atom_neighbors = neighbor_dictionnary[atom][neighbor_rank]

        # Remove duplicates, ie A-B and B-A
        atom_to_save = []
        for neighbors in atom_neighbors:
            if sorted((atom,neighbors)) not in distance_list:
                distance_list.append( sorted((atom,neighbors)) )

    return np.array(distance_list)

# ---------------------------------------------
# Generate the list of pairs at a specific rank
def listPairs(type_info, rank=6):

    """Create the pair of lists at the specified rank
    Argument(s):
        type_info {dict} -- Dictionary containing all the informations on the molecule type. Can be extracted with read_simulation.getMolInfos()
        rank {int} -- Number of atoms (-1) between two neighbours along the same line used for distance calculations. At rank 1, the neighbours of an atom are all atom sharing a direct bond with it.
                      Default is 6.
    Output(s):
        ranked_bonds_ids {np.ndarray} -- Array containing all the distance pairs at a specific rank. Dimension(s) are in (n_distances, 2).
    """

    # Get the bonds
    bonds = type_info['heavy_atoms']['bonds']['ids']

    # Generate the map at the given rank
    ranked_bonds_ids = _generate_distance_list(bonds, neighbor_rank=rank)

    return ranked_bonds_ids

##-\-\-\-\-\-\-\-\-\-\-\-\
## CALCULATE THE DISTANCES
##-/-/-/-/-/-/-/-/-/-/-/-/

# -------------------------------------
# Compute the distances at a given rank
def computeDistances(positions, ranked_bonds_ids):

    """Compute all the distances using the map
    Argument(s):
        positions {np.ndarray} -- Array of the positions of the atoms of the molecules. Dimension(s) should be in (n_frames, n_molecules, n_atoms_per_molecule, 3).
        ranked_bonds_ids {np.ndarray} -- Array containing all the distance pairs at a specific rank. Dimension(s) should be in (n_distances, 2).
    Output(s):
        distances {np.ndarray} -- Array of the distances of the atoms of the molecules. Dimension(s) are in (n_frames, n_molecules, n_distances).
    """

    # Reshape the position array
    moleculeNbr = positions.shape[1]
    atomNbr = positions.shape[2]
    positions = np.reshape(positions, (positions.shape[0], moleculeNbr*atomNbr, 3))

    # Loop over all the frames
    all_distances = []
    for frame in tqdm(range(positions.shape[0]), desc='Computing distances...'):

        # Loop over all the distance pairs
        a = arange(0)
        b = arange(0)
        for (i, j) in ranked_bonds_ids:
            a = hstack((a, (i + arange(moleculeNbr) * atomNbr)))
            b = hstack((b, (j + arange(moleculeNbr) * atomNbr)))

        # Calculate the distances and return the resulting array
        vectdist = (positions[frame][a] - positions[frame][b])

        all_distances.append( (vectdist ** 2).sum(axis=1) ** 0.5 )

    # Reshape the distance array
    all_distances = np.array(all_distances)
    all_distances = np.reshape(all_distances, (all_distances.shape[0], ranked_bonds_ids.shape[0], moleculeNbr))
    all_distances = np.swapaxes(all_distances, 1,2)

    return all_distances
