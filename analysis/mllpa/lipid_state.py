#!/usr/bin/env python

import os
import sys
import numpy as np
from tqdm import tqdm
import pickle

from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

import mllpa.general_functions as general_functions

##-\-\-\
## Models
##-/-/-/

# List of all the files with the models for machine learning
model_lists = {

# List models for the CHARMM forcefield
'charmm':{
'DPPC':'dppc_charmm_20180714.sav',
},
}

# Get the path to the file
def get_data(path):
	_ROOT = os.path.abspath(os.path.dirname(__file__))
	return os.path.join(_ROOT, 'model', path)

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Construction of the list of neighbors
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# Neighbor_list
neighbor_list = {

# List models for the CHARMM forcefield
'charmm':{
# Dictionnary for DPPC
'DPPC':{
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
'C316':['C315']},

},
}

# Generate the list of the neighbors per rank for the lipid
def get_neighbour_list(lipid, forcefield='charmm'):

	neighbor_rank = {}
	for atom in neighbor_list[forcefield][lipid].keys():
		ranked_neighbors = [[str(atom)]]
		prev_neigh = []

		temp_neighbors = neighbor_list[forcefield][lipid][atom]
		ranked_neighbors.append(temp_neighbors)

		for i in range(2, 26):
			temp_new_rank = []
			for neigh in temp_neighbors:
				temp_list = neighbor_list[forcefield][lipid][neigh]

				for elem in temp_list:
					if elem not in ranked_neighbors[-2]:
						temp_new_rank.append(elem)

			ranked_neighbors.append(temp_new_rank)
			temp_neighbors = temp_new_rank

		neighbor_rank[atom] = ranked_neighbors

	return neighbor_rank

# Measure the distances between neighbors
def measure_neighbors_distance(positions, neighbor_rank, rank = 6): # Value found for rank for DPPC on the 14/07/2018 by optimisation

	neighbor_distances = {}
	for atom in positions.keys():
		atom_name = str(atom)
		temp_position = positions[atom]

		ranked_neighbors = neighbor_rank[atom][rank]
		for neighbor in ranked_neighbors:
			both_name = [atom_name, str(neighbor)]
			distance_name = sorted(both_name)[0] + '-' + sorted(both_name)[1]

			if distance_name not in neighbor_distances:
				neighbor_position = positions[neighbor]
				neighbor_distances[distance_name] = general_functions.distance_3d( temp_position, neighbor_position )

	return neighbor_distances

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Rescale the positions of the lipid
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# Group lists
group_list = {

# List models for the CHARMM forcefield
'charmm':{
# Dictionnary for DPPC
'DPPC':{
'glyc':['C1', 'C2', 'C3', 'C21', 'C31'],
'tail1':['C2','C21', 'C22', 'O21', 'O22'],
'tail2':['C3','C31', 'C32', 'O31', 'O32'],

},
},

}

# Generic atom positions
atom_list = {

# List models for the CHARMM forcefield
'charmm':{
# Dictionnary for DPPC
'DPPC':['N', 'C12', 'C11', 'C29', 'C210', 'C211', 'C212', 'C213', 'C214', 'C215', 'C216', 'C39', 'C310', 'C311', 'C312', 'C313', 'C314', 'C315', 'C316']
},

}

# Fit the lipid inside a cylinder - find its vertical axis
def get_vertical_axis(position_array):
	lipid_center = position_array.mean(axis=0)
	uu, dd, vv = np.linalg.svd(position_array - lipid_center)

	return vv[0]

# Get the positions of the group to rescale the lipid
def get_group_positions(lipid_name, positions, forcefield='charmm'):
	coord_glyc = group_list[forcefield][lipid_name]['glyc']
	coord_list_tail1 = group_list[forcefield][lipid_name]['tail1']
	coord_list_tail2 = group_list[forcefield][lipid_name]['tail2']

	x_glyc = 0
	y_glyc = 0
	z_glyc = 0

	x_tail1 = 0
	y_tail1 = 0
	z_tail1 = 0

	x_tail2 = 0
	y_tail2 = 0
	z_tail2 = 0

	for atom in positions.keys():
		if str(atom) in coord_glyc:
			x_glyc += positions[atom][0]/5
			y_glyc += positions[atom][1]/5
			z_glyc += positions[atom][2]/5

		elif str(atom) in coord_list_tail1:
			x_tail1 += positions[atom][0]/5
			y_tail1 += positions[atom][1]/5
			z_tail1 += positions[atom][2]/5

		elif str(atom) in coord_list_tail2:
			x_tail2 += positions[atom][0]/5
			y_tail2 += positions[atom][1]/5
			z_tail2 += positions[atom][2]/5

	tail1 = [x_tail1, y_tail1, z_tail1]
	tail2 = [x_tail2, y_tail2, z_tail2]

	origin = np.array([x_glyc,y_glyc,z_glyc]) # Get the reference of the new set of coordinates for the rescaling
	x_vector = [x_tail2 - x_tail1, y_tail2 - y_tail1, z_tail2 - z_tail1]

	return origin, x_vector, tail1, tail2

# Shift and rotate the lipid to normalize its position in space
def do_rescale(lipid_name, positions, position_array, forcefield='charmm'): 

	# Get rescaled axis and vectors
	origin, x_vector, tail1, tail2 = get_group_positions(lipid_name, positions, forcefield)
	z_vector = get_vertical_axis(position_array)

	# Measure rotation
	zv_x_angle = -general_functions.vector_angle(z_vector, 'xy')
	zv_z_angle = -general_functions.vector_angle( general_functions.rotate_2d(z_vector, zv_x_angle, 'z'), 'zx' )

	temp_x_vector = general_functions.rotate_2d( general_functions.rotate_2d(x_vector, zv_x_angle, 'z'), zv_z_angle, 'y')

	xv_y_angle = -general_functions.vector_angle( temp_x_vector, 'xy' )

	# Rotate the lipid
	rescaled_positions = {}
	polar_positions = {}

	flip_state = False
	for atom in positions.keys():
		shifted_position = positions[atom] - origin
		rotation_1 = general_functions.rotate_2d( shifted_position, zv_x_angle, 'z' )
		rotation_2 = general_functions.rotate_2d( rotation_1, zv_z_angle, 'y' )
		rotation_3 = general_functions.rotate_2d( rotation_2, xv_y_angle, 'z' )

		if str(atom) == 'N':
			if rotation_3[2] < 0:
				flip_state = True

		if flip_state is True:
			rotation_3 = general_functions.rotate_2d( rotation_3, np.pi, 'x' )

		rescaled_positions[atom] = rotation_3
		polar_positions[atom] = np.sqrt( rotation_3[0]**2 + rotation_3[1]**2 )

	return rescaled_positions, polar_positions

##-\-\-\-\-\-\-\-\-\-\-\-\
## Predict the lipid state
##-/-/-/-/-/-/-/-/-/-/-/-/

def predict_state(rescaled_positions, polar_positions, neighbor_distances, model):

	# Prepare the parameters
	coord_set = []
	dist_set = []

	temp_coord = []
	for atom in rescaled_positions.keys():
		temp_coord.append(polar_positions[atom])
		temp_coord.append(rescaled_positions[atom][2])
	coord_set.append(temp_coord)

	temp_dist = []
	for key in neighbor_distances.keys():
		temp_dist.append(neighbor_distances[key])
	dist_set.append(temp_dist)

	coord_set = np.asarray(coord_set)
	dist_set = np.asarray(dist_set)

	# Get the models
	knn, svm_coord, nb, svm_dist = pickle.load(open(model, 'rb'))

	# Get the model predictions
	predictions_knn = knn.predict(coord_set)
	predictions_svm_coord = svm_coord.predict(coord_set)
	predictions_svm_dist = svm_dist.predict(dist_set)
	predictions_nb = nb.predict(dist_set)

	# Get the model final verification
	if predictions_knn[0] == predictions_svm_coord[0] and predictions_knn[0] == predictions_nb[0] and predictions_knn[0] == predictions_svm_dist[0] :
		lipid_state = predictions_knn[0]

	else:
		if predictions_svm_dist[0] == 'gel':
			lipid_state = predictions_svm_dist[0]
		elif predictions_svm_coord[0] == 'fluid':
			lipid_state = predictions_svm_coord[0]
		elif predictions_nb[0] == 'gel' :
			lipid_state = predictions_nb[0]
		else:
			lipid_state = predictions_svm_dist[0]

	return lipid_state

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Main functions of the script
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

def get_state(lipid_name, positions, position_array, forcefield='charmm'):
	# Get the rescaled positions
	rescaled_positions, polar_positions = do_rescale(lipid_name, positions, position_array, forcefield)

	# Get the intramolecular distances
	list_neighbors = get_neighbour_list(lipid_name, forcefield)
	neighbor_distances = measure_neighbors_distance(positions, list_neighbors)

	# Predict the lipid state
	model = get_data(model_lists[forcefield][lipid_name])
	lipid_state = predict_state(rescaled_positions, polar_positions, neighbor_distances, model)

	return lipid_state
