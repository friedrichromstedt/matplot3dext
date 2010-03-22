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

import numpy

"""matplot3dext points."""


class Point:
	"""Matplot3dext point class."""

	def __init__(self, position, 
			renderers_point = None,
			renderers_line = None,
			renderers_face = None):
		"""Put point to position POSITION."""
	
		if renderers_point is None:
			renderers_point = set()
		if renderers_line is None:
			renderers_line = set()
		if renderers_face is None:
			renderers_face = set()

		self.position = numpy.asarray(position)

		# Initialise empty attributes ...

		self.renderers_point = renderers_point
		self.renderers_line = renderers_line
		self.renderers_face = renderers_face

		self.attached_lines = set()

	#
	# Renderer addition ...
	#

	def add_renderers(self, 
			renderers_point,
			renderers_line,
			renderers_face):
		"""Adds the renderers RENDERERS_POINT, RENDERERS_LINE, and
		RENDERERS_FACE to the Point.  Update lines attached."""

		self.renderers_point |= renderers_point
		self.renderers_line |= renderers_line
		self.renderers_face |= renderers_face

		for line in self.attached_lines:
			line.update_renderers_from_points()

	#
	# Connection methods ...
	#

	def add_line(self, line):
		"""Attach Line LINE.  Do not update the line's renderers."""

		self.attached_lines.add(line)

	def remove_line(self, line):
		"""Remove Line LINE."""

		self.attached_lines.remove(line)

	#
	# Subdivision framework ...
	#

	def subdivide(self, subdivision):
		"""Apply all renderers from the subdivision."""
		
		assert(subdivision.ndim == 0)

		self.add_renderers(
				renderers_point = subdivision.renderers_point,
				renderers_line = subdivision.renderers_line,
				renderers_face = subdivision.renderers_face)

	#
	# Freeing memory ...
	#

	def destroy(self):
		"""Resolves reference loops.  Destroys all attached lines too."""

		for line in self.attached_lines:
			line.destroy()

		del self.attached_lines
