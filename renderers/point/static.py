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

"""Renders all points the same."""


class StaticPointRenderer(matplot3dext.renderers.interface.Renderer, 
		keyconf.Configuration):
	"""Renders all point the same."""

	def __init__(self, **plot_kwargs):
		"""PLOT_KWARGS will be directly forwarded to the plot command."""

		keyconf.Configuration.__init__(self)

		self.configure(**plot_kwargs)

	def render(self, point, backend):
		"""Render matplot3dext point POINT using backend BACKEND."""

		backend.plot_point(point.position, **self)
