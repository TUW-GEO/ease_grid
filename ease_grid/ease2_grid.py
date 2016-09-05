# The MIT License (MIT)
#
# Copyright (c) 2016,Christoph Paulik
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
Module for generation of EASE grid 2.0 latitudes and longitudes.
'''

import pyproj
import math
import pygeogrids
import numpy as np


class EASE2_grid(object):
    """
    EASE grid 2.0 definition.

    Parameters
    ----------
    res: float
        Resolution of the grid tiling in meters.
    proj: string, optional
       Projection to use 'N' for North, 'S' for South and
       'G' for Global
    map_scale: float, optional
       if the map_scale is given and should not be calculated

    Attributes
    ----------
    res: float
       resolution that the grid tiling should have
    map_scale: float
       resolution that is possible based on integer tiling of the projection
    x_pixel: float
       pixels extent in x direction in meters
    y_pixel: float
       pixels extent in y direction in meters
    latdim: numpy.ndarray
       latitudes used in the tiling
    londim: numpy.ndarray
       longitudes used in the tiling
    shape: tuple
       size of the tiling in (latdim, londim)
    """

    def __init__(self, res, proj='G', map_scale=None):
        self.res = res
        if proj != 'G':
            raise NotImplementedError(
                "Only Global projection supported for now.")
        self.proj = proj
        self.map_scale = map_scale
        self.geod = pygeogrids.geodetic_datum.GeodeticDatum("WGS84")
        # global ease grid 2.0
        if self.proj == 'G':
            self.londim, self.latdim = self.setup_global()
            self.shape = (len(self.latdim), len(self.londim))

    def setup_global(self):
        self.ease = pyproj.Proj(("+proj=cea +lat_0=0 +lon_0=0 +lat_ts=30 "
                                 "+x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m"))
        # circumference of the WGS84 ellipsoid at latitude 30 degrees
        self.circum_ref_lat = self.geod.ParallelRadi(30) * 2 * math.pi

        self.x_int = int(self.circum_ref_lat / self.res)
        # x_int has to be an even number
        if self.x_int % 2 != 0:
            self.x_int = self.x_int - 1
        if self.map_scale is None:
            self.map_scale = self.circum_ref_lat / self.x_int

        # We want to tile the projection into a grid that has the same sampling as a
        # 36x36 km square pixel. So we calculate the size of our pixels in x direction
        # and then calculate the necessary size in y direction from that.

        self.x_min, self.y_max = self.ease(-180, 90)
        self.x_max, self.y_min = self.ease(180, -90)

        # calculate x extent in meters and size of pixel in x direction
        self.x_extent = self.x_max - self.x_min
        self.x_pixel = self.x_extent / self.x_int
        # the y_pixel size can now be calculated so that the area covered by a pixel is
        # a close to the square pixel of the wanted resolution
        self.y_pixel = (self.map_scale ** 2) / self.x_pixel

        # now we can start from the center of this projection which is at 0,0
        # longitude, latitude and also 0,0 x,y and calculate pixel boundaries until we
        # reach the border of the projection

        # Ease grid pixels are defined with the center points by convention so we
        # create shifted points by self.x_pixel/2 and self.y_pixel/2

        y_arr_neg = np.arange(-self.y_pixel / 2, self.y_min, -self.y_pixel)
        x_arr_neg = np.arange(-self.x_pixel / 2, self.x_min, -self.x_pixel)

        y_arr_pos = np.arange(self.y_pixel / 2, self.y_max, self.y_pixel)
        x_arr_pos = np.arange(self.x_pixel / 2, self.x_max, self.x_pixel)

        # now we can put the two arrays together
        # one array has to be flipped so they fit together from -180 to +180 in
        # longitude and 90 to -90 in latitude.
        x_arr = np.concatenate([x_arr_neg[::-1], x_arr_pos])
        y_arr = np.concatenate([y_arr_pos[::-1], y_arr_neg])

        # In y direction the last pixel might not fit completely into the valid
        # projected area. To check this we calcualte the north border of the
        # pixels and project it. If the norht border does not project then we discard
        # the northern and southern pixel center.

        try:
            lat = self.ease(0, y_arr[0] + self.y_pixel / 2,
                            inverse=True,
                            errcheck=True)[1]
            if lat > 86.6225:
                y_arr = y_arr[1:-1]
        except RuntimeError:
            # Exclude northmost and southmost latitude
            y_arr = y_arr[1:-1]
        londim, _ = self.ease(x_arr, np.zeros(x_arr.shape), inverse=True)
        _, latdim = self.ease(np.zeros(y_arr.shape), y_arr, inverse=True)
        return londim, latdim
