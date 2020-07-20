#!/usr/bin/env python

import os
import sys
import numpy as np
from tqdm import tqdm
import pickle

import mllpa.general_functions as general_functions

##-\-\-\-\-\-\-\-\
## Predict frontier
##-/-/-/-/-/-/-/-/

def read_frame_frontier(system, lipid_list, output_file, frame=0):
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

	os.system('python2 voronoi.py temp_top.info frontier '+str(system.box_size[frame][0])+' '+str(system.box_size[frame][1]))
	os.system('python2 voronoi.py temp_bottom.info frontier '+str(system.box_size[frame][0])+' '+str(system.box_size[frame][1]))

	# Get the area from Python2
	all_neigh = {}
	top_info = open('temp_top.info','r')
	for line in top_info:
		temp_neighbours = line.strip().split('\t')[1].split('-')
		all_neigh[str(line.strip().split('\t')[0])] = [[j.state[frame] for j in lipid_list if j.id == int(x)][0] for x in temp_neighbours]

	os.system('rm temp_top.info')

	bottom_info = open('temp_bottom.info','r')
	for line in bottom_info:
		temp_neighbours = line.strip().split('\t')[1].split('-')
		all_neigh[str(line.strip().split('\t')[0])] = [[j.state[frame] for j in lipid_list if j.id == int(x)][0] for x in temp_neighbours]

	os.system('rm temp_bottom.info')

	# Sort the area between phases
	gel_phase = []
	fluid_phase = []

	gel_nbr = 0
	gel_frontier_nbr = 0
	fluid_nbr = 0
	fluid_frontier_nbr = 0

	for lipid in lipid_list:
		temp_neigh_state = all_neigh[str(lipid.id)]
		if lipid.state[frame] == 'gel':
			nbr_fluid = temp_neigh_state.count('fluid')
			if nbr_fluid >= 2:
				lipid.state[frame] = 'gel-frontier'
				gel_frontier_nbr += 1
			else:
				gel_nbr += 1
		else:
			nbr_gel = temp_neigh_state.count('gel')
			if nbr_gel >= 2:
				lipid.state[frame] = 'fluid-frontier'
				fluid_frontier_nbr += 1
			else:
				fluid_nbr += 1

	# Save the 2D coordinates
	outfile_top = open(output_file+'_2d/'+output_file+'_top_'+str(frame)+'_'+str(system.box_size[frame][0])+'.txt','w')
	outfile_bottom = open(output_file+'_2d/'+output_file+'_bottom_'+str(frame)+'_'+str(system.box_size[frame][0])+'.txt','w')
	for lipid in lipid_list:
		if lipid.leaflet[frame] == 'top':
			outfile_top.write( str(lipid.id)+' '+str(lipid.com_inbox[frame][0])+' '+str(lipid.com_inbox[frame][1])+' 0.0 '+lipid.state[frame]+'\n' )
		else:
			outfile_bottom.write( str(lipid.id)+' '+str(lipid.com_inbox[frame][0])+' '+str(lipid.com_inbox[frame][1])+' 0.0 '+lipid.state[frame]+'\n' )
			
	outfile_top.close()
	outfile_bottom.close()

	# Save the 3D coordinates
	outfile = open(output_file+'_3d/'+output_file+'_'+str(frame)+'_'+str(system.box_size[frame][0])+'_'+str(system.box_size[frame][2])+'.txt','w')
	for lipid in lipid_list:
		outfile.write( str(lipid.id)+' '+str(lipid.com_inbox[frame][0])+' '+str(lipid.com_inbox[frame][1])+' '+str(lipid.com_inbox[frame][2])+' '+lipid.state[frame]+'\n' )
		outfile.write( str(lipid.id+1000)+' '+str(lipid.ghost_inbox[frame][0])+' '+str(lipid.ghost_inbox[frame][1])+' '+str(lipid.ghost_inbox[frame][2])+' '+lipid.state[frame]+'\n' )
	outfile.close()

	return gel_nbr, fluid_nbr, gel_frontier_nbr, fluid_frontier_nbr

##-\-\-\-\-\-\-\-\
## System analysis
##-/-/-/-/-/-/-/-/

def multiple_predict_frontier(system, lipid_list, output_file):
	lipid_number = len(lipid_list)

	os.system('mkdir '+output_file+'_2d')
	os.system('mkdir '+output_file+'_3d')

	# Loop on all frames
	gel_ratio = []
	gel_frontier_ratio = []
	fluid_ratio = []
	fluid_frontier_ratio = []

	for i in tqdm(range(0,system.number_frames)):
		gel_nbr, fluid_nbr, gel_frontier_nbr, fluid_frontier_nbr = read_frame_frontier(system, lipid_list, output_file, i)

		gel_ratio.append( gel_nbr* 100 /lipid_number  )
		fluid_ratio.append( fluid_nbr* 100 /lipid_number  )
		gel_frontier_ratio.append( gel_frontier_nbr* 100 /lipid_number  )
		fluid_frontier_ratio.append( fluid_frontier_nbr* 100 /lipid_number  )

	# Save the statistics
	statfile = open(output_file+'_frontier_stat.dat','w')
	statfile.write('frame\tgel\tfluid\tgel-frontier\tfluid-frontier\n')
	for i in range(0, len(gel_ratio)):
		statfile.write(str(i)+'\t'+str(gel_ratio[i])+'\t'+str(fluid_ratio[i])+'\t'+str(gel_frontier_ratio[i])+'\t'+str(fluid_frontier_ratio[i])+'\n')
	statfile.close()

	# Save the new system
	pickle.dump(system, open(output_file+'_frontier.com','wb'))

##-\-\-\-\-\-\-\
## Frame analysis
##-/-/-/-/-/-/-/

# Analysis on a single frame
def single_predict_frontier(system, lipid_list, output_file):
	lipid_number = len(lipid_list)

	os.system('mkdir '+output_file+'_2d')
	os.system('mkdir '+output_file+'_3d')

	# Loop on all frames
	gel_nbr, fluid_nbr, gel_frontier_nbr, fluid_frontier_nbr = read_frame_frontier(system, lipid_list, output_file, 0)

	# Display the statistics
	print("""
State ratio:
------------
Gel """+str(gel_nbr*100/lipid_number)+""" %
Fluid """+str(fluid_nbr*100/lipid_number)+""" %
Frontier """+str((gel_frontier_nbr+fluid_frontier_nbr)*100/lipid_number)+' %')

	# Save the new system and statistics
	statfile = open(output_file+'_frontier_stat.dat','w')
	temp_text = """
State ratio:
------------
Gel """+str(gel_nbr*100/lipid_number)+""" %
Fluid """+str(fluid_nbr*100/lipid_number)+""" %
Frontier """+str((gel_frontier_nbr+fluid_frontier_nbr)*100/lipid_number)+' %'
	statfile.write(temp_text)
	statfile.close()

	# Save the new system
	pickle.dump(system, open(output_file+'_frontier.com','wb'))

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Main functions of the script
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

def predict_frontier(system_file, output_file):
	system = pickle.load(open(system_file, 'rb'))
	lipid_list = system.get_lipid_list()

	if system.number_frames == 1:
		print('Running single frame analysis...')
		single_predict_frontier(system, lipid_list, output_file)
	else:
		print('Running multiple frame analysis')
		multiple_predict_frontier(system, lipid_list, output_file)
