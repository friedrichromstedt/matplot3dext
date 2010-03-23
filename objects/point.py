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

# Developed since: Mar 2010

import numpy

"""matplot3dext points."""


class Point:
	"""Matplot3dext point class."""

	def __init__(self, position, 
			renderers_point,
			renderers_line,
			renderers_face,
			world):
		"""Put point to position POSITION."""
	
		self.position = numpy.asarray(position)

		# Initialise empty attributes ...

		self.renderers_point = renderers_point
		self.renderers_line = renderers_line
		self.renderers_face = renderers_face

		self.attached_lines = set()
		self.attached_faces = set()

		world.add_point(self)

	#
	# Renderer addition ...
	#

	def attach_renderers(self, 
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

	def attach_line(self, line):
		"""Attach Line LINE.  Do not update the LINE's renderers.  Attaches
		also all Faces attached to LINE."""

		self.attached_lines.add(line)

		self.attached_faces |= line.attached_faces

	def detach_line(self, line):
		"""Detach Line LINE.  Also detaches the Faces attached to LINE."""

		self.attached_lines.remove(line)
		self.attached_faces -= line.attached_faces

	def attach_face(self, face):
		"""Attach Face FACE.  Do not update the FACE's renderers.  Assume that
		the .attached_lines of the FACE are already attached (do not attach
		the FACE's .attached_lines to self)."""

		self.attached_faces.add(face)

	def detach_face(self, face):
		"""Detach Face FACE."""

		self.attached_faces.remove(face)

	#
	# Subdivision framework ...
	#

	def subdivide(self, subdivision):
		"""Apply all renderers from the subdivision."""
		
		assert(subdivision.ndim == 0)

		self.attach_renderers(
				renderers_point = subdivision.renderers_point,
				renderers_line = subdivision.renderers_line,
				renderers_face = subdivision.renderers_face)

	#
	# Freeing memory ...
	#

	def destroy(self, world):
		"""Resolves reference loops.  Destroys all attached lines too."""

		for line in self.attached_lines:
			line.destroy()

		self.attached_lines = set()
		self.attached_faces = set()

		world.remove_point(self)
