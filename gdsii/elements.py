# -*- coding: utf-8 -*-
#
#   Copyright © 2010 Eugeniy Meshcheryakov <eugen@debian.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
    GDSII element classes
    ~~~~~~~~~~~~~~~~~~~~~

    This module contains definitions for classes representing
    various GDSII elements. Mapping between GDSII elements and
    classes is given in the following table:

        +-------------------+-------------------+
        | :const:`AREF`     | :class:`ARef`     |
        +-------------------+-------------------+
        | :const:`BOUNDARY` | :class:`Boundary` |
        +-------------------+-------------------+
        | :const:`BOX`      | :class:`Box`      |
        +-------------------+-------------------+
        | :const:`NODE`     | :class:`Node`     |
        +-------------------+-------------------+
        | :const:`PATH`     | :class:`Path`     |
        +-------------------+-------------------+
        | :const:`SREF`     | :class:`SRef`     |
        +-------------------+-------------------+
        | :const:`TEXT`     | :class:`Text`     |
        +-------------------+-------------------+
"""
from __future__ import absolute_import
from . import exceptions, record, tags, _records

__all__ = (
    'Boundary',
    'Path',
    'SRef',
    'ARef',
    'Text',
    'Node',
    'Box'
)

_ELFLAGS = _records.OptionalWholeRecord('elflags', tags.ELFLAGS, 'Element flags (bitfield).')
_PLEX = _records.SimpleOptionalRecord('plex', tags.PLEX, 'Plex (integer).')
_LAYER = _records.SimpleRecord('layer', tags.LAYER, 'Layer (integer).')
_DATATYPE = _records.SimpleRecord('data_type', tags.DATATYPE, 'Data type (integer).')
_PATHTYPE = _records.SimpleOptionalRecord('path_type', tags.PATHTYPE, 'Path type (integer).')
_WIDTH = _records.SimpleOptionalRecord('width', tags.WIDTH, 'Width of the path (integer).')
_BGNEXTN = _records.SimpleOptionalRecord('bgn_extn', tags.BGNEXTN, 'Beginning extension for path type 4 (integer, optional).')
_ENDEXTN = _records.SimpleOptionalRecord('end_extn', tags.ENDEXTN, 'End extension for path type 4 (integer, optional).')
_XY = _records.XYRecord('xy', tags.XY, 'Points.')
_SNAME = _records.StringRecord('struct_name', tags.SNAME, 'Name of a referenced structure (byte array).')
_STRANS = _records.STransRecord('strans', tags.STRANS, 'Transformation flags.')
_COLROW = _records.ColRowRecord('cols', 'rows', 'Number of columns (integer).', 'Number of rows (integer).')
_TEXTTYPE = _records.SimpleRecord('text_type', tags.TEXTTYPE, 'Text type (integer).')
_PRESENTATION = _records.OptionalWholeRecord('presentation', tags.PRESENTATION,
""" Bit array that specifies how the text is presented (optional).
    Meaning of bits:

    * Bits 10 and 11 specify font number (0-3).
    * Bits 12 and 13 specify vertical justification (0 - top, 1 - middle, 2 - bottom).
    * Bits 14 and 15 specify horizontal justification (0 - left, 1 - center, 2 - rigth).
""")
_STRING = _records.StringRecord('string', tags.STRING, 'A string as bytes array.')
_NODETYPE = _records.SimpleRecord('node_type', tags.NODETYPE, 'Node type (integer).')
_BOXTYPE = _records.SimpleRecord('box_type', tags.BOXTYPE, 'Box type (integer).')
_PROPERTIES = _records.PropertiesRecord('properties',
""" List containing properties of an element.
    Properties are represented as tuples (propattr, propvalue).
    Type of propattr is int, propvalue is bytes.
""")

class _Base(object):
    """Base class for all GDSII elements."""

    # dummy descriptors to silence pyckecker, should be set in derived classes
    _gds_tag = None
    _gds_objs = None
    __slots__ = ()

    @classmethod
    def _load(cls, gen):
        """
        Load an element from file using given generator `gen`.

        :param gen: :class:`pygdsii.record.Record` generator
        :returns: new element of class defined by `gen`
        """
        element_class = cls._tag_to_class_map[gen.current.tag]
        if not element_class:
            raise exceptions.FormatError('unexpected element tag')
        # do not call __init__() during reading from file
        # __init__() should require some arguments
        new_element = element_class._read_element(gen)
        return new_element

    @classmethod
    def _read_element(cls, gen):
        """Read element using `gen` generator."""
        self = cls.__new__(cls)
        gen.read_next()
        for obj in self._gds_objs:
            obj.read(self, gen)
        gen.current.check_tag(tags.ENDEL)
        gen.read_next()
        return self

    def _save(self, stream):
        record.Record(self._gds_tag).save(stream)
        for obj in self._gds_objs:
            obj.save(self, stream)
        record.Record(tags.ENDEL).save(stream)

class Boundary(_Base):
    """Class for :const:`BOUNDARY` GDSII element."""
    _gds_tag = tags.BOUNDARY
    _gds_objs = (_ELFLAGS, _PLEX, _LAYER, _DATATYPE, _XY, _PROPERTIES)
    __slots__ = ('layer', 'data_type', 'xy', 'elfalgs', 'plex', 'properties')

    def __init__(self, layer, data_type, xy, elfalgs=None, plex=None,
            properties=None):
        self.layer = layer
        self.data_type = data_type
        self.xy = xy
        self.elfalgs = elfalgs
        self.plex = plex
        self.properties = properties

class Path(_Base):
    """Class for :const:`PATH` GDSII element."""
    _gds_tag = tags.PATH
    _gds_objs = (_ELFLAGS, _PLEX, _LAYER, _DATATYPE, _PATHTYPE, _WIDTH,
            _BGNEXTN, _ENDEXTN, _XY, _PROPERTIES)
    __slots__ = ('layer', 'data_type', 'xy', 'elflags', 'plex', 'path_type',
            'width', 'bgn_extn', 'end_extn', 'properties')

    def __init__(self, layer, data_type, xy, elflags=None, plex=None,
            path_type=None, width=None, bgn_extn=None, end_extn=None,
            properties=None):
        self.layer = layer
        self.data_type = data_type
        self.xy = xy
        self.elflags = elflags
        self.plex = plex
        self.path_type = path_type
        self.width = width
        self.bgn_extn = bgn_extn
        self.end_extn = end_extn
        self.properties = properties

class SRef(_Base):
    """Class for :const:`SREF` GDSII element."""
    _gds_tag = tags.SREF
    _gds_objs = (_ELFLAGS, _PLEX, _SNAME, _STRANS, _XY, _PROPERTIES)
    __slots__ = ('struct_name', 'xy', 'elflags', 'strans', 'mag', 'angle',
            'properties')

    def __init__(self, struct_name, xy, elflags=None, strans=None, mag=None,
            angle=None, properties=None):
        self.struct_name = struct_name
        self.xy = xy
        self.elflags = elflags
        self.strans = strans
        self.mag = mag
        self.angle = angle
        self.strans = properties

class ARef(_Base):
    """Class for :const:`AREF` GDSII element."""
    _gds_tag = tags.AREF
    _gds_objs = (_ELFLAGS, _PLEX, _SNAME, _STRANS, _COLROW, _XY, _PROPERTIES)
    __slots__ = ('struct_name', 'cols', 'rows', 'xy', 'elflags', 'plex',
            'strans', 'mag', 'angle', 'properties')

    def __init__(self, struct_name, cols, rows, xy, elflags=None, plex=None,
            strans=None, mag=None, angle=None, properties=None):
        self.struct_name = struct_name
        self.cols = cols
        self.rows = rows
        self.xy = xy
        self.elflags = elflags
        self.plex = plex
        self.strans = strans
        self.mag = mag
        self.angle = angle
        self.properties = properties

class Text(_Base):
    """Class for :const:`TEXT` GDSII element."""
    _gds_tag = tags.TEXT
    _gds_objs = (_ELFLAGS, _PLEX, _LAYER, _TEXTTYPE, _PRESENTATION, _PATHTYPE,
            _WIDTH, _STRANS, _XY, _STRING, _PROPERTIES)
    __slots__ = ('layer', 'text_type', 'xy', 'string', 'elflags', 'plex',
            'presentation', 'path_type', 'width', 'strans', 'mag', 'angle',
            'properties')

    def __init__(self, layer, text_type, xy, string, elflags=None, plex=None,
            presentation=None, path_type=None, width=None, strans=None,
            mag=None, angle=None, properties=None):
        self.layer = layer
        self.text_type = text_type
        self.xy = xy
        self.string = string
        self.elflags = elflags
        self.plex = plex
        self.presentation = presentation
        self.path_type = path_type
        self.width = width
        self.strans = strans
        self.mag = mag
        self.angle = angle
        self.properties = properties

class Node(_Base):
    """Class for :const:`NODE` GDSII element."""
    _gds_tag = tags.NODE
    _gds_objs = (_ELFLAGS, _PLEX, _LAYER, _NODETYPE, _XY, _PROPERTIES)
    __slots__ = ('layer', 'node_type', 'xy', 'elflags', 'plex', 'properties')

    def __init__(self, layer, node_type, xy, elflags=None, plex=None,
            properties=None):
        self.layer = layer
        self.node_type = node_type
        self.xy = xy
        self.elflags = elflags
        self.plex = plex
        self.properties = properties

class Box(_Base):
    """Class for :const:`BOX` GDSII element."""
    _gds_tag = tags.BOX
    _gds_objs = (_ELFLAGS, _PLEX, _LAYER, _BOXTYPE, _XY, _PROPERTIES)
    __slots__ = ('layer', 'box_type', 'xy', 'elflags', 'plex', 'properties')

    def __init__(self, layer, box_type, xy, elflags=None, plex=None,
            properties=None):
        self.layer = layer
        self.box_type = box_type
        self.xy = xy
        self.elflags = elflags
        self.plex = plex
        self.properties = properties

_all_elements = (Boundary, Path, SRef, ARef, Text, Node, Box)

_Base._tag_to_class_map = (lambda: dict(((cls._gds_tag, cls) for cls in _all_elements)))()
