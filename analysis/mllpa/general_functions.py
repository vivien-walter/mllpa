#!/usr/bin/env python

import numpy as np

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

	# Get the axis vectors
	v1 = [1.0,0.0]
	v2 = [0.0,1.0]

	# Measure the angles
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

# Calculate the distance between two points in a 3D space
def distance_3d(a,b):
	return np.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2 )
