#!/usr/bin/env python

import os
import sys
import numpy as np
import pyvoro

##-\-\-\-\-\-\-\-\
## 2D visualisation
##-/-/-/-/-/-/-/-/

def view_2d(dataset_file, box_x, box_y):

	# Extract the informations from the file
	lipid_id = []
	lipid_com = []

	datafile = open(dataset_file,'r')
	for line in datafile:
		temp_line = line.strip().split('\t')
		lipid_id.append(temp_line[0])
		lipid_com.append( [float(temp_line[1]),float(temp_line[2])] )

	# Perform the Voronoi tessellation
	cells = pyvoro.compute_2d_voronoi( lipid_com,[[0.,box_x],[0.,box_y]],2.0, periodic=[True]*2 )

	# Save the results
	os.system('rm '+dataset_file)

	datafile = open(dataset_file,'w')
	for i, lipid in enumerate(lipid_id):

		textline = lipid
		for vertices in cells[i]['vertices']:
			textline += '\t' + str(vertices)
		textline += '\n'

		datafile.write( textline )
	datafile.close()

##-\-\-\-\-\-\-\-\
## 3D visualisation
##-/-/-/-/-/-/-/-/

def view_3d(dataset_file, box_x, box_y, box_z):

	# Extract the informations from the file
	lipid_id = []
	lipid_com = []

	datafile = open(dataset_file,'r')
	for line in datafile:
		temp_line = line.strip().split('\t')
		lipid_id.append(temp_line[0])
		lipid_com.append( [float(temp_line[1]),float(temp_line[2]),float(temp_line[3])] )

	# Perform the Voronoi tessellation
	cells = pyvoro.compute_voronoi( lipid_com,[[0.,box_x],[0.,box_y],[0.,box_z]],2.0, periodic=[True, True, False] )

	# Save the results
	os.system('rm '+dataset_file)

	datafile = open(dataset_file,'w')
	for i, lipid in enumerate(lipid_id):

		textline = lipid
		for vertices in cells[i]['vertices']:
			textline += '\t' + str(vertices)
		textline += '\n'

		datafile.write( textline )
	datafile.close()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Measure individual lipid area
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

def get_lipid_area(dataset_file, box_x, box_y):

	# Extract the informations from the file
	lipid_id = []
	lipid_com = []

	datafile = open(dataset_file,'r')
	for line in datafile:
		temp_line = line.strip().split('\t')
		lipid_id.append(temp_line[0])
		lipid_com.append( [float(temp_line[1]),float(temp_line[2])] )

	# Perform the Voronoi tessellation
	cells = pyvoro.compute_2d_voronoi( lipid_com,[[0.,box_x],[0.,box_y]],2.0, periodic=[True]*2 )

	# Save the results
	os.system('rm '+dataset_file)

	datafile = open(dataset_file,'w')
	for i, lipid in enumerate(lipid_id):
		datafile.write( lipid+'\t'+ str(cells[i]['volume'])+'\n' )
	datafile.close()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Predict if the lipid is at a frontier
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

def get_frontier(dataset_file, box_x, box_y):

	# Extract the informations from the file
	lipid_id = []
	lipid_com = []

	datafile = open(dataset_file,'r')
	for line in datafile:
		temp_line = line.strip().split('\t')
		lipid_id.append(temp_line[0])
		lipid_com.append( [float(temp_line[1]),float(temp_line[2])] )

	# Perform the Voronoi tessellation
	cells = pyvoro.compute_2d_voronoi( lipid_com,[[0.,box_x],[0.,box_y]],2.0, periodic=[True]*2 )

	# Save the results
	os.system('rm '+dataset_file)

	datafile = open(dataset_file,'w')
	for i, lipid in enumerate(lipid_id):
		temp_text = lipid+'\t'
		for neighbor in cells[i]['faces']:
			temp_text += str(lipid_id[neighbor['adjacent_cell']])+'-'

		datafile.write( temp_text[0:-1]+'\n' )
	datafile.close()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Main functions of the script
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

dataset_file = sys.argv[1]
analysis_type = sys.argv[2]
box_x = float(sys.argv[3])
box_y = float(sys.argv[4])

if analysis_type == 'lipid_area':
	get_lipid_area(dataset_file, box_x, box_y)
elif analysis_type == 'frontier':
	get_frontier(dataset_file, box_x, box_y)
elif analysis_type == '2dview':
	view_2d(dataset_file, box_x, box_y)
elif analysis_type == '3dview':
	box_z = float(sys.argv[5])
	view_3d(dataset_file, box_x, box_y, box_z)
