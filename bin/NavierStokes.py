from Model import Model
from Workspace import Workspace
from bin.Field import Field

class NavierStokes(Model):
    
    def __init__(self, bcmodel, input):
        self.className = "NavierStokes"
        self.BCmodel = bcmodel
        self.padding = 2 # size of halo
        self.flo_params = input.flo_params # grab physical parameters
        

    # initialize state
    def init_state(self, workspace, state):
        self.__check_vars(workspace)

        # copy into padded state field
        w = workspace.get_field("w", self.className)
        self.__copy_in(state, w)

        # pass off to boundary condition model to initialize
        self.BCmodel.init_state(self, workspace, w)
        
        # copy out to non-padded field
        self.__copy_out(w, state)


    # flux calculations
    from .model_funcs import eflux_wrap,nsflux_wrap, dflux_wrap, dfluxc_wrap

    def get_flux(self, workspace, state, output, update_factor=1):
        self.__check_vars(workspace)
        
        # initialize the variables we want in the workspace 
        self.__check_vars(self, workspace)

        # set rfil value
        rfil = update_factor

        # retrieve necessary workspace fields
        def get(varName):
            return workspace.get_field(varName, self.className)
        w = get("w")
        fw = get("fw")
        vw = get("vw")
        dw = get("dw")


        # copy state into padded array
        self.__copy_in(state, w)

        # calculate residuals
        ##### TO DO #####
        

        # copy residuals into output array
        self.__copy_out(dw, output)



    def get_safe_timestep(self, workspace, state, timestep):
        self.__check_vars(workspace)
        # retrieve necessary workspace fields
        def get(varName):
            return workspace.get_field(varName, self.className)
        dtl = get("dtl")
        rfl = get("rfl")

        # default is to set dt to dtl
        dt = dtl

        # export dt
        self.__copy_out(dt, timestep)


    # update rev and rlv
    def update_physics(self, model, workspace, state):
        self.__check_vars(workspace)

        # copy state into padded field
        w = workspace.get_field("w", self.className)
        self.__copy_in(state, w)

        self.BCmodel.update_physics(self, model, workspace, state)


    # calls 'step.f' to update stability conditions
    def update_stability(self, model, workspace, state):
        self.__check_vars(workspace)
        
        # copy state into padded field
        w = workspace.get_field("w", self.className)
        self.__copy_in(state, w)

        self.BCmodel.update_stability(self, model, workspace, state)

    
    def transfer_down(self, workspace1, workspace2):
        self.__check_vars(workspace)
        self.BCmodel.transfer_down(self, workspace1, workspace2)

    # copy non-padded fields into padded fields
    def __copy_in(self, field, paddedField):
        self.__check_vars(workspace)
        # get field size
        [leni, lenj] = field.size()
        p = self.padding

        # perform copy operation
        for i in range(0, leni):
            for j in range(0, lenj):
                paddedField[i+p][j+p] = field[i][j]

    # extract data from a padded field
    def __copy_out(self, paddedField, field):
        # get field size
        [leni, lenj] = field.size()
        p = self.padding

        # perform copy operation
        for i in range(0, leni):
            for j in range(0, lenj):
                field[i][j] = paddedField[i+p][j+p]

    # check if dictionary has been initialized
    def __check_vars(self, workspace):
        if not workspace.has_dict(self.className):
            self.__init_vars(workspace)

    # initialize class workspace fields
    def __init_vars(self, workspace):
        [nx, ny] = workspace.field_size()
        grid_size = [nx+1, ny+1]
        field_size = [nx+2, ny+2]
        stateDim = self.dim
        className = self.className

        # initialize list of variables to add
        vars = dict()

        # add state variables stored at cell center with padding
        for stateName in ["w", "dw", "vw", "fw"]:
            vars[stateName] = [field_size, stateDim]

        # add scalar variables stored at cell center with padding
        for stateName in ["P","radi","radj","rfl","dtl","rfli","rflj","vol"]:
            vars[stateName] = [field_size, stateDim]

        # add scalar variables stored at edges
        for stateName in ["porI","porJ"]:
            vars[stateName] = [grid_size, stateDim]

        workspace.init_vars(className, vars)