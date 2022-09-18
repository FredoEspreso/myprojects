import pygame, sys
from pygame.locals import *
import os
from math import atan,pi
import utility
import random
import numpy as np
from agent import Bird
from grid_data_structure import Grid

imgs_folder="\\imgs\\"
WIDTH=1200
HEIGHT=1080
noofagents=70
fps=30
cell_size=120


class Simulation:
	def __init__(self):
		np.seterr('raise')
		pygame.init()
		self.window = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption('Flock O\' Birds!')
		self.create_agents()
		self.clock= pygame.time.Clock()
		
	def start(self):
		while True: # main game loop
			self.clock.tick(fps)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
					
			self.update()
			self.del_and_spawn()
			self.draw_window(self.window)
			pygame.display.update()	

	#create agents
	def create_agents(self):
		self.agents=[]
		for i in range(noofagents):
			agent=Bird((random.randint(30,WIDTH-1-30),random.randint(30,HEIGHT-1-30)),
								0,
								"arrow.png")
			self.agents.append(agent)

	#updates the state of the agents
	def update(self):
		#grid=Grid(self.agents,cell_size,WIDTH,HEIGHT)
		for agent in self.agents:
			agent.update(self.agents)

	#draw graphics
	def draw_window(self,win):
		global arrow,surf,i,angle
		win.fill((0,0,0))
		for agent in self.agents:
			im= utility.rot_center(agent.original_img, agent.angle)
			win.blit(im , (agent.pos[0]-25,agent.pos[1]-25))

	#delete the agents out of bounds and spawn new ones
	def del_and_spawn(self):
		idx_to_delete=[]
		for i,agent in enumerate(self.agents):
			if(np.linalg.norm(agent.pos-(WIDTH/2,HEIGHT/2))>800):
				idx_to_delete=[i]+idx_to_delete
		for i in idx_to_delete:
			self.agents.pop(i)
		for i in range(len(idx_to_delete)):
			self.agents.append(Bird((random.randint(30,WIDTH-1-30),random.randint(30,HEIGHT-1-30)),
								0,
								"arrow.png"))

if (__name__=="__main__"):
	s=Simulation()
	s.start()