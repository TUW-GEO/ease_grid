=========
ease_grid
=========

The Equal-Area Scalable Earth (EASE) Grid is a system of projections that is
used by NASA and others for distribution of remote sensing data.

You can find some overview information at `the NSIDC website
<http://nsidc.org/data/ease>`_. Unfortunately from the documentation it was not
clear to me how the latitude, longitude values of certain EASE grid resolutions
were calculated. So I wrote this package to find out.

Supported EASE Grids
====================

There are two versions of EASE grid systems. This package focuses on EASE-Grid
2.0 at the moment. The data we were reading is disseminated on the global
EASE-Grid projection which is why this is the one that is currently supported.

Note
====

This project has been set up using PyScaffold 2.5.6. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
