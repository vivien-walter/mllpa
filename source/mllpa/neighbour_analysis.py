import numpy as np
from tess import Container
from tqdm import tqdm

from mllpa.interface_communication import _is_float, _is_string, _is_array, _error_input_type

##-\-\-\-\-\-\-\
## TESSELLATIONS
##-/-/-/-/-/-/-/

# ------------------------------------------
# Extract the vertices from the tessellation
def _get_vertices(cells):

    # Loop over all cells
    vertices_dictionnary = {}
    for cell in cells:
        vertices_dictionnary[cell.id] = cell.vertices()

    return vertices_dictionnary

#--------------------------------
# List the neighbors of each cell
def _get_neighbors(cells, threshold=.01):

    cell_ids = np.array([cell.id for cell in cells])

    # Loop over all cells
    neighbors_dictionnary = {}
    for cell in cells:

        # Get the different informations
        neighbors = np.array( cell.neighbors() )
        face_area = np.array( cell.face_areas() )

        # Remove the current cell from the list
        current_id = cell.id
        face_area = face_area[neighbors != current_id]
        neighbors = neighbors[neighbors != current_id]

        # Apply the threshold
        area_threshold = np.sum(face_area) * threshold
        neighbors = neighbors[face_area >= area_threshold]

        neighbors_dictionnary[current_id] = np.copy(neighbors)

    return neighbors_dictionnary

# ---------------------------------------
# Remove selected ids from neighbour list
def _clean_neighbours(neighbours, all_ids, accepted_ids):

    filtered_neighbours = [ x for x in neighbours if all_ids[x] in accepted_ids ]

    return filtered_neighbours

# -----------------------------------------
# Do the Voronoi tessellation of the system
def _3d_tessellations(center_of_masses, box, threshold=0.01):

    # Do the tessellation
    tessellation = Container(center_of_masses, limits=box, periodic=True)

    # Extract and refine the informations
    volumes = np.array([cell.volume() for cell in tessellation])
    vertices = _get_vertices(tessellation)
    neighbours = _get_neighbors(tessellation, threshold=threshold)

    return volumes, vertices, neighbours

# ---------------------------------
# Modify the input for a 2D Voronoi
def _2d_tessellations(center_of_masses, box, threshold=0.01):

    # Copy the input
    computed_COMs = np.copy(center_of_masses)
    computed_box = np.copy(box)

    # Modify the dimensions
    computed_COMs[:,2] = 0.5
    computed_box[2] = 1

    # Call the 3D tessellations
    volumes, vertices, neighbours = _3d_tessellations(computed_COMs, computed_box, threshold=threshold)

    return volumes, vertices, neighbours

# --------------------------------------
# Find the tessellations in a 2D bilayer
def _tessellation_bilayer(center_of_masses, boxes, ids, leaflets, threshold=0.01):

    # Process all the frames
    all_volumes = []
    all_vertices = []
    all_neighbours = []
    for frame in tqdm(range(center_of_masses.shape[0]), desc="Computing tessellations..."):

        # Extract the information of the current frame
        current_COMs = center_of_masses[frame]
        current_box = boxes[frame]
        current_leaflet = leaflets[frame]

        # Split the system in leaflets
        top_COMs = current_COMs[current_leaflet == 'top']
        top_ids = ids[current_leaflet == 'top']
        bottom_COMs = current_COMs[current_leaflet == 'bottom']
        bottom_ids = ids[current_leaflet == 'bottom']

        # Process each leaflet
        current_top_volumes, current_top_vertices, current_top_neighbours = _2d_tessellations(top_COMs, current_box, threshold=threshold)
        current_bottom_volumes, current_bottom_vertices, current_bottom_neighbours = _2d_tessellations(bottom_COMs, current_box, threshold=threshold)

        # Merge the leaflets
        current_volumes = np.zeros(current_leaflet.shape)
        current_volumes[current_leaflet == 'top'] = current_top_volumes
        current_volumes[current_leaflet == 'bottom'] = current_bottom_volumes
        all_volumes.append(current_volumes)

        # Save the vertices and neighbours
        current_vertices = {}
        current_neighbours = {}

        for i, id in enumerate(top_ids):
            current_vertices[id] = current_top_vertices[i]
            current_neighbours[id] = current_top_neighbours[i]

        for i, id in enumerate(bottom_ids):
            current_vertices[id] = current_bottom_vertices[i]
            current_neighbours[id] = current_bottom_neighbours[i]

        all_vertices.append(current_vertices)
        all_neighbours.append(current_neighbours)

    # Convert in array
    all_volumes = np.array(all_volumes)

    return all_volumes, all_vertices, all_neighbours

# -------------------------------------
# Find the tessellations in a 3D system
def _tessellation_3d_system(center_of_masses, boxes, ids, ghosts, threshold=0.01):

    # Merge the center of masses and ghosts
    all_objects = np.concatenate([center_of_masses, ghosts], axis=1)
    ghosts_ids = np.arange(1, ghosts.shape[1]+1) * -1
    all_ids = np.concatenate([ids, ghosts_ids])

    # Process all the frames
    all_volumes = []
    all_vertices = []
    all_neighbours = []
    for frame in tqdm(range(center_of_masses.shape[0]), desc="Computing tessellations..."):

        # Extract the information of the current frame
        current_positions = all_objects[frame]
        current_box = boxes[frame]

        # Perform the 3D tessellations
        current_volumes, current_vertices, current_neighbours = _3d_tessellations(current_positions, current_box, threshold=threshold)

        # Remove the ghosts from the volumes
        volumes = current_volumes[all_ids >= 0]
        all_volumes.append(volumes)

        # Save the vertices and neighbours
        vertices = {}
        neighbours = {}

        for i, id in enumerate(all_ids):
            if id >= 0:
                vertices[id] = current_vertices[i]
                neighbours[id] = _clean_neighbours(current_neighbours[i], all_ids, ids)

        all_vertices.append(vertices)
        all_neighbours.append(neighbours)

    # Convert in array
    all_volumes = np.array(all_volumes)

    return all_volumes, all_vertices, all_neighbours

# ----------------------------------------
# Find the tessellations in a "2D" vesicle
def _tessellation_vesicle(center_of_masses, boxes, ids, leaflets, ghosts, threshold=0.01):

    # Merge the center of masses and ghosts
    all_objects = np.concatenate([center_of_masses, ghosts], axis=1)
    ghosts_ids = np.arange(1, ghosts.shape[1]+1) * -1
    all_ids = np.concatenate([ids, ghosts_ids])

    # Process all the frames
    all_volumes = []
    all_vertices = []
    all_neighbours = []
    for frame in tqdm(range(center_of_masses.shape[0]), desc="Computing tessellations..."):

        # Extract the information of the current frame
        current_positions = all_objects[frame]
        current_box = boxes[frame]
        current_leaflets = leaflets[frame]

        # Get the IDs by leaflet
        inner_ids = ids[current_leaflets == 'inner']
        outer_ids = ids[current_leaflets == 'outer']

        # Perform the 3D tessellations
        current_volumes, current_vertices, current_neighbours = _3d_tessellations(current_positions, current_box, threshold=threshold)

        # Remove the ghosts from the volumes
        volumes = current_volumes[all_ids >= 0]
        all_volumes.append(volumes)

        # Save the vertices and neighbours
        vertices = {}
        neighbours = {}

        for i, id in enumerate(all_ids):
            if id >= 0:

                if id in inner_ids:
                    kept_ids = inner_ids
                else:
                    kept_ids = outer_ids

                vertices[id] = current_vertices[i]
                neighbours[id] = _clean_neighbours(current_neighbours[i], all_ids, kept_ids)

        all_vertices.append(vertices)
        all_neighbours.append(neighbours)

    # Convert in array
    all_volumes = np.array(all_volumes)

    return all_volumes, all_vertices, all_neighbours

# ---------------------------------------
# Find the tessellations in a 3d solution
def _tessellation_solution(center_of_masses, boxes, ids, leaflets, ghosts, threshold=0.01):

    # Merge the center of masses and ghosts
    all_objects = np.concatenate([center_of_masses, ghosts], axis=1)
    ghosts_ids = (np.copy(ids) * -1) - 1
    all_ids = np.concatenate([ids, ghosts_ids])
    inner_ids = ids[leaflets == 'inner']
    outer_ids = ids[leaflets == 'outer']

    # Process all the frames
    all_volumes = []
    all_vertices = []
    all_neighbours = []
    for frame in tqdm(range(center_of_masses.shape[0]), desc="Computing tessellations..."):

        # Extract the information of the current frame
        current_positions = all_objects[frame]
        current_box = boxes[frame]

        # Perform the 3D tessellations
        current_volumes, current_vertices, current_neighbours = _3d_tessellations(current_positions, current_box, threshold=threshold)

        # Remove the ghosts from the volumes
        volumes = current_volumes[all_ids >= 0]
        all_volumes.append(volumes)

        # Save the vertices and neighbours
        vertices = {}
        neighbours = {}

        for i, id in enumerate(all_ids):
            if id >= 0:

                if id in inner_ids:
                    kept_ids = inner_ids
                else:
                    kept_ids = outer_ids

                vertices[id] = current_vertices[i]
                neighbours[id] = _clean_neighbours(current_neighbours[i], all_ids, kept_ids)

        all_vertices.append(vertices)
        all_neighbours.append(neighbours)

    # Convert in array
    all_volumes = np.array(all_volumes)

    return all_volumes, all_vertices, all_neighbours

# ------------------------------------
# Find the tessellations in the system
def findTessellations(center_of_masses, boxes, ids, leaflets=None, ghosts=None, geometry='bilayer', threshold=0.01):

    # Check the input
    if not _is_string(geometry):
        _error_input_type('Geometry', str(str))
    if not _is_float(threshold):
        _error_input_type('Threshold', str(float))

    # Compute the tessellations in a 2D bilayer
    if geometry == 'bilayer':
        volumes, vertices, neighbours = _tessellation_bilayer(center_of_masses, boxes, ids, leaflets, threshold=threshold)

    # Compute the tessellations in a 3D bilayer or vesicle
    elif geometry == 'bilayer_3d' or geometry == 'vesicle_3d':
        volumes, vertices, neighbours = _tessellation_3d_system(center_of_masses, boxes, ids, ghosts, threshold=threshold)

    # Compute the tessellations in the leaflets of a vesicles
    elif geometry == 'vesicle':
        volumes, vertices, neighbours = _tessellation_vesicle(center_of_masses, boxes, ids, leaflets, ghosts, threshold=threshold)

    # Compute the tessellations in a solution
    elif geometry == 'solution':
        volumes, vertices, neighbours = _tessellation_solution(center_of_masses, boxes, ids, threshold=threshold)

    else:
        raise ValueError("The selected geometry is not valid.")

    return volumes, vertices, neighbours

##-\-\-\-\-\-\-\-\-\
## PROCESS NEIGHBOURS
##-/-/-/-/-/-/-/-/-/

# ------------------------------------------------------------------------
# Return the states of the neighbours of each molecule in the tessellation
def neighborStates(neighbours, states):

    # List all the available states
    states_list = np.unique(states)
    states_nbr = states_list.shape[0]

    # Read all the frames
    all_states = []
    for frame in tqdm(range(states.shape[0]), desc='Analysing the neighbors...'):

        # Get the current parameters
        current_states = states[frame]
        current_neighbors = neighbours[frame]

        # Read all the neighbors
        neighbors_states = []
        for mol_id in range(current_states.shape[0]):

            # Extract the states of the current molecule
            molecule_neighbours = current_neighbors[mol_id]
            molecule_states = current_states[molecule_neighbours]

            # Calculate the number of neighbors in each state
            neighbours_per_state = []
            for state_index in range(states_nbr):
                neighbours_per_state.append( molecule_states[molecule_states == states_list[state_index]].shape[0] )

            neighbors_states.append(neighbours_per_state)

        all_states.append(neighbors_states)

    # Convert in array
    all_states = np.array(all_states)

    return all_states, states_list

##-\-\-\-\-\-\
## GET LEAFLETS
##-/-/-/-/-/-/

# ------------------------------
# Find the leaflets in a bilayer
def _leaflets_bilayer(center_of_masses):

    # Find the Z position of the membrane mid-plane
    membrane_mid_plane = np.mean(center_of_masses, axis=1)[:,2]

    # Initialise the leaflets
    leaflets = np.zeros((center_of_masses.shape[0], center_of_masses.shape[1])).astype('U256')
    leaflets[:,:] = 'top'

    # Assign the leaflets
    leaflets[center_of_masses[:,:,2] < membrane_mid_plane[:,np.newaxis]] = 'bottom'

    return leaflets

# ------------------------------
# Find the leaflets in a vesicle
def _leaflets_vesicle(center_of_masses):

    # Find the center of the vesicle
    vesicle_center = np.mean(center_of_masses, axis=1)

    # Find the mean radius
    radii = np.mean( (center_of_masses - vesicle_center[:,np.newaxis,:])**2, axis=2 )
    mean_radius = np.mean(radii, axis=1)

    # Initialise the leaflets
    leaflets = np.zeros((center_of_masses.shape[0], center_of_masses.shape[1])).astype('U256')
    leaflets[:,:] = 'outer'

    # Assign the leaflets
    leaflets[radii < mean_radius[:,np.newaxis]] = 'inner'

    return leaflets

# -----------------------------
# Find the leaflets in bilayers
def findLeaflets(center_of_masses, geometry='bilayer'):

    # Check the input
    if not _is_array(center_of_masses):
        _error_input_type('Positions', str(np.ndarray))
    if not _is_string(geometry):
        _error_input_type('Geometry', str(str))

    # Find the leaflets in a bilayer
    if 'bilayer' in geometry:
        leaflets = _leaflets_bilayer(center_of_masses)

    # Find the leaflets in a vesicle
    elif 'vesicle' in geometry:
        leaflets = _leaflets_vesicle(center_of_masses)

    # Raise an error if there is an error
    else:
        raise ValueError("The selected geometry is not valid.")

    return leaflets

##-\-\-\-\-\
## GET GHOSTS
##-/-/-/-/-/

# ----------------------------
# Generate ghosts in a bilayer
def _ghosts_bilayer(center_of_masses, positions, ids, leaflets):

     # Calculate the min and max positions of the molecules
    min_position = np.amin(positions[:,:,:,2], axis=2)
    max_position = np.amax(positions[:,:,:,2], axis=2)

    # Isolate the molecules currently processed
    current_coms = center_of_masses[:,ids]
    current_leaflets = leaflets[:,ids]

    # Initialize the ghost array
    ghosts = np.copy(current_coms)
    ghosts[:,:,2] = 2*min_position - ghosts[:,:,2]

    # Replace the ghost
    ghost_mask = current_leaflets == 'top'
    ghosts[ghost_mask,2] = 2*max_position[ghost_mask] - np.copy(current_coms[ghost_mask,2])

    return ghosts

# ----------------------------
# Generate ghosts in a vesicle
def _ghosts_vesicles(center_of_masses, positions, ids, leaflets):

    # Find the center of the vesicle
    vesicle_center = np.mean(center_of_masses, axis=1)

    # Isolate the molecules currently processed
    current_coms = center_of_masses[:,ids]
    current_leaflets = leaflets[:,ids]

    # Calculate the vectors center-COMs and their norms
    vectors_COMs = current_coms - vesicle_center[:,np.newaxis,:]
    norms_COMs = np.linalg.norm(vectors_COMs, axis=2)

    # Calculate the shortest and longest vectors center-atoms for each molecule
    vectors_atoms = positions - vesicle_center[:, np.newaxis , np.newaxis , :]
    norms_atoms = np.linalg.norm(vectors_atoms, axis=3)
    shortest_norm = np.amin(norms_atoms, axis=2)
    longest_norm = np.amax(norms_atoms, axis=2)

    # Norm factors
    shortest_factor = (2 * shortest_norm / norms_COMs) - 1
    longest_factor = (2 * longest_norm / norms_COMs) - 1

    # Calculate the new vectors
    vectors_ghosts = np.copy(vectors_COMs) * shortest_factor[:,:,np.newaxis]
    vectors_ghosts[current_leaflets == 'outer'] = np.copy(vectors_COMs)[current_leaflets == 'outer'] * longest_factor[current_leaflets == 'outer',np.newaxis]

    # Calculate the positions of the ghosts
    ghosts = vesicle_center[:,np.newaxis,:] + vectors_ghosts

    return ghosts

# ---------------------------------
# Generate the ghosts for membranes
def generateGhosts(center_of_masses, positions, ids, leaflets, geometry='bilayer'):

    # Find the leaflets in a bilayer
    if 'bilayer' in geometry:
        ghosts = _ghosts_bilayer(center_of_masses, positions, ids, leaflets)

    # Find the leaflets in a vesicle
    elif 'vesicle' in geometry:
        ghosts = _ghosts_vesicles(center_of_masses, positions, ids, leaflets)

    # Raise an error if there is an error
    else:
        raise ValueError("The selected geometry is not valid.")

    return ghosts
