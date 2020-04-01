
import numpy as np
from gdsii.library import Library
from gdsii.structure import Structure
from gdsii.elements import Boundary, RaithCircle



NAME = "raith-circle"

# the library holds everything in the .gds file.  It behaves as a python list
# units in nm
lib = Library(3, NAME, 1e-9, 0.001)

# define nm in gds units
nm = 1.
um = 1000 * nm


# 'struct' is the root 'cell' of this gds file.  It behaves as a python list
struct = Structure(NAME)
lib.append(struct)

struct += [
    # add a circle defined as a special Raith element
    RaithCircle(
        layer = 0,
        data_type = 1000, # dose adjust, 1000 = 1.0
        center = [0, 0],
        radius = 10 * um),
    
    # add a ring defined as a special Raith element
    RaithCircle(
        layer = 0,
        data_type = 1000, # dose adjust, 1000 = 1.0
        center = [20*um, 0],
        radius = 10 * um,
        width = 1 * um),
]

# RaithCircle called like:
#     RaithCircle(layer, data_type, center, radius, verts=64,
#         ellipse=False, filled=True, arced=False, arc=(0, 6283185), width=0):


# save to file
with open(NAME + ".gds", 'wb') as outfile:
    lib.save(outfile)
