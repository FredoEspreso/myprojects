import pygame, sys
from pygame.locals import *
import os
from math import atan,pi,sqrt
import numpy as np

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def direction_to_angle(direction):
	x=direction[0]
	y=-direction[1]
	if(y==0):
		if(x>0):
			angle=0
		if(x<0):
			angle=pi
	elif(y>0 and x==0):
		angle=pi/2
	elif(y<0 and x==0):
		angle=-pi/2
	else:
		if(x>0):
			angle=atan(y/x)
		if(x<0):
			angle=pi+atan(y/x)
	return 180*angle/pi

def normalize(v):
	if( not (v==0).all() ):
		return v/np.linalg.norm(v)
	else:
		return v

def constrain_to_radius(v,r):
	if( (v==0).all() ):
		return v
	else:
		if(np.linalg.norm(v)>r):
			return r*normalize(v)
		else:
			return v

original_arrow = pygame.image.load(
os.path.join('imgs','arrow.png'))
original_arrow= pygame.transform.scale(original_arrow, (50,50))
original_arrow= rot_center(original_arrow, 90)
