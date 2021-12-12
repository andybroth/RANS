from bin.BoundaryConditioner import BoundaryConditioner
from bin.NS_AirfoilBC_imp import NS_AirfoilBC_imp as implementation

class NS_AirfoilBC(BoundaryConditioner):
    
    
    def __init__(self, input):
        pass

    # initialize state
    def init_state(self, model, workspace):
        self.__check_vars(workspace)
        return implementation.init_state(self, model, workspace)

    # Methods for applying boundary conditions

    # update rev and rlv
    def update_physics(self, model, workspace, state):
        self.__check_vars(workspace)
        implementation.update_physics(self, model, workspace, state)
    
    # update stability
    def update_stability(self, model, workspace, state):
        self.__check_vars(workspace)
        implementation.update_physics(self, model, workspace, state)
    
    # apply far-field boundary conditions
    def bc_far(self, model, workspace, state):
        self.__check_vars(workspace)
        implementation.bc_far(self, model, workspace, state)


    # apply wall boundary conditions
    def bc_wall(self, model, workspace, state):
        self.__check_vars(workspace)
        implementation.bc_wall(self, model, workspace, state)


    # apply halo boundary conditions
    def halo(self, model, workspace, state):
        self.__check_vars(workspace)
        implementation.halo(self, model, workspace, state)


    # apply all boundary conditions
    def bc_all(self, model, workspace, state):
        self.__check_vars(workspace)
        self.bc_wall(self, model, workspace, state)
        self.bc_far(self, model, workspace, state)
        self.halo(self, model, workspace, state)

    # transfer data between workspaces
    def transfer_down(self, model, workspace1, workspace2):
        self.__check_vars(workspace1)
        self.__check_vars(workspace2)
        implementation.transfer_down(self, model, workspace1, workspace2)


    # initialize class workspace fields
    def __init_vars(self, workspace):
        field_size = workspace.field_size()
        className = self.className

        vars = dict()
        vars["pori"] = [field_size, 1]
        vars["porj"] = [field_size, 1]

        self.__set_porosity(workspace)

        workspace.init_vars(className, vars)

    # set the porosity values
    def __set_porosity(self, workspace):
        implementation.set_porosity(self, workspace)