import pygame, sys
from pygame.locals import *
import os
from math import atan,pi
import utility
import random
import numpy as np

np.seterr('raise')
noofagents=70
fps=30
pygame.init()
WIDTH=1200
HEIGHT=1080
window = pygame.display.set_mode((WIDTH, HEIGHT))
imgs_folder="\\imgs\\"
pygame.display.set_caption('Hello World!')
from agent import Agent


i=0
def init():
	global agents
	agents=[]
	for i in range(noofagents):
		agents.append(Agent((random.randint(30,WIDTH-1-30),random.randint(30,HEIGHT-1-30)),
							0,
							"arrow.png"))

def update():
	for agent in agents:
		agent.update(agents)

def draw_window(win):
	global arrow,surf,i,angle
	win.fill((0,0,0))
	for agent in agents:
		im= utility.rot_center(agent.original_img, agent.angle)
		win.blit(im , (agent.pos[0]-25,agent.pos[1]-25))

def del_and_spawn():
	idx_to_delete=[]
	for i,agent in enumerate(agents):
		if(np.linalg.norm(agent.pos-(WIDTH/2,HEIGHT/2))>800):
			idx_to_delete=[i]+idx_to_delete
	for i in idx_to_delete:
		agents.pop(i)
	for i in range(len(idx_to_delete)):
		agents.append(Agent((random.randint(30,WIDTH-1-30),random.randint(30,HEIGHT-1-30)),
							0,
							"arrow.png"))

def main():
	init()
	clock= pygame.time.Clock()
	while True: # main game loop
		clock.tick(fps)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
		update()
		del_and_spawn()
		draw_window(window)

		pygame.display.update()

if (__name__=="__main__"):
	main()