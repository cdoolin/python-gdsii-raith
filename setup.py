from distutils.core import setup

long_desc = """
python-gdsii is a library that can be used to read, create, modify and save
GDSII files. It supports both low-level record I/O and high level interface to
GDSII libraries (databases), structures, and elements.

This package also includes scripts that can be used to convert binary GDS file
to a simple text format (gds2txt), YAML (gds2yaml), and from text fromat back
to GDSII (txt2gds).

python-gdsii-raith implements a custom gdsii record for use with drawing curves
on RAITH electron beam lithography systems.
"""

setup(
    name = 'python-gdsii-raith',
    version = '0.1.0',
    description = 'GDSII manipulation library with RAITH EBL support',
    long_description = long_desc,
    url = 'https://github.com/cdoolin/python-gdsii-raith',
    packages = ['gdsii'],
    scripts = [
        'scripts/gds2txt',
        'scripts/gds2yaml',
        'scripts/txt2gds',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    license = 'LGPL-3+',
    platforms = 'any'
)
