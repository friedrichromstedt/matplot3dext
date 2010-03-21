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

# Last changed: 2010 Mar 21
# Developed since: Mar 2010

import matplot3dext.renderers.interface
import keyconf

"""Renders point with optional colormaps for markeredgecolor and 
markerfacecolor."""


class ColormapPointRenderer(matplot3dext.renderers.interface.Renderer,
		keyconf.Configuration):
	"""Renders point using markeredgecolor and markerfacecolor to specify
	matplot3dext.colormapping.colormap.Colormap instances, used to color the
	respective parts of the points."""

	def __init__(self, **plot_kwargs):
		"""PLOT_KWARGS are handed mostly directly over to the plot command, 
		with exceptions for the kwargs colormap_markeredgecolor and 
		colormap_markerfacecolor.  Those must be matplot3dext.colormap.\
		interface.Colormap instances used to map the points onto color space.
		The resulting colors are used for the respective plot kwargs."""

		keyconf.Configuration.__init__(self)

		# Set defaults ...

		self.markeredgecolor = None
		self.markerfacecolor = None

		# Store the configuration ...

		self.colormaps = keyconf.Configuration()
		self.add_components(colormaps = self.colormaps)

		self.configure(**plot_kwargs)

	def render(self, point, backend):
		"""Render matplot3dext point POINT using backend BACKEND."""

		# By default use the configuration from self ...

		plot_kwargs = dict(self)  # Copies.

		# Check for colormap for markeredgecolor ...

		if self.colormaps.is_configured('markeredgecolor'):
			plot_kwargs.update(markeredgecolor = \
					self.colormap.get_config('markeredgecolor').\
					get_color(point))

		# Check for colormap for markerfacecolor ...

		if self.colormaps.is_configured('markerfacecolor'):
			plot_kwargs.update(markerfacecolor = \
					self.colormap.get_config('markerfacecolor').\
					get_color(point))
		
		# Render.

		backend.plot_point(point.position, **plot_kwargs)
