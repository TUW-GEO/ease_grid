# The MIT License (MIT)
#
# Copyright (c) 2016, TU Wien
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Tests for EASE grid 2.0 class.
'''

from ease_grid import EASE2_grid
import numpy.testing as nptest
import numpy as np
import os


def test_EASE2_global_36km():

    test_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'ease_grid-test-data', 'EASE2')
    test_lat = os.path.join(test_path, 'EASE2_M36km.lats.964x406x1.double')
    test_lon = os.path.join(test_path, 'EASE2_M36km.lons.964x406x1.double')
    egrid = EASE2_grid(36000)
    assert egrid.shape == (406, 964)
    nptest.assert_almost_equal(egrid.x_pixel, egrid.map_scale)
    nptest.assert_almost_equal(egrid.y_pixel, egrid.map_scale)
    nptest.assert_almost_equal(egrid.map_scale, 36032.220840583752)
    lat_should = np.fromfile(test_lat, dtype=np.float64)
    lon_should = np.fromfile(test_lon, dtype=np.float64)
    nptest.assert_almost_equal(egrid.londim,
                               lon_should.reshape((406, 964))[0, :])
    nptest.assert_almost_equal(egrid.latdim,
                               lat_should.reshape((406, 964))[:, 0])


def test_EASE2_global_25km():

    test_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'ease_grid-test-data', 'EASE2')
    test_lat = os.path.join(test_path, 'EASE2_M25km.lats.1388x584x1.double')
    test_lon = os.path.join(test_path, 'EASE2_M25km.lons.1388x584x1.double')
    egrid = EASE2_grid(25000, map_scale=25025.2600081)
    assert egrid.shape == (584, 1388)
    nptest.assert_almost_equal(egrid.map_scale, 25025.2600081)
    lat_should = np.fromfile(test_lat, dtype=np.float64)
    lon_should = np.fromfile(test_lon, dtype=np.float64)
    nptest.assert_almost_equal(egrid.londim,
                               lon_should.reshape((584, 1388))[100, :])
    nptest.assert_almost_equal(egrid.latdim,
                               lat_should.reshape((584, 1388))[:, 120])
