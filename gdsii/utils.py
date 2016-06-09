
from numpy import array, cos, sin, pi, linspace, matrix

#
# The vector function
#
def v(*a):
    return array(a)

#
# Polygon clipping functions.
# uses clipper/pyclipper for bool operations.
#

try:
    import pyclipper
except ImportError:
    print("pyclipper is not installed.  needed for boolean operations")

def union(p1, p2, operation=pyclipper.CT_UNION):
    pc = pyclipper.Pyclipper()
    pc.AddPath(p1, pyclipper.PT_SUBJECT, True)
    pc.AddPath(p2, pyclipper.PT_CLIP, True)

    out = pc.Execute(operation, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
    return [array(p) for p in out]

from functools import partial

difference = partial(union, operation=pyclipper.CT_DIFFERENCE)
intersection = partial(union, operation=pyclipper.CT_INTERSECTION)
xor = partial(union, operation=pyclipper.CT_XOR)

# define boolean operations that act on lists of polygons

def unions(p1, p2, operation=pyclipper.CT_UNION):
    pc = pyclipper.Pyclipper()
    pc.AddPaths(p1, pyclipper.PT_SUBJECT, True)
    pc.AddPaths(p2, pyclipper.PT_CLIP, True)

    out = pc.Execute(operation, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
    return [array(p) for p in out]


differences = partial(unions, operation=pyclipper.CT_DIFFERENCE)
intersections = partial(unions, operation=pyclipper.CT_INTERSECTION)
xors = partial(unions, operation=pyclipper.CT_XOR)
#
# Primitives
#

def rect(width, height=None, centered=True):
    if height is None:
        height = width
    p = v((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))
    if centered:
        p = p - v(0.5, 0.5)
    return array(p * v(width, height))

def circle(r, th0=0, th1=2*pi, npoints=361):
    np = (th1 - th0) / (2.*pi) * npoints
    p = [(r*cos(th), r*sin(th)) for th in linspace(th0, th1, np)]
    if (th0 % 2*pi) != (th1 % 2*pi):
        p += [(0, 0), p[0]]
    return array(p)

def ring(r0, r1, th0=0, th1=2*pi, npoints=361):
    np = abs(th1 - th0) / (2.*pi) * npoints
    p  = [(r0*cos(th), r0*sin(th)) for th in linspace(th0, th1, np)]
    p += [(r1*cos(th), r1*sin(th)) for th in linspace(th1, th0, np)]
    p += [p[0]]
    return array(p)

def rot(th):
    return array([(cos(th), sin(th)), (-sin(th), cos(th))])

deg = degree = pi / 180.
# define a circle shaped polygon that can be substituded with a RaithCircle shape
# so circles to show up in other .gds editors

def circleold():
    r, r0 = radius, center

    rarc = array(arc) / 1e6

    path  = [v((r + width/2.) * cos(theta),
               (r + width/2.) * sin(theta)) for theta in linspace(rarc[0], rarc[1], verts)]
    if not filled and width > 0:
        path += [v((r - width/2.) * cos(theta),
                   (r - width/2.) * sin(theta)) for theta in linspace(rarc[1], rarc[0], verts)]

    return Boundary(layer, data_type, [p + r0 for p in path])
