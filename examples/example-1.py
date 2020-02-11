
import numpy as np
from gdsii.library import Library
from gdsii.structure import Structure
from gdsii.elements import Boundary

from gdsii.utils import rot, degree, v, rect, circle, ring, differences, difference, union, unions


# define units

nm = 1.
um = 1000 * nm
mm = 1000 * um
 

NAME = "example-1"

# the library holds everything in the .gds file.  It behaves as a python list
# set units in nm
lib = Library(3, NAME, 1e-9, 0.001)


# new GDSII structure
struct0 = Structure("cell0")
lib.append(struct0)




p0 = v(0*nm, 0*nm)

# manually create a polygon
poly = np.array([(1, 2), (3, 4), (5, 6)]) * nm

# translate
poly = poly + v(100*nm, 0)

# scale
poly = poly * v(2., 2.)



# add the polygon to the gdsII structure

struct0 += [
    Boundary(0, 1000, poly),
]

# Polygon set!

polyset = [
    circle(50*nm, th0=0, th1=np.pi, npoints=80),
    rect(200*nm, 400*nm, centered=False) + v(0*nm, 0),
]


# add a polygon set to gdsii file with list comprehension:
# struct0 += [Boundary(0, 1000, p) for p in polyset]

# boolean operations


polyset = unions([
    circle(50*nm, th0=0, th1=np.pi, npoints=80),
], [
    rect(200*nm, 400*nm, centered=False) + v(0*nm, 0),
])

sub = rect(width=500*nm, height=100*nm, centered=False) + v(10*nm, 100*nm)

# polyset += sub
# subtract a rectangle
polyset = differences(polyset, [
    sub,
])



# add a polygon set to gdsii file with list comprehension:
struct0 += [Boundary(0, 1000, p) for p in polyset]

# save to file
with open("example-1.gds", 'wb') as outfile:
    lib.save(outfile)