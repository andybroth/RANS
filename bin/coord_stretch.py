import numpy as np

def coord_stretch(self):
    #use parameters from geo_param in input
    geo    = self.geo
    xte    = geo["xte"]
    boundx = geo["boundx"]
    bunch  = geo["bunch"]
    ylim1  = geo["ylim1"]
    ylim2  = geo["ylim2"]
    ax     = geo["ax"]
    sy     = geo["sy"]

    #geo_var
    a0     = self.a0
    a1     = self.a1
    b0     = self.b0
    s0     = self.s0

    #parameters defined in sqrtgrid class
    il     = self.il
    nx     = self.nx
    ny     = self.ny

    ile    = self.ile
    pi     = np.pi
    xlim   = xte*boundx
    dx     = 2.0*boundx/nx

    px     = pi/xlim
    bp     = bunch/px

    a2     = 3.0*ylim1  -4.0*ylim2
    a3     = 2.0*ylim1  -3.0*ylim2

    for i in range(0,nx):
        d  = (i  -ile)*dx
        if abs(d) <= xlim:
            d = d  +bp*np.sin(px*d)
        else:
            b         = 1.
            if d < 0.0:
                b = -1
            a  =1.0  -((d  -b*xlim)/(1.0  -xlim))**2 
            c  = a**ax
            d  = b*xlim  +(1.0  -bunch)*(d  -b*xlim)/c
        a0[i] = d
        d     = abs(d/xlim)
        if d >= 1.0:
            a1[i]     = ylim2*xlim/abs(a0[i])
        else:
            a1[i]     = ylim1  -d*d*(a2  -a3*d)

        d = a0(i)*a1(i)
    return
      
      

    

