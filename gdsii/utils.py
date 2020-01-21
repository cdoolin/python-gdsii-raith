
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
    

    if len(p1) > 0:
        pc.AddPaths(p1, pyclipper.PT_SUBJECT, True)

    # exclude single points
    p2 = [p for p in p2 if p.shape[0] > 1]
    if len(p2) > 0:
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
    """return a polygon (2d np array) creating a rectangle"""
    if height is None:
        height = width
    p = v((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))
    if centered:
        p = p - v(0.5, 0.5)
    return array(p * v(width, height))

def circle(r, th0=0, th1=2*pi, npoints=361):
    """returns a polygon (2d numpy array) creating a circle"""
    np = int((th1 - th0) / (2.*pi) * npoints)
    if np  < 1:
        return array([(0, 0),])
    #     np = 1
    p = [(r*cos(th), r*sin(th)) for th in linspace(th0, th1, np)]
    if (th0 % (2*pi)) != (th1 % (2*pi)):
        p += [(0, 0), p[0]]
    return array(p)

def ring(r0, r1, th0=0, th1=2*pi, npoints=361):
    """return a polygon (2d np array) creating a ring"""
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



def to_fbms_path(path):
    # convert a standard path which has the format of a list of 2-vectors to
    # the path format required by the FBMS element
    # FBMS element allows a 3rd option which specifies a radius of curvature between to point,
    # and then wants that repacked in pairs of 2 vectors.
    # the radius is specified as the distance from between the midpoint of the vertex and the vertex previous the fbms line curves to.
    fbms = [(0, 0), (0, 0)]
    fbms += [(0, path[0][0]), (path[0][1], 0)]
    for p in path[1:]:
        if len(p) < 3 or p[2] == 0:
            fbms += [(1, p[0]), (p[1], 0)]
        else:
            fbms += [(2, p[0]), (p[1], p[2])]
    return fbms
