#!/usr/bin/env python

# Import all required packages
#-----------------------------

import sys

from tqdm import tqdm

import numpy as np
import MDAnalysis as md

import matplotlib.pyplot as plt

# Generic informations
#---------------------

lipid_name = 'DPPC'
ranking = 6

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## User-defined dicitonaries
##-/-/-/-/-/-/-/-/-/-/-/-/-/

neighbor_list = {
# Choline
'N':['C13','C14','C15','C12'],
'C13':['N'],
'C14':['N'],
'C15':['N'],
'C12':['N', 'C11'],
'C11':['C12', 'O12'],
# Phosphate
'O12':['C11', 'P'],
'P':['O11','O12','O13','O14'],
'O13':['P'],
'O14':['P'],
'O11':['C1', 'P'],
# Glycerol
'C1':['O11','C2'],
'C2':['C1', 'O21','C3'],
'C3':['C2', 'O31'],
# Tail 1
'O21':['C2','C21'],
'C21':['O21','O22','C22'],
'O22':['C21'],
'C22':['C21','C23'],
'C23':['C22','C24'],
'C24':['C23','C25'],
'C25':['C24','C26'],
'C26':['C25','C27'],
'C27':['C26','C28'],
'C28':['C27','C29'],
'C29':['C28','C210'],
'C210':['C29','C211'],
'C211':['C210','C212'],
'C212':['C211','C213'],
'C213':['C212','C214'],
'C214':['C213','C215'],
'C215':['C214','C216'],
'C216':['C215'],
# Tail 2
'O31':['C3','C31'],
'C31':['O31','O32','C32'],
'O32':['C31'],
'C32':['C31','C33'],
'C33':['C32','C34'],
'C34':['C33','C35'],
'C35':['C34','C36'],
'C36':['C35','C37'],
'C37':['C36','C38'],
'C38':['C37','C39'],
'C39':['C38','C310'],
'C310':['C39','C311'],
'C311':['C310','C312'],
'C312':['C311','C313'],
'C313':['C312','C314'],
'C314':['C313','C315'],
'C315':['C314','C316'],
'C316':['C315']
}

##-\-\-\-\-\-\-\-\-\
## User-defined lists
##-/-/-/-/-/-/-/-/-/

coord_glyc = ['C1', 'C2', 'C3', 'C21', 'C31']
coord_list_tail1 = ['C2','C21', 'C22', 'O21', 'O22']
coord_list_tail2 = ['C3','C31', 'C32', 'O31', 'O32']
atom_list = ['N', 'C12', 'C11', 'C29', 'C210', 'C211', 'C212', 'C213', 'C214', 'C215', 'C216', 'C39', 'C310', 'C311', 'C312', 'C313', 'C314', 'C315', 'C316']

##-\-\-\-\-\-\-\-\-\-\-\
## User-defined functions
##-/-/-/-/-/-/-/-/-/-/-/

# Measure the angle between a vector and one of the coordinates axis
def vector_angle(u, plane='xy'): # Angle is measured regarding the first coordinate given

	# Transform vector u in 2d
	if plane == 'xy':
		u_2d = [u[0],u[1]]
	elif plane == 'xz':
		u_2d = [u[0],u[2]]
	elif plane == 'zy':
		u_2d = [u[2],u[1]]
	elif plane == 'zx':
		u_2d = [u[2],u[0]]

	v1 = [1.0,0.0]
	v2 = [0.0,1.0]

	angle = np.arccos( np.dot(u_2d,v1) / (np.linalg.norm(u_2d)) )
	angle_signed = np.arccos( np.dot(u_2d,v2) / (np.linalg.norm(u_2d)) )

	if angle_signed > np.pi/2 : # Check the sign of the angle according to the other axis of the plane
		angle = -angle

	return angle

# Rotate a 3D vector in a 2D plane
def rotate_2d(u, angle, axis):
	if axis == 'x': # Rotate around the x-axis
		new_matrix = [u[0], np.cos(angle)*u[1]-np.sin(angle)*u[2], np.sin(angle)*u[1]+np.cos(angle)*u[2]]
	elif axis == 'y': # Rotate around the y-axis
		new_matrix = [np.cos(angle)*u[0]+np.sin(angle)*u[2], u[1], -np.sin(angle)*u[0]+np.cos(angle)*u[2]]
	else: # Rotate around the z-axis
		new_matrix = [np.cos(angle)*u[0]-np.sin(angle)*u[1], np.sin(angle)*u[0]+np.cos(angle)*u[1], u[2]]

	return new_matrix

def distance_3d(a,b):
	return np.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2 )

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Class to store the informations about the lipids
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class lipid:
	def __init__(self, name, i, atoms, rank):
		self.name = name
		self.id = i
		self.raw_positions = {}
		self.neighbor_distances = {}
		self.rescaled_positions = {}
		self.polar_positions = {}

		# Start the two basic functions to get the positions of all atoms of the lipid and then rescale them
		self.get_positions(atoms)
		self.measure_neighbors_distance(rank)
		self.get_vertical_axis()
		self.get_group_positions()
		self.do_rescale()

		#self.check_positions()
		#self.show_lipid()

	def get_positions(self, atoms): # Get the position of all non-Hydrogen atoms
		self.position_array = []
		for atom in atoms:
			if atom.type != 'H':
				self.raw_positions[atom.name] = atom.position
				self.position_array.append(atom.position)

		self.position_array = np.array(self.position_array)

	def measure_neighbors_distance(self, rank):
		for atom in self.raw_positions.keys():
			atom_name = str(atom)
			temp_position = self.raw_positions[atom]

			ranked_neighbors = neighbor_rank[atom][rank]
			for neighbor in ranked_neighbors:
				both_name = [atom_name, str(neighbor)]
				distance_name = sorted(both_name)[0] + '-' + sorted(both_name)[1]

				if distance_name not in self.neighbor_distances:
					neighbor_position = self.raw_positions[neighbor]
					self.neighbor_distances[distance_name] = distance_3d( temp_position, neighbor_position )

	def get_vertical_axis(self):
		lipid_center = self.position_array.mean(axis=0)
		uu, dd, vv = np.linalg.svd(self.position_array - lipid_center)

		self.z_vector = vv[0]

	def get_group_positions(self):
		x_glyc = 0
		y_glyc = 0
		z_glyc = 0

		x_tail1 = 0
		y_tail1 = 0
		z_tail1 = 0

		x_tail2 = 0
		y_tail2 = 0
		z_tail2 = 0

		for atom in self.raw_positions.keys():
			if str(atom) in coord_glyc:
				x_glyc += self.raw_positions[atom][0]/5
				y_glyc += self.raw_positions[atom][1]/5
				z_glyc += self.raw_positions[atom][2]/5

			elif str(atom) in coord_list_tail1:
				x_tail1 += self.raw_positions[atom][0]/5
				y_tail1 += self.raw_positions[atom][1]/5
				z_tail1 += self.raw_positions[atom][2]/5

			elif str(atom) in coord_list_tail2:
				x_tail2 += self.raw_positions[atom][0]/5
				y_tail2 += self.raw_positions[atom][1]/5
				z_tail2 += self.raw_positions[atom][2]/5

		self.avg_tail1_position = [x_tail1, y_tail1, z_tail1]
		self.avg_tail2_position = [x_tail2, y_tail2, z_tail2]

		self.origin = np.array([x_glyc,y_glyc,z_glyc]) # Get the reference of the new set of coordinates for the rescaling
		self.x_vector = [x_tail2 - x_tail1, y_tail2 - y_tail1, z_tail2 - z_tail1]

	def do_rescale(self): # Shift and rotate the lipid to normalize its position in space

		self.rescaled_position_array = []

		self.zv_x_angle = -vector_angle(self.z_vector, 'xy')
		self.zv_z_angle = -vector_angle( rotate_2d(self.z_vector, self.zv_x_angle, 'z'), 'zx' )

		temp_x_vector = rotate_2d( rotate_2d(self.x_vector, self.zv_x_angle, 'z'), self.zv_z_angle, 'y')

		self.xv_y_angle = -vector_angle( temp_x_vector, 'xy' )

		flip_state = False

		for atom in self.raw_positions.keys():
			shifted_position = self.raw_positions[atom] - self.origin
			rotation_1 = rotate_2d( shifted_position, self.zv_x_angle, 'z' )
			rotation_2 = rotate_2d( rotation_1, self.zv_z_angle, 'y' )
			rotation_3 = rotate_2d( rotation_2, self.xv_y_angle, 'z' )

			if str(atom) == 'N':
				if rotation_3[2] < 0:
					flip_state = True

			if flip_state is True:
				rotation_3 = rotate_2d( rotation_3, np.pi, 'x' )

			self.rescaled_positions[atom] = rotation_3
			self.polar_positions[atom] = np.sqrt( rotation_3[0]**2 + rotation_3[1]**2 )
			self.rescaled_position_array.append(rotation_3)

		self.rescaled_position_array = np.array(self.rescaled_position_array)

	def check_positions(self):
		
		lipid_center = self.rescaled_position_array.mean(axis=0)
		uu, dd, vv = np.linalg.svd(self.rescaled_position_array - lipid_center)

		self.check_z = vv[0]

		x_glyc = 0
		y_glyc = 0
		z_glyc = 0

		x_tail1 = 0
		y_tail1 = 0
		z_tail1 = 0

		x_tail2 = 0
		y_tail2 = 0
		z_tail2 = 0

		for atom in self.rescaled_positions.keys():
			if str(atom) in coord_glyc:
				x_glyc += self.rescaled_positions[atom][0]/5
				y_glyc += self.rescaled_positions[atom][1]/5
				z_glyc += self.rescaled_positions[atom][2]/5

			elif str(atom) in coord_list_tail1:
				x_tail1 += self.rescaled_positions[atom][0]/5
				y_tail1 += self.rescaled_positions[atom][1]/5
				z_tail1 += self.rescaled_positions[atom][2]/5

			elif str(atom) in coord_list_tail2:
				x_tail2 += self.rescaled_positions[atom][0]/5
				y_tail2 += self.rescaled_positions[atom][1]/5
				z_tail2 += self.rescaled_positions[atom][2]/5

		self.check_tail1_position = [x_tail1, y_tail1, z_tail1]
		self.check_tail2_position = [x_tail2, y_tail2, z_tail2]
		
	def show_lipid(self):
		x_pos = []
		y_pos = []
		z_pos = []

		for atom in self.rescaled_positions.keys():
			x_pos.append(self.rescaled_positions[atom][0])
			y_pos.append(self.rescaled_positions[atom][1])
			z_pos.append(self.rescaled_positions[atom][2])

		plt.figure(1)
		plt.subplot(131)
		plt.plot(x_pos, z_pos, 'ko')
		plt.plot([self.check_tail1_position[0],self.check_tail2_position[0]],[self.check_tail1_position[2],self.check_tail2_position[2]],'g-')
		#plt.plot([self.check_head_position[0],self.check_tail_position[0]],[self.check_head_position[2],self.check_tail_position[2]],'r-')

		plt.subplot(132)
		plt.plot(y_pos, z_pos, 'ko')
		plt.plot([self.check_tail1_position[1],self.check_tail2_position[1]],[self.check_tail1_position[2],self.check_tail2_position[2]],'g-')
		#plt.plot([self.check_head_position[1],self.check_tail_position[1]],[self.check_head_position[2],self.check_tail_position[2]],'r-')

		plt.subplot(133)
		plt.plot(x_pos, y_pos, 'ko')
		plt.plot([self.check_tail1_position[0],self.check_tail2_position[0]],[self.check_tail1_position[1],self.check_tail2_position[1]],'g-')			
		#plt.plot([self.check_head_position[0],self.check_tail_position[0]],[self.check_head_position[1],self.check_tail_position[1]],'r-')
		
		plt.show()

##-\-\-\-\-\-\
## Begin script
##-/-/-/-/-/-/

# Generate the list of the neighbors per rank
print('Generating neighbors list...')

neighbor_rank = {}
for atom in tqdm(neighbor_list.keys()):
	ranked_neighbors = [[str(atom)]]
	prev_neigh = []

	temp_neighbors = neighbor_list[atom]
	ranked_neighbors.append(temp_neighbors)

	for i in range(2, 26):
		temp_new_rank = []
		for neigh in temp_neighbors:
			temp_list = neighbor_list[neigh]

			for elem in temp_list:
				if elem not in ranked_neighbors[-2]:
					temp_new_rank.append(elem)

		ranked_neighbors.append(temp_new_rank)
		temp_neighbors = temp_new_rank

	neighbor_rank[atom] = ranked_neighbors

# Get the distribution of neighbors per rank
print('Getting average neighbors number...')

neighbors_stats = []
for i in range(len(neighbor_rank['P'])):
	temp_nbr = []
	for atom in neighbor_rank.keys():
		temp_nbr.append(len(neighbor_rank[atom][i]))
	neighbors_stats.append([np.mean(temp_nbr),np.std(temp_nbr)])

statfile = open('dppc_neighbors_stats.dat','w')
statfile.write('rank, nbr_neighbors, std\n')
for i, stat in enumerate(neighbors_stats):
	text_to_write = str(i)+','+str(stat[0])+','+str(stat[1])+'\n'
	statfile.write(text_to_write)
statfile.close()

# Get the coordinates from the structure files

# Analyse the fluid file
fluid_lipids = []
for i in range(1,4):
	fluid_topol = md.Universe('fluid_'+str(i)+'.gro')
	for i in tqdm( range(1, len( fluid_topol.select_atoms('resname '+lipid_name).residues ) + 1) ):
		temp_selection = fluid_topol.select_atoms('resid '+str(i))
		fluid_lipids.append( lipid(lipid_name, i, temp_selection, ranking) )

# Analyse the gel file
gel_lipids = []

for i in range(1,4):
	gel_topol = md.Universe('gel_'+str(i)+'.gro')
	for i in tqdm( range(1, len( gel_topol.select_atoms('resname '+lipid_name).residues ) + 1) ):
		temp_selection = gel_topol.select_atoms('resid '+str(i))
		gel_lipids.append( lipid(lipid_name, i, temp_selection, ranking) )

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Machine learning - coordinates only
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

all_data = []

# Create parameter list
temp_list = []
for key in fluid_lipids[0].raw_positions.keys():
	#if str(key) in atom_list:
	temp_list.append(str(key)+'_r')
	#temp_list.append(str(key)+'_x')
	#temp_list.append(str(key)+'_y')
	temp_list.append(str(key)+'_z')
for key in fluid_lipids[0].neighbor_distances.keys():
	temp_list.append(str(key))
temp_list.append('class')
all_data.append(temp_list)

# Extract informations from the class
pointer = 0
for lipid in fluid_lipids:
	temp_list = []
	#temp_list = [pointer]
	for atom in lipid.rescaled_positions.keys():
		#if str(atom) in atom_list:
		temp_list.append(lipid.polar_positions[atom])
		#temp_list.append(lipid.rescaled_positions[atom][0])
		#temp_list.append(lipid.rescaled_positions[atom][1])
		temp_list.append(lipid.rescaled_positions[atom][2])
	for key in lipid.neighbor_distances.keys():
		temp_list.append(lipid.neighbor_distances[key])
	temp_list.append('fluid')
	all_data.append(temp_list)
	pointer += 1

for lipid in gel_lipids:
	temp_list = []
	#temp_list = [pointer]
	for atom in lipid.rescaled_positions.keys():
		#if str(atom) in atom_list:
		temp_list.append(lipid.polar_positions[atom])
		#temp_list.append(lipid.rescaled_positions[atom][0])
		#temp_list.append(lipid.rescaled_positions[atom][1])
		temp_list.append(lipid.rescaled_positions[atom][2])
	for key in lipid.neighbor_distances.keys():
		temp_list.append(lipid.neighbor_distances[key])
	temp_list.append('gel')
	all_data.append(temp_list)
	pointer += 1

#dataset = np.array(all_data)

# Save all data in a csv file
datafile = open('dataset_1.csv','w')
for line in all_data:
	text_to_write = ''
	for info in line[0:-1]:
		text_to_write += str(info) + ','
	text_to_write += str(line[-1]) + '\n'
	datafile.write(text_to_write)

datafile.close()
