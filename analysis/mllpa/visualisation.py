#!/usr/bin/env python

import os
import sys
import numpy as np
from tqdm import tqdm
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image
import imageio

import mllpa.general_functions as general_functions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Generate image from matplotlib
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

def fig2data(fig):
	fig.canvas.draw()
	w,h = fig.canvas.get_width_height()
	buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
	buf.shape = ( w, h,4 )
 
	# canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
	buf = np.roll ( buf, 3, axis = 2 )
	return buf

def fig2img(fig):
	buf = fig2data(fig)
	w, h, d = buf.shape
	return Image.frombytes( "RGBA", ( w ,h ), buf.tostring( ) )

##-\-\-\-\-\-\-\-\
## Get tessellation
##-/-/-/-/-/-/-/-/

# 2 Dimensions
def read_frame_2d(output_file, system, lipid_list, frame=0):

	# Sent the informations into Python2
	top_info = open('temp_top.info','w')
	bottom_info = open('temp_bottom.info','w')
	lipid_state = {}
	for lipid in lipid_list:
		lipid_state[str(lipid.id)] = lipid.state[frame]

		if lipid.leaflet[frame] == 'top':
			top_info.write(str(lipid.id)+'\t'+str(lipid.com[frame][0])+'\t'+str(lipid.com[frame][1])+'\n')
		else:
			bottom_info.write(str(lipid.id)+'\t'+str(lipid.com[frame][0])+'\t'+str(lipid.com[frame][1])+'\n')
	top_info.close()
	bottom_info.close()

	os.system('python2 voronoi.py temp_top.info 2dview '+str(system.box_size[frame][0])+' '+str(system.box_size[frame][1]))
	os.system('python2 voronoi.py temp_bottom.info 2dview '+str(system.box_size[frame][0])+' '+str(system.box_size[frame][1]))

	# Get the vertices from Python2
	top_vertices = {}
	top_info = open('temp_top.info','r')
	for line in top_info:
		temp_vertices = []

		temp_id = str(line.strip().split('\t')[0])
		raw_vertices = line.strip().split('\t')[1::]

		for vertice in raw_vertices:
			temp_vertices.append( [float(vertice.split(',')[0][1::]),float(vertice.split(',')[1][0:-1])] )

		top_vertices[temp_id] = temp_vertices

	os.system('rm temp_top.info')

	bottom_vertices = {}
	bottom_info = open('temp_bottom.info','r')
	for line in bottom_info:
		temp_vertices = []

		temp_id = str(line.strip().split('\t')[0])
		raw_vertices = line.strip().split('\t')[1::]

		for vertice in raw_vertices:
			temp_vertices.append( [float(vertice.split(',')[0][1::]),float(vertice.split(',')[1][0:-1])] )

		bottom_vertices[temp_id] = temp_vertices

	os.system('rm temp_bottom.info')

	# Show the visualisation
	fig, axes = plt.subplots(ncols=2, sharex=True, sharey=True)

	for lipid in lipid_list:
		if lipid.leaflet[frame] == 'top':
			axis_number = 0
		else:
			axis_number = 1

		if lipid_state[str(lipid.id)] == 'gel':
			lipid_color = 'bo'
		elif lipid_state[str(lipid.id)] == 'fluid':
			lipid_color = 'ro'
		else:
			lipid_color = 'ko'

		axes[axis_number].plot(lipid.com[frame][0],lipid.com[frame][1], lipid_color, markersize=2)

	for lipid_key in top_vertices.keys():
		if lipid_state[str(lipid_key)] in ['gel','gel-frontier']:
			cell_color = 'b'
		else:
			cell_color = 'r'		

		polygon = top_vertices[lipid_key]
		axes[0].fill(*zip(*polygon), color=cell_color, alpha=.5)

	axes[0].set_title('Top')
	#axes[0].set_xlim(min_ax,max_ax)
	#axes[0].set_ylim(min_ax,max_ax)
	axes[0].get_xaxis().set_visible(False)
	axes[0].get_yaxis().set_visible(False)
	axes[0].set(adjustable='box-forced', aspect='equal')

	for lipid_key in bottom_vertices.keys():
		if lipid_state[str(lipid_key)] in ['gel','gel-frontier']:
			cell_color = 'b'
		else:
			cell_color = 'r'

		polygon = bottom_vertices[lipid_key]
		axes[1].fill(*zip(*polygon), color=cell_color, alpha=.5)

	axes[1].set_title('Bottom')
	#axes[1].set_xlim(min_ax,max_ax)
	#axes[1].set_ylim(min_ax,max_ax)
	axes[1].get_xaxis().set_visible(False)
	axes[1].get_yaxis().set_visible(False)
	axes[1].set(adjustable='box-forced', aspect='equal')

	fig2img(fig).save(output_file+'.png')
from skimage import io
# 3 Dimensions
def read_frame_3d(system, lipid_list, frame=0):

	# Sent the informations into Python2
	lipid_state = {}
	lipid_info = open('temp_system.info','w')
	for lipid in lipid_list:
		lipid_info.write(str(lipid.id)+'\t'+str(lipid.com[frame][0])+'\t'+str(lipid.com[frame][1])+'\t'+str(lipid.com[frame][2])+'\n')
		lipid_info.write(str(lipid.id+1000)+'\t'+str(lipid.ghost[frame][0])+'\t'+str(lipid.ghost[frame][1])+'\t'+str(lipid.ghost[frame][2])+'\n')
		lipid_state[str(lipid.id)] = lipid.state[frame]

	lipid_info.close()

	os.system('python2 voronoi.py temp_system.info 3dview '+str(system.box_size[frame][0])+' '+str(system.box_size[frame][1])+' '+str(system.box_size[frame][2]))

	# Get the vertices from Python2
	all_vertices = {}
	lipid_info = open('temp_system.info','r')
	for line in lipid_info:
		temp_vertices = []

		temp_id = str(line.strip().split('\t')[0])

		if int(temp_id) < 1000:
			raw_vertices = line.strip().split('\t')[1::]

			for vertice in raw_vertices:
				temp_vertices.append( [float(vertice.split(',')[0][1::]),float(vertice.split(',')[1]),float(vertice.split(',')[2][0:-1])] )

			all_vertices[temp_id] = temp_vertices

	os.system('rm temp_system.info')

	# Show the view
	fig = plt.figure()
	axis = Axes3D(fig)

	for lipid in lipid_list:
		if lipid_state[str(lipid.id)] == 'gel':
			lipid_color = 'b'
		else:
			lipid_color = 'r'

		axis.scatter(lipid.com[frame][0],lipid.com[frame][1],lipid.com[frame][2], c=lipid_color)

	plt.show()

##-\-\-\-\-\-\
## Read frames
##-/-/-/-/-/-/

# Read single frame
def read_single_view(output_file, system, lipid_list, dimension):
	if dimension == '2':
		read_frame_2d(output_file, system, lipid_list, 0)
	else:
		read_frame_3d(system, lipid_list, 0)

# Read multiple frames
def read_multiple_view(output_file, system, lipid_list, dimension):

	os.system('mkdir temp_'+output_file+'_gif')

	if dimension == '2':
		for i in tqdm(range(0,system.number_frames)):
			read_frame_2d('temp_'+output_file+'_gif/temp_'+str(i), system, lipid_list, i)

	all_images = []
	for i in range(0,system.number_frames):
		all_images.append( imageio.imread('temp_'+output_file+'_gif/temp_'+str(i)+'.png') )
	imageio.mimsave(output_file+'.gif', all_images)

	os.system('rm -r temp_'+output_file+'_gif')

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Main functions of the script
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

def show_membrane(system_file, output_file, dimension='2'):
	system = pickle.load(open(system_file, 'rb'))
	lipid_list = system.get_lipid_list()

	if system.number_frames == 1:
		print('Running single frame analysis...')
		read_single_view(output_file, system, lipid_list, dimension)
	else:
		print('Running multiple frame analysis')
		read_multiple_view(output_file, system, lipid_list, dimension)
