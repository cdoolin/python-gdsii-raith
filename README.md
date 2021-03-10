python-gdsii-raith
==================

python-gdsii-raith is a modification of the python-gdsii library to add a
RaithCircle element for use with RAITH Electron Beam lithography software.

It also adds the `utils` module which provides a framework for generating
designs agnostic from the python-gdsii library.  It includes functions for generating
basic shapes, as well as implementing boolean operations using the pyclipper library.

Designs built this way use python and numpy structures to represent polygons and polygon sets, which
can be easily converted to gdsii shapes.

### Install

```bash
pip install git+https://github.com/cdoolin/python-gdsii-raith@master
```

### Vector:

`utils` provides a function, `v` to create numpy vectors.  Its definition is simply: `v = lambda a*: numpy.array(*a)
`.

That is, to create a length two numpy array to use as a 2-vector, it can be done with `v(10, 20)`, instead of `array([10, 20])`.

This is purely syntactic sugar, but comes in use when dealing with polygons as described below.

### Polygon:

A polygon is a collection of 2-vectors to describe a path or enclosed shape.  It is a two-dimensional numpy array with shape (n, 2), where n is the number of points in the polygon.  It can be constructed by passing a list of tuples to numpy's array function like:

```python
poly = array([(1, 2), (3, 4), (5, 6)])
```

Or, for through a list of x and y values like
```python
x = linspace(0, 10, 11)
y = x**2.

poly = vstack((x, y)).T
```

By using a two dimensional numpy array, these polygons can be easily scaled and transposed through use of the Vectors described above.  For example, to translate the polygon by (100, 200), it can be done like:

```python
poly = poly + v(100, 200)
```

Or to scale, by

```python
poly = poly * v(2, 2).
```

To join two polygons together into a single continous polygon, numpy's vstack function can be used:

```python
poly = numpy.vstack((poly1, poly2)).
```

Finally, a polygon can be converted to a gdsii object, often a Boundary, directly passing it.  eg.

```python
b = Boundary(0, 1000, poly),
```
where 0 is the layer number, 1000 is a gdsii parameter which on the Raith software defines the dose factor (1000 = 1.0 dose).


The utils library includes a few functions for generating useful polygons,

```python
circlepoly = circle(r=50)
rectpoly = rect(width=100, height=100, centered=True)
```
### PolygonSet:

A polygon set is a python list of Polygons.  This is useful grouping polygons together to create a more complicated design.  PolygonSets are also used directly in the boolean operation functions.

Operations such as translation and scaling can be done through python list comprehension:

```python
polyset = [p + v(10, 20) for p in polyset]
```

or


```python
polyset = [p * v(2, 2) for p in polyset].
```

Likewise, to add a set of polygons to a gdsii structure can be done like:

```python
struct += [Boundary(0, 1000, p) for p in polyset]
```


















### python-gdsii:

(original library documentation)

python-gdsii is a library that can be used to read, create, modify and save
GDSII files. It supports both low-level record I/O and high level interface to
GDSII libraries (databases), structures, and elements.

This package also includes scripts that can be used to convert binary GDS file
to a simple text format (gds2txt), YAML (gds2yaml), and from text fromat
back to GDSII (txt2gds).

#### Usage

For most cases interface provided by Library class from gdsii.library should be
enough. Here is a small example:

```python
    from gdsii.library import Library
    from gdsii.elements import *

    # read a library from a file
    with open('file.gds', 'rb') as stream:
        lib = Library.load(stream)

    # let's move the first structure to a new library
    new_lib = Library(5, b'NEWLIB.DB', 1e-9, 0.001)
    struc = lib.pop(0) # libraries and structures are derived from list class
    new_lib.append(struc)

    # let's also add some elements...
    # Note: first and last points in the boundary should be the same
    #       this is required by GDSII spec.
    struc.append(Boundary(45, 0, [(-100000, -100000), (-100000, 0), (0,0), (0, -100000), (-100000, -100000)]))

    # Save both files with different names...
    with open('newfile1.gds', 'wb') as stream:
        lib.save(stream)

    with open('newfile2.gds', 'wb') as stream:
        new_lib.save(stream)
```


### python-gdsii Raith elements

For all elements, the data_type parameter of gdsii elements is used to store the relative dose, with a value of 1000 equal to a relative dose of 1.0.



To use Raith elements, the classes `RaithCircle` and `RaithFBMS` have been added to `gdsii.elements`.

A special Raith gdsii element can be added to a structure by making sure they are first imported:

```python
from gdsii.elements import RaithCircle, RaithFBMS
```

and then adding to an existing structure:

```python
struct.append(
    RaithCircle(
        layer = 0,
        data_type = 1000, # dose adjust, 1000 = 1.0
        center = [0, 0],
        radius = 10 * um))
```

A more complete example can be found [in the examples directory](examples/raith-circle.py).

To create a `RaithCircle`, the initializer function looks like:
```python
RaithCircle(
    layer, data_type,
    center, # 2-length list for center coordinates 
    radius, verts=64, ellipse=False, filled=True, arced=False, 
    arc=(0, 6283185), width=0)
```

and for `RaithFBMS`:
```python
RaithFBMS(
    layer, data_type, 
    xy, # 2*n length list of x, y coordinates for FBMS path
    width=0)
```
