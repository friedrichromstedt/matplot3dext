# Copyright (c) 2010 Friedrich Romstedt <www.friedrichromstedt.org>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Last changed: 2010 Mar 22
# Developed since: Mar 2010

import matplot3dext.colormaps.interface

"""Colormaps with built-in normalisation.  They are used to hand over
colormaps and normalisation instance in one single object.  

The kind of objects matplot3dext.colormap.norm.NormColormaps can color depends 
on the capabilities of the normalisation object used."""


class NormColormap(matplot3dext.colormaps.interface.Colormap):
	"""Colormap with built-in normalisation.  Used to hand over colormaps
	and normalisation instance in one single object."""

	def __init__(self, cmap, norm):
		"""CMAP is a matplotlib.colors.Colormap instance.  NORM is something
		used to retrieve real values from something else, it must have a 
		method .normalise() accepting the object to be normalised as 
		argument."""

		self.cmap = cmap
		self.norm = norm

	def get_color(self, object):
		"""Get the color used for object OBJECT."""
		
		return self.cmap(self.norm.normalise(object))
