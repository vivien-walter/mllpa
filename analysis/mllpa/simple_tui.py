#!/usr/bin/env python

import os
import sys
import datetime
import time
import glob
import readline

import MDAnalysis as md

import mllpa.read_lipid as read_lipid
import mllpa.statistics as statistics
import mllpa.extract_com as extract_com
import mllpa.visualisation as visualisation

##
##
##

all_topology_files = ['*.gro','*.pdb']
all_trajectory_files = ['*.trr','*.xtc']

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Functions specific to this script
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

def prefill_input(message, text):
	def hook():
		readline.insert_text(text)
		readline.redisplay()
	readline.set_pre_input_hook(hook)
	result = input(message)
	readline.set_pre_input_hook()
	return result

##-\-\-\-\-\-\-\-\-\-\
## Other TUI functions
##-/-/-/-/-/-/-/-/-/-/

def show_exit_message():
	now = datetime.datetime.now()
	print("""
================================================================
================================================================

Done! Script executed on the """+ str(now.strftime("%Y-%m-%d at %H:%M")) +"""

================================================================
================================================================
""")

##-\-\-\-\-\-\-\-\-\-\-\
## Read simulation files
##-/-/-/-/-/-/-/-/-/-/-/

def call_read_lipid_function(topology_file, trajectory_file = None):

	print("""
================================================================
================================================================
""")

	if trajectory_file is None:
		filename = topology_file.split('.')[-2]
		begin = '0' 
		end = None
		skip = '0'
	else:
		temp_universe = md.Universe(topology_file, trajectory_file)

		begin = '1' 
		end = str(len(temp_universe.trajectory))
		skip = '0'
		filename = trajectory_file.split('.')[-2]

		print('Processing '+str(end)+""" frames
""")

		begin = prefill_input('Begin at? (int) ', begin)
		end = prefill_input('End at? (int) ', end)
		skip = prefill_input('Skipped frames? (int) ', skip)

	filename = prefill_input('Output file name? ', filename)
		
	print("""
================================================================
================================================================
""")
	read_lipid.get_trajectory(topology_file, filename, trajectory_file, begin, end, skip)
	show_exit_message()

# Get trajectory file
def check_trajectory(topology_file, trajectory_list):
	read_trajectory = True

	while read_trajectory:
		print("""
Select trajectory file to read:
-------------------------------""")

		for file in trajectory_list:
			print(file)

		print("""
NONE to read the topology file only
RETURN to go the main menu
EXIT to leave the program
""")
		# Get the user choice
		trajectory_input = input("? ")

		if trajectory_input in trajectory_list:
			read_trajectory = False
			call_read_lipid_function(topology_file, trajectory_input)
								
		# Return to the previous menu
		elif trajectory_input.upper() == 'NONE':
			read_trajectory = False
			call_read_lipid_function(topology_file)

		# Return to the previous menu
		elif trajectory_input.upper() == 'RETURN':
			read_trajectory = False
			call_read_simulation()

		# Leave the script
		elif trajectory_input.upper() == 'EXIT':
			read_trajectory = False
			show_exit_message()

		# Display error message on wrong selection
		else:
			print("""
/!\ ERROR! The requested selection is not valid! /!\ """)

			time.sleep(2)

# Get topology file
def call_read_simulation():
	read_topology = True

	while read_topology:
		print("""
================================================================
================================================================

##########################################
ML-LPA readsim -- READING SIMULATION FILES
##########################################

Select topology file to read:
-----------------------------""")
	
		# Get the list of all topology files in the folder
		topology_list = []
		for file_type in all_topology_files:
			for file in glob.glob(file_type):
				topology_list.append(file)

		# Raise error if there is no topology file in the folder
		if not topology_list:
			print("""/!\ ERROR! No topology file can be found in the directory /!\ """)
			time.sleep(2)

			read_topology = False
			call_main_screen()

		else:	
			for file in topology_list:
				print(file)

			print("""
RETURN to go the main menu
EXIT to leave the program
""")
			# Get the user choice
			topology_input = input("? ")

			if topology_input in topology_list:

				# Check the existence of trajectory files			
				trajectory_list = []
				for file_type in all_trajectory_files:
					for file in glob.glob(file_type):
						trajectory_list.append(file)

				if not trajectory_list:
					read_topology = False
					call_read_lipid_function(topology_input)

				else:
					read_topology = False
					check_trajectory(topology_input, trajectory_list)
					

			# Return to the previous menu
			elif topology_input.upper() == 'RETURN':
				read_topology = False
				call_main_screen()

			# Leave the script
			elif topology_input.upper() == 'EXIT':
				read_topology = False
				show_exit_message()

			# Display error message on wrong selection
			else:
				print("""
/!\ ERROR! The requested selection is not valid! /!\ """)

				time.sleep(2)

##-\-\-\-\-\-\-\-\
## Lipid statistics
##-/-/-/-/-/-/-/-/

def call_lipid_stats():
	read_statistics = True

	while read_statistics:
		print("""
================================================================
================================================================

######################################
ML-LPA lpstats -- STATISTICS ON LIPIDS
######################################

Select system file to read:
---------------------------""")
	
		# Get the list of all topology files in the folder
		system_list = []
		for file in glob.glob('*.com'):
			system_list.append(file)

		# Raise error if there is no topology file in the folder
		if not system_list:
			print("""/!\ ERROR! No system file can be found in the directory /!\ """)
			time.sleep(2)

			read_statistics = False
			call_main_screen()

		else:	
			for file in system_list:
				print(file)

			print("""
RETURN to go the main menu
EXIT to leave the program
""")
			# Get the user choice
			system_input = input("? ")

			if system_input in system_list:
				read_statistics = False
				print("""
================================================================
================================================================
""")

				filename = system_input.split('.')[-2]
				filename = prefill_input('Output file name? ', filename)
					
				print("""
================================================================
================================================================
""")

				statistics.make_stats(system_input, filename)
				show_exit_message()			

			# Return to the previous menu
			elif system_input.upper() == 'RETURN':
				read_statistics = False
				call_main_screen()

			# Leave the script
			elif system_input.upper() == 'EXIT':
				read_statistics = False
				show_exit_message()

			# Display error message on wrong selection
			else:
				print("""
/!\ ERROR! The requested selection is not valid! /!\ """)

				time.sleep(2)

##-\-\-\-\-\-\-\-\-\-\-\
## Extract COM positions
##-/-/-/-/-/-/-/-/-/-/-/

def call_extract_com():
	read_com = True

	while read_com:
		print("""
================================================================
================================================================

###################################
ML-LPA getcom -- EXTRACT LIPIDS COM
###################################

Select system file to read:
---------------------------""")
	
		# Get the list of all topology files in the folder
		system_list = []
		for file in glob.glob('*.com'):
			system_list.append(file)

		# Raise error if there is no topology file in the folder
		if not system_list:
			print("""/!\ ERROR! No system file can be found in the directory /!\ """)
			time.sleep(2)

			read_com = False
			call_main_screen()

		else:	
			for file in system_list:
				print(file)

			print("""
RETURN to go the main menu
EXIT to leave the program
""")
			# Get the user choice
			system_input = input("? ")

			if system_input in system_list:
				read_com = False
				print("""
================================================================
================================================================
""")

				filename = system_input.split('.')[-2]
				filename = prefill_input('Output file name? ', filename)
					
				print("""
================================================================
================================================================
""")

				extract_com.predict_frontier(system_input, filename)
				show_exit_message()			

			# Return to the previous menu
			elif system_input.upper() == 'RETURN':
				read_com = False
				call_main_screen()

			# Leave the script
			elif system_input.upper() == 'EXIT':
				read_com = False
				show_exit_message()

			# Display error message on wrong selection
			else:
				print("""
/!\ ERROR! The requested selection is not valid! /!\ """)

				time.sleep(2)

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## Create Voronoi Tessellation
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

def call_visualisation():
	read_voronoi = True

	while read_voronoi:
		print("""
================================================================
================================================================

#############################################
ML-LPA memview -- SHOW MEMBRANE VISUALISATION
#############################################

Select system file to read:
---------------------------""")


		# Get the list of all topology files in the folder
		system_list = []
		for file in glob.glob('*.com'):
			system_list.append(file)

		# Raise error if there is no topology file in the folder
		if not system_list:
			print("""/!\ ERROR! No system file can be found in the directory /!\ """)
			time.sleep(2)

			read_voronoi = False
			call_main_screen()

		else:	
			for file in system_list:
				print(file)

			print("""
RETURN to go the main menu
EXIT to leave the program
""")
			# Get the user choice
			system_input = input("? ")

			if system_input in system_list:
				read_voronoi = False
				print("""
================================================================
================================================================
""")

				read_dimension = True

				while read_dimension:
					dimension = input('Dimensionality of the visualisation? (2/3) ')

					if dimension in ['2','3']:
						read_dimension = False
					else:
						print("""
/!\ ERROR! The requested selection is not valid! /!\ 
""")

						time.sleep(2)

				filename = system_input.split('.')[-2]
				filename = prefill_input('Output file name? ', filename)
					
				print("""
================================================================
================================================================
""")

				visualisation.show_membrane(system_input, filename, dimension)
				show_exit_message()			

			# Return to the previous menu
			elif system_input.upper() == 'RETURN':
				read_voronoi = False
				call_main_screen()

			# Leave the script
			elif system_input.upper() == 'EXIT':
				read_voronoi = False
				show_exit_message()

			# Display error message on wrong selection
			else:
				print("""
/!\ ERROR! The requested selection is not valid! /!\ """)

				time.sleep(2)

##-\-\-\-\-\-\
## Main Screen
##-/-/-/-/-/-/

def call_main_screen():
	read_main_screen = True
	while read_main_screen:

		print("""
================================================================
================================================================
      ___           ___       ___       ___           ___     
     /\__\         /\__\     /\__\     /\  \         /\  \    
    /::|  |       /:/  /    /:/  /    /::\  \       /::\  \   
   /:|:|  |      /:/  /    /:/  /    /:/\:\  \     /:/\:\  \  
  /:/|:|__|__   /:/  /    /:/  /    /::\~\:\  \   /::\~\:\  \ 
 /:/ |::::\__\ /:/__/    /:/__/    /:/\:\ \:\__\ /:/\:\ \:\__\ 
 \/__/~~/:/  / \:\  \    \:\  \    \/__\:\/:/  / \/__\:\/:/  /
       /:/  /   \:\  \    \:\  \        \::/  /       \::/  / 
      /:/  /     \:\  \    \:\  \        \/__/        /:/  /  
     /:/  /       \:\__\    \:\__\                   /:/  /   
     \/__/         \/__/     \/__/                   \/__/    

================================================================
================================================================

Welcome to the text-interface of the ML-LPA module for Python !!

Current version: alpha (19/08/2018)
Author: Vivien WALTER (vivien.walter@gmail.com)
Git: tbd

================================================================
================================================================

Select action:
--------------
1. Read simulation files
2. Make statistics on lipids
3. Extract center of mass
4. Create representation
0. Exit
""")

		# Get user choice for next menu
		user_choice = input('? ')

		if user_choice == '1':
			read_main_screen = False
			call_read_simulation()
		elif user_choice == '2':
			read_main_screen = False
			call_lipid_stats()
		elif user_choice == '3':
			read_main_screen = False
			call_extract_com()
		elif user_choice == '4':
			read_main_screen = False
			call_visualisation()

		# Exit the interface
		elif user_choice == '0':
			read_main_screen = False
			show_exit_message()

		# Display error message on wrong selection
		else:
			print("""
/!\ ERROR! The requested selection is not valid! /!\ """)

			time.sleep(2)

## REMOVE AT THE END
#call_main_screen()
