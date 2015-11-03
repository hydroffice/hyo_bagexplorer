HydrOffice BAG Explorer
=======================

.. image:: https://readthedocs.org/projects/hydroffice-bag_explorer/badge/?version=latest
    :target: http://hydroffice-bag_explorer.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

General info
------------

.. image:: https://bitbucket.org/ccomjhc/hyo_bag_explorer/raw/tip/hydroffice/bag_explorer/media/BAGExplorer_128.png
    :alt: logo

HydrOffice is a research development environment for ocean mapping. It provides a collection of hydro-packages, each of them dealing with a specific issue of the field.
The main goal is to speed up both algorithms testing and research-2-operation.

BAG Explorer is a light application, based on HDF Compass and the HydrOffice BAG library tools, to explore BAG data files.

HDF Compass is written in Python, but ships as a native application on Windows, OS X, and Linux, by using PyInstaller and Py2App to package the app.
For more info about HDF Compass, visit the `GitHub <http://github.com/HDFGroup/hdf-compass>`_ repository and the `project <https://www.hdfgroup.org/projects/compass/>`_ web page.

HydrOffice BAG library provides access to BAG-specific features, as well as a collection of tools to verify and manipulate BAG data files.


Dependencies
------------

For executing and packaging the *BAG Explorer* app:

* ``hdf_compass`` (that requires several dependencies as ``matplotlib``, ``wxPython``, ``h5py``)
* ``hydroffice.bag`` (that also requires ``lxml`` and ``osgeo.gdal``)
* ``PyInstaller`` *[for freezing the application]*
* ``appdmg`` *[for creating a dmg on Mac]*


Freezing
--------

Use of Pyinstaller
~~~~~~~~~~~~~~~~~~

* ``pyinstaller --clean -y BAGExplorer.1file.spec``
* ``pyinstaller --clean -y BAGExplorer.1folder.spec``

Creation of MAC OS dmg
~~~~~~~~~~~~~~~~~~~~~~

* ``appdmg spec.json BAGExplorer.dmg``


Other info
----------

* Bitbucket: `https://bitbucket.org/ccomjhc/hyo_bag_explorer <https://bitbucket.org/ccomjhc/hyo_bag_explorer>`_
* Project page: `http://ccom.unh.edu/project/hydroffice <http://ccom.unh.edu/project/hydroffice>`_
* License: BSD-like license (See `COPYING <https://bitbucket.org/ccomjhc/hyo_bag_explorer/raw/tip/COPYING.txt>`_)
