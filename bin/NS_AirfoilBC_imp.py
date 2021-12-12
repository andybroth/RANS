import bcfar_fort, bcwall_fort, halo_fort
from bin.Field import Field

def init_state(self, model, workspace):
    field_size = workspace.field_size()
    stateDim = self.dim
    state = Field(field_size, stateDim)

    ##### TO DO #####

    return state

# update rev and rlv
def update_physics(self, model, workspace, state):
    pass
    ##### TO DO #####


# update stability
def update_stability(self, model, workspace, state):
    pass
    ##### TO DO #####


def bc_far(self, model, workspace, state):
    # define helper function for getting fields
    def get(varName):
        return workspace.get_field(varName, model.className)

    # get geometry dictionary
    geom = workspace.get_geometry()
    
    # dims
    [ib, jb] = state.size()
    il = ib-2
    jl = jb-2
    ie = ib-1
    je = jb-1
    itl = geom.itl
    itu = geom.itu
    
    # flo_var
    w = state.get_vals()
    rlv = get("rlv").get_vals()
    rev = get("rev").get_vals()
    p = get("p").get_vals()
    
    # mesh_var
    coords = workspace.get_field("x")
    x = coords.get_vals()
    coords = workspace.get_field("xc")
    xc = coords.get_vals()
    
    # out_var
    cp = 0
    cf = 0
    
    # flo_param
    gamma = model.gamma
    rm = model.rm
    rho0 = model.rho0
    p0 = model.p0
    h0 = model.h0
    c0 = model.c0
    u0 = model.u0
    v0 = model.v0
    ca = model.ca
    sa = model.sa
    re = model.re
    prn = 0
    prt = 0
    scal = geom.scal
    chord = geom.chord
    xm = geom.xm
    ym = geom.ym
    kvis = model.kvis
    
    # solv_param
    bc = 0
    
    # mg_param
    mode = 1
    if workspace.is_finest():
        mode = 0
    
    bcfar_fort.bcfar(il, jl, ie, je, itl, itu,
                        w, p, rlv, rev,
                        x, xc, 
                        cp, cf,
                        gamma,rm,rho0,p0,h0,c0,u0,v0,ca,sa,re,prn,prt,scal,chord,xm,ym,kvis,
                        bc,
                        mode)


def bc_wall(self, model, workspace, state):
    # define helper function for getting fields
    def get(varName):
        return workspace.get_field(varName, model.className)

    # get geometry dictionary
    geom = workspace.get_geometry()
    
    # dims
    [ib, jb] = state.size()
    nx = ib-3
    ny = jb-3
    il = ib-2
    ie = ib-1
    itl = geom.itl
    itu = geom.itu
    
    # flo_var
    w = state.get_vals()
    p = get("p").get_vals()
    rev = get("rev").get_vals()
    
    # mesh_var
    coords = workspace.get_field("x")
    x = coords.get_vals()
    
    # flo_param
    rm = model.mach
    sa = model.sa
    kvis = model.kvis
    
    # solv_param
    isym = 0
    
    bcwall_fort.bcwall(ny, il, ie, ib, itl, itu, 
                        w, p, rev,
                        x,
                        rm, sa, kvis,
                        isym)


def halo(self, model, workspace, state):
    # define helper function for getting fields
    def get(varName):
        return workspace.get_field(varName, model.className)

    # get geometry dictionary
    geom = workspace.get_geometry()
    
    # dims
    [ib, jb] = state.size()
    il = ib-2
    jl = jb-2
    ie = ib-1
    je = jb-1
    itl = geom.itl
    itu = geom.itu
    
    # flo_var
    w = state.get_vals()
    p = get("p").get_vals()

    # mesh_var
    coords = workspace.get_field("x")
    x = coords.get_vals()
    vol = get("vol").get_vals()
    
    halo_fort.halo(il, jl, ie, je, ib, jb, itl, itu,
            w, p,
            x, vol)


def transfer_down(self, model, workspace1, workspace2, rev1, rlv1, rev2, rlv2):
    # get geometry dictionary
    geom1 = workspace1.get_geometry()
    geom2 = workspace2.get_geometry()