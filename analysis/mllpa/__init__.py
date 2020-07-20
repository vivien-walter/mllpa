#!/usr/bin/env python

import os
import sys
import argparse

import mllpa.simple_tui as simple_tui
import mllpa.read_lipid as read_lipid
import mllpa.statistics as statistics
import mllpa.extract_com as extract_com
import mllpa.visualisation as visualisation

##-\-\-\-\-\-\-\-\
## Argument parsers
##-/-/-/-/-/-/-/-/

def call_tui():
	simple_tui.call_main_screen()

def call_readsim():
	parser = argparse.ArgumentParser(description='Extract the states of the lipid in the bilayer')

	def file_choices(choices,fname):
		ext = os.path.splitext(fname)[1][1:]
		if ext not in choices:
			parser.error("File doesn't end with one of {}".format(choices))
		return fname

	parser.add_argument('-f', '--topology_file',required=True,
			type=lambda s:file_choices(("gro","pdb"),s),
			help='topology file (.pdb or .gro)')
	parser.add_argument('-t', '--trajectory_file',
			type=lambda s:file_choices(("trr","xtc"),s),
			default = None,
			help='(Opt.) trajectory file (.trr or .xtc, default is none)')
	parser.add_argument('-o', '--output_file',required=True,
			help='generic name for the output files')
	parser.add_argument('-b', '--begin',
			default='1',
			help='(Opt.) first frame to read (default:1)')
	parser.add_argument('-e', '--end',
			default=None,
			help='(Opt.) dimension of the visualisation (default:last frame)')
	parser.add_argument('-skip', '--skip',
			default='0',
			help='(Opt.) number of frames to skip (default:0)')

	args = parser.parse_args()

	read_lipid.get_trajectory(args.topology_file, args.output_file, args.trajectory_file, args.begin, args.end, args.skip)

def call_lpstats():
	parser = argparse.ArgumentParser(description='Calculate statistics on the lipid bilayer')

	def file_choices(choices,fname):
		ext = os.path.splitext(fname)[1][1:]
		if ext not in choices:
			parser.error("File doesn't end with one of {}".format(choices))
		return fname

	parser.add_argument('-s', '--system_file',required=True,
			type=lambda s:file_choices(("com"),s),
			help='system file with the bilayer informations (.com)')
	parser.add_argument('-o', '--output_file',required=True,
			help='generic name for the output files')

	args = parser.parse_args()

	statistics.make_stats(system_file, output_file)

def call_getcom():
	parser = argparse.ArgumentParser(description='Calculate statistics on the lipid bilayer')

	def file_choices(choices,fname):
		ext = os.path.splitext(fname)[1][1:]
		if ext not in choices:
			parser.error("File doesn't end with one of {}".format(choices))
		return fname

	parser.add_argument('-s', '--system_file',required=True,
			type=lambda s:file_choices(("com"),s),
			help='system file with the bilayer informations (.com)')
	parser.add_argument('-o', '--output_file',required=True,
			help='generic name for the output files')

	args = parser.parse_args()

	extract_com.predict_frontier(system_file, output_file)

def call_memview():
	parser = argparse.ArgumentParser(description='Generate a visualisation of the bilayer')

	def file_choices(choices,fname):
		ext = os.path.splitext(fname)[1][1:]
		if ext not in choices:
			parser.error("File doesn't end with one of {}".format(choices))
		return fname

	parser.add_argument('-s', '--system_file',required=True,
			type=lambda s:file_choices(("com"),s),
			help='system file with the bilayer informations (.com)')
	parser.add_argument('-o', '--output_file',required=True,
			help='generic name for the output files')
	parser.add_argument('-d', '--dimension',
			default='2',
			help='(Opt.) dimension of the visualisation (2/3, default:2)')

	args = parser.parse_args()

	visualisation.show_membrane(args.system_file, args.output_file, args.dimension)
