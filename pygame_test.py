import pygame, sys
from pygame.locals import *
import os
from math import atan,pi
from utility import direction_to_angle,rot_center

fps=30
pygame.init()
window = pygame.display.set_mode((600, 600))
imgs_folder="\\imgs\\"
pygame.display.set_caption('Hello World!')


i=0

def update():
	global arrow,surf,i,angle

	mouse_pos=pygame.mouse.get_pos()
	arrow_pos=(125,125)
	if(mouse_pos != arrow_pos):
		direction=(
			mouse_pos[0]-arrow_pos[0],
			mouse_pos[1]-arrow_pos[1])

		angle=direction_to_angle(direction)

def draw_window():
	global arrow,surf,i,angle
	window.fill((0,0,0))

	surf= rot_center(arrow, angle)

	window.blit(surf , (100,100))

def main():
	global arrow
	arrow = pygame.image.load(
	os.path.join('imgs','arrow.png'))
	arrow= pygame.transform.scale(arrow, (50,50))
	arrow= rot_center(arrow, 90)

	clock= pygame.time.Clock()
	while True: # main game loop
		clock.tick(fps)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
		update()
		draw_window()

		pygame.display.update()

if (__name__=="__main__"):
	main()