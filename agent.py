from utility import *
import os
import numpy as np
from grid_data_structure import Grid
from global_variables import *

class Agent:
    #constructor
    def __init__(self, init_pos,init_angle,img_path):
        self.max_velocity=6
        self.max_accel=0.4
        self.pos = np.array(init_pos)
        self.velocity=np.random.rand(2)*self.max_velocity*np.random.uniform(-1,1)
        self.angle = init_angle
        self.accel = np.array([0.0,0.0])

        #initialize the agent's image
        self.original_img = pygame.image.load(
        os.path.join('imgs',img_path))
        self.original_img= pygame.transform.scale(self.original_img, (40,40))
        self.original_img= rot_center(self.original_img, 90)

    #use this function to update the agent in every frame
    def update(self,agents_list):
        pass

class Bird(Agent):
    #constructor
    def __init__(self, range, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.range=range

    #use this function to update the agent in every frame
    def update(self,grid):
        prev_accel=self.accel
        #initialize acceleration to zero
        self.accel=np.array([0.0,0.0])
        neighbours=self.get_neighbours(grid,self.range)
        
        #add acceleration component
        self.accel+= 10*self.alignment(neighbours)
        self.accel+= self.cohesion(neighbours)
        self.accel+= 10*self.separation(neighbours)

        self.accel=constrain_to_radius(self.accel,self.max_accel)
        self.accel=0.8*self.accel+0.2*prev_accel
        #update velocity
        self.velocity+=self.accel
        self.velocity=constrain_to_radius(self.velocity,self.max_velocity)

        #update looking angle (same as velocity)
        if( np.linalg.norm(self.velocity)>0 ) :
            self.angle=direction_to_angle(self.velocity)

        #update position
        self.pos=self.pos*(1.0)+self.velocity
        self.pos[0]=self.pos[0]%WIDTH
        self.pos[1]=self.pos[1]%HEIGHT

    
    #returns the acceleration to seek target
    
    def seek(self,target):
        desired_velocity= target-self.pos
        desired_velocity= self.max_velocity*normalize(desired_velocity)
        return self.max_accel*normalize(1.0*desired_velocity-self.velocity)

    #returns the acceleration to seek and arrive at target
    def seek_arrive(self,target,arrive_radius):
        dist = np.linalg.norm(target-self.pos)
        if( dist>arrive_radius ):
            return self.seek(target)
        else:
            desired_velocity= target-self.pos
            desired_velocity= self.max_velocity*normalize(desired_velocity)*dist/arrive_radius
            velocity_unit=normalize(self.velocity)
            return constrain_to_radius((1.0*desired_velocity-self.velocity),self.max_accel)

    def cohesion(self,neighbourhood):
        if (neighbourhood):
            #get a list of neighbour positions
            offset_to_neighbours=list(map(lambda agent: agent.pos-self.pos,neighbourhood))
            offset_to_neighbours=[]
            for agent in neighbourhood:
                (dx,dy)=agent.pos-self.pos
                for (dx,dy) in offset_to_neighbours:
                    #ledonut topology
                    if abs(dx) > WIDTH-abs(dx) :
                        dx=dx-WIDTH
                    if abs(dy) > HEIGHT-abs(dy) :
                        dy=dy-HEIGHT
            offset_to_neighbours.append((dx,dy))
            average_offset= np.average(offset_to_neighbours,0)
            desired_velocity= normalize(average_offset)*self.max_velocity
            return self.max_accel*normalize(1.0*desired_velocity-self.velocity)
        else:
            return np.array([0,0])
    
    def alignment(self,neighbourhood):
        velocities=list(map(lambda agent: agent.velocity,neighbourhood))
        if(velocities):
            average_velocity= np.average(velocities,0)
            average_velocity= normalize(average_velocity)*self.max_velocity*0.7
            return self.max_accel*normalize(1.0*average_velocity-self.velocity)
        else:
            return np.array([0,0])
    def separation(self,neighbourhood):
        if (neighbourhood):
            offset_to_neighbours=list(map(lambda agent: agent.pos-self.pos,neighbourhood))
            offset_to_neighbours=[]
            for agent in neighbourhood:
                (dx,dy)=agent.pos-self.pos
                #ledonut topology
                if abs(dx) > WIDTH-abs(dx) :
                    dx=dx-WIDTH
                if abs(dy) > HEIGHT-abs(dy) :
                    dy=dy-HEIGHT
                offset_to_neighbours.append((dx,dy))

            desired_velocity=np.array([0.0,0.0])
            steer=np.array([0.0,0.0])
            for offset in offset_to_neighbours:
                desired_velocity -= np.array(offset)*self.max_velocity
                steer+=(1.0*desired_velocity-self.velocity)/(np.sqrt(np.linalg.norm(offset)))
            
            return constrain_to_radius(steer,self.max_accel)
        else:
            return np.array([0,0])

    def get_neighbours(self,grid,r):
        neighbours=[]
        for agent in grid.getNeighbours(self):
            (ax,ay)=self.pos
            (bx,by)=agent.pos
            (dx,dy)=(bx-ax,by-ay)
            #ledonut topology
            if abs(dx) > WIDTH-abs(dx) :
                dx=dx-WIDTH
            if abs(dy) > HEIGHT-abs(dy) :
                dy=dy-HEIGHT

            if( 0<np.linalg.norm((dx,dy))<r ):
                neighbours.append(agent)
        return neighbours
