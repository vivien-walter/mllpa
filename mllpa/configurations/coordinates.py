import numpy as np
from tqdm import tqdm

from mllpa.interface_communication import _error_array_shape

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## OPERATIONS ON POSITIONS
##-/-/-/-/-/-/-/-/-/-/-/-/-/

# -----------------------------------------------
# Shift the molecules to center them on their COM
def _shift_molecules(positions, center_of_masses):

    # Reshape and repeat the COM array
    positionShape = positions.shape
    center_of_masses = np.reshape(center_of_masses, (positionShape[0], positionShape[1], 1, positionShape[3]))
    center_of_masses = np.repeat(center_of_masses, positionShape[2], axis=2)

    return positions - center_of_masses

#--------------------------------------------
# Compute the gyration tensor of the molecule
def _gyration_tensor(position, mass):

    # Calculate the weighted position array
    mass_array = np.tile(mass, (position.shape[0], 1))
    weighted_position = position * mass_array[:, :, np.newaxis]

    # Compute all the different elements
    xx = np.sum(weighted_position[:,:,0]*position[:,:,0], axis=1)
    xy = np.sum(weighted_position[:,:,0]*position[:,:,1], axis=1)
    xz = np.sum(weighted_position[:,:,0]*position[:,:,2], axis=1)
    yy = np.sum(weighted_position[:,:,1]*position[:,:,1], axis=1)
    yz = np.sum(weighted_position[:,:,1]*position[:,:,2], axis=1)
    zz = np.sum(weighted_position[:,:,2]*position[:,:,2], axis=1)

    # Assemble the elements
    gyration_tensors = np.swapaxes( np.vstack([xx,xy,xz,xy,yy,yz,xz,yz,zz]), 0, 1)

    return np.reshape(gyration_tensors, (gyration_tensors.shape[0],3,3)) / np.sum(mass)

#--------------------------------------
# Swap columns to sort the eigenvectors
def _swap_columns(eigenvectors, eigenvalues):

    # Initialize the new eigenvector matrix
    new_eigenvectors = np.zeros(eigenvectors.shape)

    # Get the index of the corresponding eigenvalue
    min_value = np.argmin(eigenvalues, axis=1)
    max_value = np.argmax(eigenvalues, axis=1)
    mid_value = (np.full(max_value.shape, 3) - (min_value + max_value)).astype(int)

    # Swap the positions
    for i in range(new_eigenvectors.shape[0]):
        new_eigenvectors[i,:,0] = eigenvectors[i,:,min_value[i]]
        new_eigenvectors[i,:,1] = eigenvectors[i,:,mid_value[i]]
        new_eigenvectors[i,:,2] = eigenvectors[i,:,max_value[i]]

    return new_eigenvectors

#------------------------------------------------------------------
# Check the orientation of the molecule and rotate them if required
def _check_orientation(positions, index=0):

    # Normalize the orientation of the molecule so the first atom is always in positive X Y and Z
    for i in range(0, 3):
        positions[positions[:,index,i] < 0.0, :, i] *= -1

    return positions

# -----------------------------------------------------
# Rotate all the molecules using the tensor of gyration
def _rotate_molecules(positions, masses, up=True):

    # Process all frames
    new_positions = []
    for frame in tqdm(positions, desc='Rotating molecules...'):

        # Compute all the gyration tensors
        gyration_tensor = _gyration_tensor(frame, masses)

        # Retrieve the eigenvalues and vectors
        eigenvalues, eigenvectors = np.linalg.eig(gyration_tensor)

        # Swap column in the eigenvectors matrix
        eigenvectors = _swap_columns(eigenvectors, eigenvalues)

        # Invert the eigenvectors matrix
        inverted_vectors = np.linalg.inv(eigenvectors)
        inverted_vectors = np.reshape(inverted_vectors, (inverted_vectors.shape[0], 1, 3, 3))
        inverted_vectors = np.repeat(inverted_vectors, frame.shape[1], axis=1)

        # Rotate the lipids
        corrected_positions = np.matmul(inverted_vectors, np.reshape(frame,(frame.shape[0], frame.shape[1],3,1)))
        corrected_positions = np.reshape(corrected_positions, (frame.shape[0], frame.shape[1],3))

        # Rotate the lipid further if required
        if up:
            corrected_positions = _check_orientation(corrected_positions)

        new_positions.append( np.copy(corrected_positions) )

    return np.array(new_positions)

##-\-\-\-\-\-\-\-\-\-\-\
## CONVERT THE POSITIONS
##-/-/-/-/-/-/-/-/-/-/-/

# ------------------------------------------
# Compute the center of mass of the molecule
def getCOM(positions, masses):

    """Compute the COM of the molecules. Only process similar molecule types to speed up the calculation process
    Argument(s):
        positions {np.ndarray} -- Array of the positions of the atoms of the molecules. Dimension(s) should be in (n_frames, n_molecules, n_atoms_per_molecule, 3).
        masses {np.ndarray} -- Array of the masses of the atoms of the molecule type. Dimension(s) should be in (n_atoms_per_molecule).
    Output(s):
        center_of_masses {np.ndarray} -- Array of the centers of mass of the molecules. Dimension(s) are in (n_frames, n_molecules, 3)
    """

    # Generate the arrays
    mass_array = np.tile(masses, (positions.shape[0], positions.shape[1], 1))

    weighted_positions = positions * mass_array[:,:,:, np.newaxis] # Multiply the position by the atomic weights

    return np.sum(weighted_positions, axis=2) / masses.sum()

# -----------------------------------------------------
# Centre and normalise the orientation of the molecules
def rotateMolecules(positions, type_info, up=True):

    """Normalise the orientation of the molecules after centering them on their COM
    Argument(s):
        positions {np.ndarray} -- Array of the positions of the atoms of the molecules. Dimension(s) should be in (n_frames, n_molecules, n_atoms_per_molecule, 3).
        type_info {dict} -- Dictionary containing all the informations on the molecule type. Can be extracted with read_simulation.getMolInfos()
        up {bool} -- Check that the molecules are always orientated facing "up"
    Output(s):
        new_positions {np.ndarray} -- Array of the corrected positions of the atoms of the molecules. Dimension(s) are in (n_frames, n_molecules, n_atoms_per_molecule, 3)
    """

    # Check the input array
    _error_array_shape(positions.shape, 4, "(n_frames, n_molecules, n_atoms, 3)")

    # Extract the masses
    atom_masses = type_info['heavy_atoms']['masses']

    # Compute the center of mass of the molecules
    molecule_coms = getCOM(positions, atom_masses)

    # Center the molecules
    centered_positions = _shift_molecules(positions, molecule_coms)

    # Rotate the molecules
    rotated_positions = _rotate_molecules(centered_positions, atom_masses, up=up)

    return rotated_positions

# -----------------------------------------------------
# Convert 3D cartesian coordinates to polar coordinates
def cartesian2Polar(positions):

    """Transform the 3D centered cartesian coordinates into 2D polar coordinates (dismissing the angle coordinates)
    Argument(s):
        positions {np.ndarray} -- Array of the cartesian positions of the atoms of the molecules. Dimension(s) should be in (n_frames, n_molecules, n_atoms_per_molecule, 3).
    Output(s):
        new_positions {np.ndarray} -- Array of the polar positions of the atoms of the molecules. Dimension(s) are in (n_frames, n_molecules, n_atoms_per_molecule, 2)
    """

    # Initialise the new set of coordinates
    polar_position = np.zeros((positions.shape[0], positions.shape[1], positions.shape[2], 2))

    # Calculate the position in the new set of coordinates
    polar_position[:,:,:, 0] = np.sqrt(positions[:,:,:, 0] ** 2 + positions[:,:,:, 1] ** 2)
    polar_position[:,:,:, 1] = positions[:,:,:, 2]

    return polar_position
