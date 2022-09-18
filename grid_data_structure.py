from math import ceil

class Grid:
    #constructor
    def __init__(self, agent_list,cell_size,width,height):
        self.grid=[]
        self.cell_size=cell_size
        self.width=width
        self.height=height
        self.vsize=ceil(self.height/cell_size)
        self.hsize=ceil(self.width/cell_size)

        for i in range(self.hsize):
            self.grid.append([])
            for j in range(self.vsize):
                self.grid[i].append([])
        for agent in agent_list:
            (x,y)=agent.pos
            i=int(x//self.cell_size)
            j=int(y//self.cell_size)
            self.grid[i][j].append(agent)

    def getNeighbours(self,agent):
        neighbours=[]
        (x,y)=agent.pos
        agent_i=int(x//self.cell_size)
        agent_j=int(y//self.cell_size)
        for i in range(agent_i-1,agent_i+2):
            if 0<=i<self.hsize:
                for j in range(agent_j-1,agent_j+2):
                    if 0<=j<self.vsize:
                        for agent in self.grid[i][j]:
                            neighbours.append(agent)
        return neighbours
