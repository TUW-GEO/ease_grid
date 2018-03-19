=========
ease_grid
=========

.. image:: https://travis-ci.org/TUW-GEO/ease_grid.svg?branch=master
    :target: https://travis-ci.org/TUW-GEO/ease_grid

.. image:: https://coveralls.io/repos/github/TUW-GEO/ease_grid/badge.svg?branch=master
   :target: https://coveralls.io/github/TUW-GEO/ease_grid?branch=master

.. image:: https://badge.fury.io/py/ease_grid.svg
    :target: http://badge.fury.io/py/ease_grid

.. image:: https://zenodo.org/badge/12761/TUW-GEO/ease_grid.svg
   :target: https://zenodo.org/badge/latestdoi/12761/TUW-GEO/ease_grid

.. image:: https://readthedocs.org/projects/ease-grid/badge/?version=latest
    :target: http://ease-grid.readthedocs.io/en/latest/?badge=latest

The Equal-Area Scalable Earth (EASE) Grid is a system of projections that is
used by NASA and others for distribution of remote sensing data.

You can find some overview information at `the NSIDC website
<http://nsidc.org/data/ease>`_. Unfortunately from the documentation it was not
clear to me how the latitude, longitude values of certain EASE grid resolutions
were calculated. So I wrote this package to find out.

Citation
========

If you use the software in a publication then please cite it using the Zenodo DOI:

.. image:: https://zenodo.org/badge/12761/TUW-GEO/ease_grid.svg
   :target: https://zenodo.org/badge/latestdoi/12761/TUW-GEO/ease_grid

Installation
============

This package should be installable through pip:

.. code::

    pip install ease_grid

Supported EASE Grids
====================

There are two versions of EASE grid systems. This package focuses on EASE-Grid
2.0 at the moment. The data we were reading is disseminated on the global
EASE-Grid projection which is why this is the one that is currently supported.

Calculation of any global EASE2 grid should work. Compability with the tiling
scheme of NASA is tested for the global 36km grid (``EASE2_M36KM``) and the
global 25km grid (``EASE2_M25KM``). The tiling of the 25km grid is only the same
as the NASA tiling if the ``map_scale`` parameter is given explicitely. This
will also be the case for the subgrids of the 36km grid like ``EASE2_M09KM`` and
``EASE2_M03KM``. The ``map_scale`` parameters used by NASA are available from
the file ``ease2_grid_info.pro`` inside the ``easeconv*.tgz`` file at
ftp://sidads.colorado.edu/pub/tools/easegrid/geolocation_tools/

How to use
==========

To get the coordinates of a EASE2 grid:

.. code-block:: python

    from ease_grid import EASE2_grid
    egrid = EASE2_grid(36000)
    assert egrid.shape == (406, 964)
    # these two attributes contain the longitude and latitude coordinate dimension
    egrid.londim
    egrid.latdim

Contribute
==========

We are happy if you want to contribute. Please raise an issue explaining what
is missing or if you find a bug. We will also gladly accept pull requests
against our master branch for new features or bug fixes.

Development setup
-----------------

For Development we recommend a ``conda`` environment

Guidelines
----------

If you want to contribute please follow these steps:

- Fork the ease_grid repository to your account
- make a new feature branch from the ease_grid master branch
- Add your feature
- Please include tests for your contributions in one of the test directories.
  We use py.test so a simple function called test_my_feature is enough
- submit a pull request to our master branch

Note
====

This project has been set up using PyScaffold 2.5.6. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
