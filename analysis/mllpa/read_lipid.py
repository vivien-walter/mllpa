#!/usr/bin/env python

import pickle
import numpy as np
import MDAnalysis as md
from tqdm import tqdm

import mllpa.lipid_state as lipid_state

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## General lists for the analysis
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

list_lipid_type = ['DPPC']
list_solvent_type = ['SOL']

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Functions specific to this script
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# Get the array containing all atoms masses and the length of the residue
def get_mass_array(selection):
	mass_array = []
	name_array = []
	type_array = []
	for atom in selection:
		mass_array.append(atom.mass)
		name_array.append(atom.name)
		type_array.append(atom.type)

	return np.array(mass_array), np.array(name_array), type_array, len(mass_array)

# Calculate the center of mass of the molecule
def get_com(atom_positions, atom_masses):
	return np.sum( (atom_positions * atom_masses[:,None]), axis=0 ) / sum(atom_masses)

# Generate a ghost of the lipid COM for 3D Voronoi tessellation
def get_ghost(lipid, positions, leaflet = None):
	if leaflet is None:
		leaflet = lipid.leaflet[-1]

	ghost_x, ghost_y = lipid.com[-1][0:2]
		
	if leaflet == 'top':
		ghost_z = lipid.com[-1][2] + 2*( max(positions[:,2]) - lipid.com[-1][2] )
	else:
		ghost_z = lipid.com[-1][2] - 2*( lipid.com[-1][2] - min(positions[:,2]) )

	lipid.ghost.append( [ghost_x, ghost_y, ghost_z] )

# Correct any PBC problem by shifting all the COM within the system box
def get_com_inbox(molecule, box_size):
	com_x, com_y = molecule.com[-1][0:2]
	new_com_z = molecule.com[-1][2]

	if com_x < 0.0:
		new_com_x = com_x + box_size[0]
	elif com_x > box_size[0]:
		new_com_x = com_x - box_size[0]
	else:
		new_com_x = com_x

	if com_y < 0.0:
		new_com_y = com_y + box_size[1]
	elif com_y > box_size[1]:
		new_com_y = com_y - box_size[1]
	else:
		new_com_y = com_y

	molecule.com_inbox.append([new_com_x, new_com_y, new_com_z])

	if 'ghost' in molecule.__dict__.keys():
		new_ghost_z = molecule.ghost[-1][2]
		molecule.ghost_inbox.append([new_com_x, new_com_y, new_ghost_z])

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Classes to store informations of the system
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# Class to hold the informations of each lipids
class lipid():
	def __init__(self, resname, resid, com, indices, center, state):
		# Generic informations
		self.name = resname
		self.id = resid
		self.indices = indices
		self.state = [state]

		# Position informations
		if com[2] < center:
			self.leaflet = ['bottom']
		else:
			self.leaflet = ['top']

		self.com = [com]
		self.com_inbox = []

		# Ghost COM for 3D Voronoi
		self.ghost = []
		self.ghost_inbox = []

# Class to hold the informations of each other types of molecules
class molecule():
	def __init__(self, resname, resid, com, indices):
		# Generic informations
		self.name = resname
		self.id = resid
		self.indices = indices

		# Position informations
		self.com = [com]

# Class to hold the informations of the system
class system():
	# Analyse the initial system
	def __init__(self, topology):

		self.topology_file = topology
		self.trajectory_file = None

		universe = self.get_universe(self.topology_file)

		# Save the informations of the simulation
		self.number_frames = 1
		self.first_frame = 1
		self.last_frame = 1
		self.skipped_frames = 0
		self.box_size = [universe.dimensions[0:3]]

		# Get list of molecules
		self.residue_types_info = {}
		self.residue_list = []

		# Read all residues
		print('Reading residues from the topology file...')

		temp_selection = universe.select_atoms('all')
		self.membrane_center = [ np.mean(universe.select_atoms('name P').positions[:,2]) ]

		for res_info in tqdm( universe.residues ):
			temp_resname = str(res_info).split(' ')[1].split(',')[0]
			temp_resid = int( str(res_info).split(' ')[2].split('>')[0] )

			if temp_resname not in list_solvent_type:
				# Extract the list of different molecule types in the simulation
				if temp_resname not in self.residue_types_info.keys(): 
					temp_atoms = universe.select_atoms('resid '+str(temp_resid))
					temp_mass, temp_names, temp_types, temp_length = get_mass_array( temp_atoms ) 

					self.residue_types_info[temp_resname] = {'first_id':temp_resid , 'mass':temp_mass, 'length': temp_length,'name':temp_names, 'type':temp_types,'all_id': [temp_resid] }
				else:
					self.residue_types_info[temp_resname]['all_id'].append(temp_resid)

				# Extract the position and com of the residue
				temp_indices = ( (temp_resid - 1)*self.residue_types_info[temp_resname]['length'], temp_resid*self.residue_types_info[temp_resname]['length'] )
				temp_position = temp_selection.positions[temp_indices[0]:temp_indices[1]]
	
				temp_com = get_com(temp_position, self.residue_types_info[temp_resname]['mass'])

				# Save the residue in an object
				temp_atoms = universe.select_atoms('resid '+str(temp_resid))
				if temp_resname in list_lipid_type:					
					temp_position_nonH = temp_position[np.array(temp_types) != 'H']
					temp_name_nonH = np.array(temp_names)[np.array(temp_types) != 'H']
					temp_state = lipid_state.get_state(temp_resname,dict(zip(temp_name_nonH,temp_position_nonH)), temp_position[np.array(temp_types) != 'H'])

					temp_object = lipid(temp_resname,temp_resid, temp_com, temp_indices, self.membrane_center[0], temp_state)
					get_ghost(temp_object, temp_position)

				else:
					temp_object = molecule(temp_resname,temp_resid, temp_com, temp_indices)
					
				get_com_inbox(temp_object, self.box_size[0])

				self.residue_list.append([temp_resid,temp_resname, temp_object])

		self.residue_list = np.array(self.residue_list)

	# Get the universe from the simulation files
	def get_universe(self, topology, trajectory = None):
		if trajectory is None:
			universe = md.Universe(topology)
		else:
			universe = md.Universe(topology, trajectory)

		return universe

	# Get the list of lipids from the system
	def get_lipid_list(self):
		return self.residue_list[:,2][np.isin(self.residue_list[:,1], list_lipid_type)]

	# Get the list of non-lipids and non-solvent molecules from the system
	def get_other_list(self):
		temp_mask = (np.isin(self.residue_list[:,1], list_lipid_type)) | (np.isin(self.residue_list[:,1], list_solvent_type))
		return self.residue_list[:,2][~temp_mask]

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Main functions of the script
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# Extract the COM of the lipids and of the other molecules in all frames
def get_trajectory(topology_file, output_filename, trajectory_file = None, begin=1, end=None, skip=0):
	# Extract the general data in the topology file
	print('Opening '+topology_file)
	crt_system = system( topology_file )
	print(' ')

	# Append all the frames of the trajectory
	if trajectory_file is not None:
		crt_system.trajectory_file = trajectory_file
		crt_universe = crt_system.get_universe(topology_file, trajectory_file)

		max_frame = len(crt_universe.trajectory)
		if int(begin) < 0:
			begin = 0
		else:
			begin = int(begin) -1 

		if end is None:
			end = max_frame
		else:
			end = int(end)

		crt_system.number_frames = 0
		crt_system.first_frame = begin
		crt_system.last_frame = end
		crt_system.skipped_frames = int(skip)
		crt_system.box_size = []
		crt_system.membrane_center = []

		# Reinitialize properties
		for residue in crt_system.residue_list:
			temp_object = residue[2]
			temp_object.com = []
			temp_object.com_inbox = []

			if hasattr(temp_object, 'state'):
				temp_object.state = []
				temp_object.leaflet = []
				temp_object.ghost = []
				temp_object.ghost_inbox = []

		# Extract the informations slide by slide
		print('Appending '+str(crt_system.number_frames-1)+' frames from '+trajectory_file+' (skipping every '+str(crt_system.skipped_frames)+' frames)')

		temp_selection = crt_universe.select_atoms('all')
		for frame_number in tqdm( range(crt_system.first_frame,crt_system.last_frame,crt_system.skipped_frames+1) ):
			temp_frame = crt_universe.trajectory[frame_number]
			crt_system.number_frames += 1 
			temp_x,temp_y,temp_z = temp_frame.dimensions[0:3]
			
			# Get general properties
			crt_system.box_size.append([temp_x,temp_y,temp_z])
			crt_system.membrane_center.append( np.mean(crt_universe.select_atoms('name P').positions[:,2]) )

			# Scan all residues
			for residue in crt_system.residue_list:
				temp_object = residue[2]

				temp_position = temp_selection.positions[temp_object.indices[0]:temp_object.indices[1]]
				temp_com = get_com(temp_position,crt_system.residue_types_info[residue[1]]['mass'])
				temp_object.com.append( temp_com )

				# Lipid specific informations
				if residue[1] in list_lipid_type:
					temp_names = crt_system.residue_types_info[residue[1]]['name']
					temp_types = crt_system.residue_types_info[residue[1]]['type']

					temp_position_nonH = temp_position[np.array(temp_types) != 'H']
					temp_name_nonH = np.array(temp_names)[np.array(temp_types) != 'H']
					temp_state = lipid_state.get_state(residue[1],dict(zip(temp_name_nonH,temp_position_nonH)), temp_position[np.array(temp_types) != 'H'])

					temp_object.state.append(temp_state)

					if temp_com[2] < crt_system.membrane_center[-1]:
						temp_object.leaflet.append('bottom')
					else:
						temp_object.leaflet.append('top')

					get_ghost(temp_object, temp_position)

				get_com_inbox(temp_object, [temp_x,temp_y,temp_z])

		print(' ')

	# Save the result in a file
	output_filename += '_system.com'
	pickle.dump(crt_system, open(output_filename,'wb'))

	print('Simulation successfully saved in '+output_filename)
