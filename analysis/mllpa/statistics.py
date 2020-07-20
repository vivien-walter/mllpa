#!/usr/bin/env python

import os
import sys
import numpy as np
from tqdm import tqdm
import pickle

import mllpa.general_functions as general_functions

##-\-\-\-\-\-\-\
## Frame analysis
##-/-/-/-/-/-/-/

# Analysis on a single frame
def get_frame_stats(system, lipid_list, lipid_number, frame=0):
	
	# Get state ratio
	gel_number = 0
	fluid_number = 0
	for lipid in lipid_list:
		temp_state = lipid.state[frame]
		if temp_state == 'gel':
			gel_number += 1
		else:
			fluid_number += 1

	# Get the area per lipid
	total_area = system.box_size[frame][0]*system.box_size[frame][1]/(lipid_number/2)
	
	# Sent the informations into Python2
	top_info = open('temp_top.info','w')
	bottom_info = open('temp_bottom.info','w')
	for lipid in lipid_list:
		if lipid.leaflet[frame] == 'top':
			top_info.write(str(lipid.id)+'\t'+str(lipid.com[frame][0])+'\t'+str(lipid.com[frame][1])+'\n')
		else:
			bottom_info.write(str(lipid.id)+'\t'+str(lipid.com[frame][0])+'\t'+str(lipid.com[frame][1])+'\n')
	top_info.close()
	bottom_info.close()

	os.system('python2 voronoi.py temp_top.info lipid_area '+str(system.box_size[frame][0])+' '+str(system.box_size[frame][1]))
	os.system('python2 voronoi.py temp_bottom.info lipid_area '+str(system.box_size[frame][0])+' '+str(system.box_size[frame][1]))

	# Get the area from Python2
	all_area = {}
	top_info = open('temp_top.info','r')
	for line in top_info:
		all_area[str(line.strip().split('\t')[0])] = float( line.strip().split('\t')[1] )

	os.system('rm temp_top.info')

	bottom_info = open('temp_bottom.info','r')
	for line in bottom_info:
		all_area[str(line.strip().split('\t')[0])] = float( line.strip().split('\t')[1] )

	os.system('rm temp_bottom.info')

	# Sort the area between phases
	gel_phase = []
	fluid_phase = []
	for lipid in lipid_list:
		if lipid.state[frame] == 'gel':
			gel_phase.append( all_area[str(lipid.id)] )
		else:
			fluid_phase.append( all_area[str(lipid.id)] )

	return [gel_number, fluid_number], total_area, [[np.mean(gel_phase),np.std(gel_phase)],[np.mean(fluid_phase),np.std(fluid_phase)]]

##-\-\-\-\-\-\-\-\-\-\
## Read all the frames
##-/-/-/-/-/-/-/-/-/-/

def multiple_frame_stats(system, lipid_list, output_file):
	lipid_number = len(lipid_list)

	# Read all frames
	gel_ratio = []
	fluid_ratio = []

	total_area = []
	gel_area = []
	gel_area_std = []
	fluid_area = []
	fluid_area_std = []

	for i in tqdm(range(0,system.number_frames)):
		temp_number, temp_total_area, temp_state_area = get_frame_stats(system, lipid_list, lipid_number, i)

		gel_ratio.append(temp_number[0]/lipid_number)
		fluid_ratio.append(temp_number[1]/lipid_number)

		total_area.append(temp_total_area)

		gel_area.append(temp_state_area[0][0])
		gel_area_std.append(temp_state_area[0][1])
		fluid_area.append(temp_state_area[1][0])
		fluid_area_std.append(temp_state_area[1][1])

	# Display all the results
	print("""
Number of lipids: """+str(lipid_number))

	print("""
State ratio:
------------
Gel """+str(np.mean(gel_ratio)*100)+' +/- '+str(np.std(gel_ratio)*100)+""" %
Fluid """+str(np.mean(fluid_ratio)*100)+' +/- '+str(np.std(fluid_ratio)*100)+' %')

	print("""
Area per lipid:
---------------
Total """+str(np.mean(total_area))+' +/- '+str(np.std(total_area))+' A^2')

	gel_avg_area = np.mean(gel_area)
	gel_std_area = np.sqrt( np.var(gel_area) + np.mean(np.array(gel_area_std)*np.array(gel_area_std)) )
	fluid_avg_area = np.mean(fluid_area)
	fluid_std_area = np.sqrt( np.var(fluid_area) + np.mean(np.array(fluid_area_std)*np.array(fluid_area_std)) )

	print('Gel '+str(gel_avg_area)+' +/- '+str(gel_std_area)+""" A^2
Fluid """+str(fluid_avg_area)+' +/- '+str(fluid_std_area)+' A^2')

	# Save all results in a file
	statfile = open(output_file+'_stat.dat','w')
	statfile.write('frame\tgel\tfluid\tarea\tgel area\terr gel area\tfluid area\terr fluid area\n')
	for i in range(len(gel_ratio)):
		statfile.write(str(i)+'\t'+str(gel_ratio[i]*100)+'\t'+str(fluid_ratio[i]*100)+'\t'+str(total_area[i])+'\t'+str(gel_area[i])+'\t'+str(gel_area_std[i])+'\t'+str(fluid_area[i])+'\t'+str(fluid_area_std[i])+'\n')
	statfile.close()

##-\-\-\-\-\-\-\-\-\-\
## Read a single frame
##-/-/-/-/-/-/-/-/-/-/

def single_frame_stats(system, lipid_list, output_file):

	# Read the stats
	lipid_number = len(lipid_list)
	state_number, total_area, state_area = get_frame_stats(system, lipid_list, lipid_number, frame=0)

	# Display the results
	print("""
Number of lipids: """+str(lipid_number))

	gel_ratio = state_number[0]/lipid_number
	fluid_ratio = state_number[1]/lipid_number

	print("""
State ratio:
------------
Gel """+str(gel_ratio*100)+""" %
Fluid """+str(fluid_ratio*100)+' %')

	print("""
Area per lipid:
---------------
Total """+str(total_area)+' A^2')

	gel_area = state_area[0]
	fluid_area = state_area[1]

	print('Gel '+str(gel_area[0])+' +/- '+str(gel_area[1])+""" A^2
Fluid """+str(fluid_area[0])+' +/- '+str(fluid_area[1])+' A^2')

	# Save all results in a file
	statfile = open(output_file+'_stat.dat','w')
	stat_text = """Number of lipids: """+str(lipid_number)+"""

State ratio:
------------
Gel """+str(gel_ratio*100)+""" %
Fluid """+str(fluid_ratio*100)+""" %

Area per lipid:
---------------
Total """+str(total_area)+""" A^2
Gel """+str(gel_area[0])+' +/- '+str(gel_area[1])+""" A^2
Fluid """+str(fluid_area[0])+' +/- '+str(fluid_area[1])+' A^2'

	statfile.write(stat_text)
	statfile.close()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Main functions of the script
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

def make_stats(system_file, output_file):
	system = pickle.load(open(system_file, 'rb'))
	lipid_list = system.get_lipid_list()

	if system.number_frames == 1:
		print('Running single frame analysis...')
		single_frame_stats(system, lipid_list, output_file)
	else:
		print('Running multiple frame analysis')
		multiple_frame_stats(system, lipid_list, output_file)
