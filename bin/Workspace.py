import numpy as np
from Field import Field
from Grid import Grid
from Model import Model

class Workspace:
    
    # Constructor
    def __init__(self, model,grid):
        self.grd = grid
        self.mdl = model

        # make a dictionary of fields
        self.flds = {}
        init_vals = np.zeros(self.grd.dims)

        for i in range(0,len(self.mdl.reqFields)):
            self.flds[self.mdl.reqFields[i]] = Field(init_vals)
        
        
    def add_field(self, new_field):
        # Adds a new field to workspace 
        init_vals = np.zeros(self.grd.dims)
        self.flds[new_field] = Field(init_vals)
        
        return 0
    
    def move_up(stencil, field):
        return 0
    
    def move_down(stencil, field):
        return 0
    
    def move_to(stencil, field):
        return 0